import math
from PyNite import FEModel3D
import csv
from eng_module import utils
#from utils import str_to_int, str_to_float, read_csv_file

def calc_shear_modulus (nu: float, E: float) -> float:
    """
    Calculate the shear modulus for a material based on elastic moduluse "E" and Poisson's ration 'nu'

    Assume that the material is a linearly elastic isotropic material
    """   
    G = E / (2 * (1 + nu))
    return G


def euler_buckling_load (l: float, E: float, I: float, k: float) -> float:
    """
    Calculate the critical Euler buckling load for a certain column.
    "l" - Representing the length (height) of the column
    "E" - Representing the elastic modulus of the column material
    "I" - Representing the moment of inertia of the column section
    "k" - Representing the effective length factor
    """
    buckling_load = ((math.pi) ** 2 * E * I) / (k * l)**2
    return buckling_load

def beam_reactions_ss_cant (w: float, b: float, a: float) -> float:
    """
    Calculate reaction force
    w - Representing the magnitude of a uniform distributed load on the beam
    b - Representing the length of the backspan
    a - Representing the length of the cantilever
    """
    R2 = (w /(2 * b)) * (b**2 - a**2)
    R1 = (w / (2 * b)) * ((b + a) **2)
    return R1, R2

def fe_model_ss_cant (
    w: float,
    b: float, 
    a: float,
    E: float=1., 
    I: float=1.,
    A: float=1.,
    J: float=1.,
    nu: float=1.,
    rho: float=1.) -> FEModel3D:
    """
    Returns a PyNite beam model ready for analysis. The beam is going to be in the following configuration:
    |||||||||||||||||||||||| w
    ________________________
      ^ R2         o R1     
    |---b----------|--a-----|  
    """
    beam_model = FEModel3D()
    beam_model.add_node("N0",0, 0, 0)
    beam_model.add_node("N1",b, 0, 0)
    beam_model.add_node("N2",b + a, 0, 0)
    beam_model.def_support("N0", True, True, True, True, True, False)
    beam_model.def_support("N1", False, True, False, False, False, False)
    
    shear_modulus = calc_shear_modulus (E, nu)

    beam_model.add_material ("Material", E, shear_modulus, nu, rho)

    beam_model.add_member ("M0", "N0", "N2", "Material", Iy = I , Iz = I, J = J, A = A)

    beam_model.add_member_dist_load("M0", "Fy", w, w)

    return beam_model

#def read_beam_file (file_name: str) -> str:
    #"""
    #Returns a long string of text representing the text data in the file
    #"""
    #with open(file_name, 'r') as file:
    #    file_data = file.read()
    #    return file_data

def separate_lines (file_data: str) -> list[str]:
    """
    Takes file data that contains new line characters and separates them out into individual lines. 
    In other words, your function will return a list[str] where each item in the list will represent one line in the original file data.
    """
    separated_data = file_data.split('\n')
    return separated_data

def extract_data (beam_data: list[str], id: int) -> list[str]:
    """
    The function returns the data list item corresponding to the index separated out as their own list items (a list[str]).
    """
    beam_data_g = beam_data[id].split(", ")
    return beam_data_g

def get_spans (beam_length: float, cant_support_loc: float) -> tuple [float, float]:
    """
    Design a function called get_spans that takes a total beam length (a float) and the location of the cantilever support (a float) and returns the length of the backspan ("b") and the length of the cantilever ("a"), in that order. 
    The return type for this function will be tuple[float, float]
    """
    cant_length = beam_length - cant_support_loc
    simp_length = cant_support_loc
    return (simp_length,cant_length)

#def build_beam(beam_data: list[str]) -> FEModel3D:
    from PyNite import FEModel3D
    from eng_module import beams
    """
    Returns a beam finite element model for the data in 'beam_data' which is assumed to represent
    a simply supported beam with a cantilever at one end with a uniform distributed load applied
    in the direction of gravity.
    """
    LEI = extract_data(beam_data, 0)
    L = beams.str_to_float(LEI[0])
    E = beams.str_to_float(LEI[1])
    I = beams.str_to_float(LEI[2])
    supports_1_and_2 = extract_data(beam_data, 1)
    support_2 = beams.str_to_float(supports_1_and_2[1])
    load = beams.str_to_float(extract_data(beam_data, 2)[0])
    spans = get_spans(L, support_2)
    simp_length = spans[0]
    cant_length = spans[1]
    beam_model = beams.fe_model_ss_cant(load, simp_length, cant_length, E, I)
    return beam_model

#def load_beam_model (filename: str) -> FEModel3D:
    file_data = read_beam_file(filename)
    Eng_data = separate_lines(file_data)
    beam_model = build_beam(Eng_data)
    return beam_model

##################################### End of Workbook 2#####################################

#def read_beam_file (file_name: str) -> list:
#    """
#    Returns a long string of text representing the text data in the file
#    """
#    file_data = []
#    with open(file_name, 'r') as file:
#        for line in file.readlines():
#            file_data.append(line.replace("\n", ""))
#    return file_data

