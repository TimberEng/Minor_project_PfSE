from PyNite import FEModel3D
from math import sqrt
from math import tan
from math import radians
from Structural_Analysis import analysis
from eng_module import utils

#############################

def build_frame(H, L, w, ang_d):
    """
    H, l, w, ang_d
    """
    
    frame_model = FEModel3D() # Creates an empty model
    H  # mm
    L  # mm
    w  # N/mm
    ang = radians (ang_d) # rad

    #Add nodes
    frame_model.add_node("node1",0,0,0)
    frame_model.add_node("node2",0,H,0)
    frame_model.add_node("node3",L/2,H+((L/2)*tan(ang)),0)
    frame_model.add_node("node4",L,H,0)
    frame_model.add_node("node5",L,0,0)

    m = (L/2)**2 + 500**2
    member_length = sqrt(m)

    #Define material
    I_1 = 9050000.0 # mm*4
    I_2 = 672000.0 # mm*4
    J = 60500.0 # mm*4
    A = 2300 # mm*2
    frame_model.add_material(name='Steel', E=200e3, G=80e3, nu=0.25, rho=7.85e-6)
    
    #Add frame members
    frame_model.add_member('M1', 'node1', 'node2', 'Steel', I_2, I_1, J, A)
    frame_model.add_member('M2', 'node2', 'node3', 'Steel', I_2, I_1, J, A)
    frame_model.add_member('M3', 'node3', 'node4', 'Steel', I_2, I_1, J, A)
    frame_model.add_member('M4', 'node4', 'node5', 'Steel', I_2, I_1, J, A)
    
    #Add load
    frame_model.add_load_combo('L',{"D":1})
    frame_model.add_member_dist_load("M1", "Fy", -w, -w, 0, H, case="D")
    frame_model.add_member_dist_load("M2", "Fy", -w, -w, 0, member_length, case="D")
    frame_model.add_member_dist_load("M3", "Fy", -w, -w, 0, member_length, case="D")
    frame_model.add_member_dist_load("M4", "Fy", w, w, 0, H, case="D")

    #Add boundary condition
    frame_model.def_support('node1', True, True, True, True, True, True)
    frame_model.def_support('node5', True, True, True, True, True, True)

    frame_model.analyze()
    
    return frame_model

def find_max_moment(frame_model):
    #max momemnt
    moment_max_1=abs(frame_model.Members['M1'].max_moment('Mz', combo_name = 'L')/10**6)
    moment_max_2=abs(frame_model.Members['M2'].max_moment('Mz', combo_name = 'L')/10**6)
    moment_max_3=abs(frame_model.Members['M3'].max_moment('Mz', combo_name = 'L')/10**6)
    moment_max_4=abs(frame_model.Members['M4'].max_moment('Mz', combo_name = 'L')/10**6)
    #min moment
    moment_min_1=abs(frame_model.Members['M1'].min_moment('Mz', combo_name = 'L')/10**6)
    moment_min_2=abs(frame_model.Members['M2'].min_moment('Mz', combo_name = 'L')/10**6)
    moment_min_3=abs(frame_model.Members['M3'].min_moment('Mz', combo_name = 'L')/10**6)
    moment_min_4=abs(frame_model.Members['M4'].min_moment('Mz', combo_name = 'L')/10**6)
    return max (moment_max_1, moment_max_2, moment_max_3, moment_max_4, moment_min_1, moment_min_2, moment_min_3, moment_min_4)

