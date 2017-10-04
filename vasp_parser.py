
import numpy as np

def parser_function():
    """
    Parses the vasprun.xml.
    """

    ####################################################################
    # Use xml library to get born charges adn epsilon
    ####################################################################

    from pymatgen.io.vasp import Vasprun

    try:
        import xml.etree.cElementTree as ET

        tree = ET.parse('vasprun.xml')
        root = tree.getroot()

        for elements in root.iter('varray'):
            if elements.attrib['name'] == 'epsilon':
                epsilon = []
                for row in elements:
                    epsilon.append(np.array(row.text.split(), dtype=float))

                epsilon = np.array(epsilon)
                break

        for elements in root.iter('array'):
            try:
                if elements.attrib['name'] == 'born_charges':
                    born_charges = []
                    for atom in elements[1:]:
                        atom_array = []
                        for c in atom:
                            atom_array.append(np.array(c.text.split(), dtype=float))
                        born_charges.append(atom_array)

                    born_charges = np.array(born_charges)

                    break
            except KeyError:
                pass
    except:
        pass

    #########################################################################
    # Use pymatgen vasp parser to get atomic forces, stress tensor and energy
    #########################################################################

    vspr = Vasprun('vasprun.xml',
                   exception_on_bad_xml=False,
                   parse_potcar_file=False)

    # Get forces using pymatgen
    forces = np.array([vspr.ionic_steps[-1]['forces']])
    stress = np.array(vspr.ionic_steps[-1]['stress'])

    vasp_param = {}
    # vasp_param['final_energy'] = vspr.final_energy  # This includes PV
    vasp_param['energy'] = vspr.ionic_steps[-1]['electronic_steps'][-1][
        'e_wo_entrp']  # Pure internal energy (U) as appear in OUTCAR

    return {'epsilon': epsilon,
            'born_charges': born_charges,
            'forces': forces,
            'stress': stress,
            'parameters': vasp_param}


parsed_data = parser_function()

for item in parsed_data.items():
    print item[0]
    print item[1]