def separate_data (file_data: list[str]) -> list[list[str]]:
    """
    The functions purpose is to split up each individual line of data in the input
    """   
    beam_data = []
    for line_data in file_data:
        beam_data.append(line_data.split(", "))
    return beam_data

def convert_to_numeric(beam_data: list[list[str]]) -> list[list[float]]:
    """
    Separate our data, it would be convenient if all of the numeric data is converted into numbers
    """
    beam_ac_data = []
    for beam_line_data in beam_data:
        line_ac_data = []
        for data in beam_line_data:
            beam_ac = utils.str_to_float(data)
            line_ac_data.append(beam_ac)
        beam_ac_data.append(line_ac_data)
    return beam_ac_data

#def get_structured_beam_data (beam_data: list[list[str]]) -> dict:
#    """
#    This function will take a list[list[str]] as input and will return a dict. Because the dictionary is going to be heterogenous in shape (i.e. we cannot simply say it has keys of strings and values of float, for example), it is simplest just to leave the type annotation as dict
#    """
#    Eng_data = {}
#    Eng_data.update({"Name":beam_data[0][0]})
#    beam_data = convert_to_numeric(beam_data[1:])
#    #for beam_line_data in beam_data[0]:
#    Eng_data.update({"L":beam_data[0][0],"E":beam_data[0][1],"Iz":beam_data[0][2]})   
#    Eng_data.update({"Supports":beam_data[1],"Loads":beam_data[2:]})
#    #Eng_data.update(A)   
#    return Eng_data

#def get_node_locations(supports: list) -> dict[str, float]:
#    """
#    It will return a dict[str, float] meaning a dictionary with string keys and float values. 
#    """
#    node_loc = {}
#    for idx,support in enumerate(supports):
#        node_loc.update({f"N{idx}":support})
#    return node_loc

#def build_beam(beam_data: dict, A: float = 1., J: float = 1., nu: float = 1., rho: float = 1.) -> FEModel3D:
#    from PyNite import FEModel3D
#    from eng_module import beams
#    """
#    Returns a beam finite element model for the data in 'beam_data' which is assumed to represent
#    a simply supported beam with a cantilever at one end with a uniform distributed load applied
#    in the direction of gravity.
#    """
#    beam_model = FEModel3D()
#    L = beam_data["L"]
#    E = beam_data["E"]
#    I = beam_data["Iz"]
#    shear_moduls = beams.calc_shear_modulus(nu, E)
    
    #Add nodes
#    for idx, node in enumerate(beam_data["Supports"]):
#        beam_model.add_node(f"N{idx}",node, 0, 0)
#
#    #Def supports
#    beam_model.def_support("N0", True, True, True, True, True, False)
#
#    for idx_s, support in enumerate(beam_data["Supports"][1:], 1):
#        beam_model.def_support(f"N{idx_s}", False, True, False, False, False, False)
#    print(beam_data["Supports"])
#    #Add material
#    beam_model.add_material("Material", E, shear_moduls, nu, rho)
#    
#    #Add member
#    beam_model.add_member ("M1", "N0", f"N{idx}", "Material", Iy = I , Iz = I, J = J, A = A)
#    
#    #Add load combo
#    beam_model.add_load_combo("Combo 1", {"D":1})
#
#    #Add member load
#    for idx, loads in enumerate(beam_data["Loads"]):
#        beam_model.add_member_dist_load("M1", "Fy", loads[0], loads[0], loads[1], loads[2], case = "D")
#
#    return beam_model

def load_beam_model (filename: str) -> FEModel3D:
    file_data = utils.read_csv_file(filename)
    #Eng_data = separate_data(file_data)
    Struc_data = get_structured_beam_data(file_data)
    beam_model = build_beam(Struc_data)
    return beam_model


##################################### End of Workbook 3#####################################

def read_beam_file (file_name: str) -> list[list[str]]:
    """
    Returns a long string of text representing the text data in the file
    """
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        file_data = list(csv_reader)
    return utils.read_csv_file (file_data)

def parse_supports(supports: list[str]) -> dict[float, str]:
    """
    The function will take a list[str] representing a list of supports and returns a dict[float, str] meaning a dictionary with float keys and str values.
    Mainly used for supports
    """
    support = {}
    for support_detail in supports:
        loc, cond = support_detail.split(":")
        support.update({utils.str_to_float(loc):cond})
    return support

def parse_loads(loads:list[list[str|float]]) -> list[dict]:
    """
    To turn each sublist in the loads list into a structured dictionary.
    Mainly used for loads.
    """
    load_detail = []
    for load in loads:
        load_type, direc = load[0].split(":")
        if load_type == "POINT":
            load_detail.append(
                {"Type": load_type.title(), 
                 "Direction": direc, 
                 "Magnitude": load[1], 
                 "Location": load[2],
                 "Case": load[3].split(":")[1]
                }
            )  
        elif load_type == "DIST":
            load_detail.append(
                {"Type": load_type.title(),
                 "Direction": direc,
                 "Start Magnitude": load[1],
                 "End Magnitude": load[2],
                 "Start Location": load[3],
                 "End Location": load[4],
                 "Case": load[5].split(":")[1]
                }
            )
    return load_detail