def  find_max_shear(frame_model):
    #max shear
    shear_max_1=abs(frame_model.Members['M1'].max_shear('Fy', combo_name = 'L')/10**3)
    shear_max_2=abs(frame_model.Members['M2'].max_shear('Fy', combo_name = 'L')/10**3)
    shear_max_3=abs(frame_model.Members['M3'].max_shear('Fy', combo_name = 'L')/10**3)
    shear_max_4=abs(frame_model.Members['M4'].max_shear('Fy', combo_name = 'L')/10**3)
    #min shear
    shear_min_1=abs(frame_model.Members['M1'].min_shear('Fy', combo_name = 'L')/10**3)
    shear_min_2=abs(frame_model.Members['M2'].min_shear('Fy', combo_name = 'L')/10**3)
    shear_min_3=abs(frame_model.Members['M3'].min_shear('Fy', combo_name = 'L')/10**3)
    shear_min_4=abs(frame_model.Members['M4'].min_shear('Fy', combo_name = 'L')/10**3)
    return max(shear_max_1, shear_max_2, shear_max_3, shear_max_4, shear_min_1, shear_min_2, shear_min_3, shear_min_4)

def find_max_vertical(frame_model):
    #Vertical Displacement
    displ_vmax_1 = abs(frame_model.Members['M1'].max_deflection('dy', combo_name="L"))
    displ_vmax_2 = abs(frame_model.Members['M2'].max_deflection('dy', combo_name="L"))
    displ_vmax_3 = abs(frame_model.Members['M3'].max_deflection('dy', combo_name="L"))
    displ_vmax_4 = abs(frame_model.Members['M4'].max_deflection('dy', combo_name="L"))
    displ_vmin_1 = abs(frame_model.Members['M1'].min_deflection('dy', combo_name="L"))
    displ_vmin_2 = abs(frame_model.Members['M2'].min_deflection('dy', combo_name="L"))
    displ_vmin_3 = abs(frame_model.Members['M3'].min_deflection('dy', combo_name="L"))
    displ_vmin_4 = abs(frame_model.Members['M4'].min_deflection('dy', combo_name="L"))
    
    return max(displ_vmax_1, displ_vmax_2, displ_vmax_3, displ_vmax_4, displ_vmin_1, displ_vmin_2, displ_vmin_3, displ_vmin_4)

def find_max_horizontal(frame_model):
    #Vertical Displacement
    displ_hmax_1 = abs(frame_model.Members['M1'].max_deflection('dx', combo_name="L"))
    displ_hmax_2 = abs(frame_model.Members['M2'].max_deflection('dx', combo_name="L"))
    displ_hmax_3 = abs(frame_model.Members['M3'].max_deflection('dx', combo_name="L"))
    displ_hmax_4 = abs(frame_model.Members['M4'].max_deflection('dx', combo_name="L"))
    displ_hmin_1 = abs(frame_model.Members['M1'].min_deflection('dx', combo_name="L"))
    displ_hmin_2 = abs(frame_model.Members['M2'].min_deflection('dx', combo_name="L"))
    displ_hmin_3 = abs(frame_model.Members['M3'].min_deflection('dx', combo_name="L"))
    displ_hmin_4 = abs(frame_model.Members['M4'].min_deflection('dx', combo_name="L"))
    
    return max(displ_hmax_1, displ_hmax_2, displ_hmax_3, displ_hmax_4, displ_hmin_1, displ_hmin_2, displ_hmin_3, displ_hmin_4)

def get_list (frame_model) -> list[list]:
    shear_list = []
    moment_list = []
    vertical_list = []
    horizontal_list = []
    for idx, member in frame_model.Members.items():
        shear_list.append(member.shear_array("Fy",n_points=1000, combo_name="L"))
        moment_list.append(member.moment_array("Mz", n_points=1000, combo_name="L"))
        vertical_list.append(member.deflection_array("dy",n_points=1000,combo_name="L"))
        horizontal_list.append(member.deflection_array("dx", n_points=1000, combo_name="L"))
    return shear_list, moment_list, vertical_list, horizontal_list

def get_nodes(frame_model) -> list:
    X = []
    Y = []
    for item in frame_model.Nodes.values():
        X.append(item.X)
        Y.append(item.Y)
    return X, Y

section_data = utils.read_csv_file("section.csv")   

analysis.csv_record_to_Isction(section_data[1])