def parse_beam_attributes(data_in_details:list[float]) -> dict[str, float]:
    """
     It takes one parameter, a list[float] representing the list of beam attributes on that second line of the file. 
     It returns a dictionary containing all of the beam attributes required for modelling the beam in PyNite (dict[str, float]).
    """
    beam_details = {"L": 1, 
                    "E": 1, 
                    "Iz": 1, 
                    "Iy": 1, 
                    "A": 1, 
                    "J": 1, 
                    "nu": 1, 
                    "rho": 1}
    for idx, beam_data in enumerate(data_in_details):
        cyc_idx = idx % 8
        if cyc_idx == 0:
            beam_details.update({"L": beam_data})
        elif cyc_idx == 1:
            beam_details.update({"E": beam_data})
        elif cyc_idx == 2:
            beam_details.update({"Iz": beam_data})
        elif cyc_idx == 3:
            beam_details.update({"Iy": beam_data})
        elif cyc_idx == 4:
            beam_details.update({"A": beam_data})
        elif cyc_idx == 5:
            beam_details.update({"J": beam_data})
        elif cyc_idx == 6:
            beam_details.update({"nu": beam_data})
        elif cyc_idx == 7:
            beam_details.update({"rho": beam_data})
    return beam_details

def get_structured_beam_data (beam_data: list[list[str]]) -> dict:
    """
    This function will take a list[list[str]] as input and will return a dict. Because the dictionary is going to be heterogenous in shape (i.e. we cannot simply say it has keys of strings and values of float, for example), it is simplest just to leave the type annotation as dict
    """
    Eng_data = {}
    Eng_data.update({"Name":beam_data[0][0]})
    beam_data = convert_to_numeric(beam_data[1:])
    Eng_data.update(parse_beam_attributes(beam_data[0]))
    Eng_data.update({"Supports":parse_supports(beam_data[1]),"Loads":parse_loads(beam_data[2:])})
    return Eng_data

def get_node_locations(supports: list, beam_length: float) -> dict[str, float]:
    """
    It will return a dict[str, float] meaning a dictionary with string keys and float values. 
    """
    node_loc = {}
    if supports[0] != 0:
        node_loc.update({"N0":0})
        for idx,support in enumerate(supports,1):
            node_loc.update({f"N{idx}":support})
    else:
        for idx,support in enumerate(supports,0):
            node_loc.update({f"N{idx}":support})
    if support != beam_length:
        node_loc.update({f"N{idx+1}":beam_length})
    return node_loc

def build_beam(beam_data: dict) -> FEModel3D:
    from PyNite import FEModel3D
    from eng_module import beams
    """
    Returns a beam finite element model for the data in 'beam_data' which is assumed to represent
    a simply supported beam with a cantilever at one end with a uniform distributed load applied
    in the direction of gravity.
    """
    beam_model = FEModel3D()
    L = beam_data["L"]
    E = beam_data["E"]
    I = beam_data["Iz"]
    nu = beam_data["nu"]
    rho = beam_data["rho"]
    J = beam_data["J"]
    A = beam_data["A"]
    shear_moduls = beams.calc_shear_modulus(nu, E)
    
    #Add nodes
    nodes_summ = []

    for node in beam_data["Supports"]:
        nodes_summ.append(node)

    Support_summ = get_node_locations(nodes_summ, L)
    for node in Support_summ:
        beam_model.add_node(node, Support_summ[node], 0, 0)

    #Def supports
    for item, loc in Support_summ.items():
        for pos, supp_type in beam_data["Supports"].items():
            if loc == pos:
                if supp_type == "F":
                    beam_model.def_support(item, True, True, True, True, True, True)
                elif supp_type == "P":
                    beam_model.def_support(item, True, True, True, True, True, False)
                elif supp_type == "R":
                    beam_model.def_support(item, False, True, False, False, False, False)
    
    #Add material
    beam_model.add_material("Material", E, shear_moduls, nu, rho)
    
    #Add member
    beam_model.add_member ("Test Beam", "N0", node, "Material", Iy = I , Iz = I, J = J, A = A)
    
    #Add load combo
    #beam_model.add_load_combo("Combo 1", {"Dead":1, "Live":1})
    #beam_model.add_load_combo("Combo 2", {"D":1, "L":1})
    #beam_model.add_load_combo("D", {"D":1})
    #beam_model.add_load_combo("L", {"L":1})
    #Add member load
    for load in beam_data["Loads"]:
        if load["Type"] == "Point":
            beam_model.add_member_pt_load("Test Beam", load["Direction"], load["Magnitude"], load["Location"], load["Case"])
            beam_model.add_load_combo(load["Case"], {load["Case"]:1})
        elif load["Type"] == "Dist":
            beam_model.add_member_dist_load("Test Beam", load["Direction"], load["Start Magnitude"], load["End Magnitude"], load["Start Location"], load["End Location"], load["Case"])
            beam_model.add_load_combo(load["Case"], {load["Case"]:1})

    return beam_model