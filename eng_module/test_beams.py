from eng_module import beams
import pytest
import math


def test_calc_shear_modulus ():
    E_1 = 200000
    nu_1 = 0.3

    E_2 = 3645
    nu_2 = 0.2

    assert beams.calc_shear_modulus (nu_1, E_1) == 76923.07692307692
    assert beams.calc_shear_modulus (nu_2, E_2) == 1518.75

def test_euler_buckling_load ():
    l = 5300 # mm
    E = 200000 # MPa
    I = 632e6 # mm**4
    k = 1.0

    assert beams.euler_buckling_load(l, E, I, k) == 44411463.02234584

    l = 212 # inch
    E = 3645 # ksi ("ksi" == "kips per square inch")
    I = 5125.4 # inch**4
    k = 2.0
    assert beams.euler_buckling_load(l, E, I, k) == 1025.6361727834453

#def test_beam_reactions_ss_cant ():
    # Beam 1
    #w = 50 # kN/m (which is the same as N/mm)
    #a = 2350 # mm
    #b = 4500 # mm

    #assert beams.beam_reactions_ss_cant (w, b, a) == (260680.55555555556, 81819.44444444445)

    # Beam 2 # Equal spans; should get 0.0 at backspan reaction
    #w = 19 # lbs/inch == 228 lbs/ft
    #a = 96 # inch
    #b = 96 # inch
    #assert beams.beam_reactions_ss_cant (w, b, a) == (3648.0, 0.0)

#def test_fe_model_ss_cant():
    #beam_model1= beams.fe_model_ss_cant(-10, 10, 10)
    #beam_model1.analyze_linear()
    #n0 = beam_model1.Nodes['N0'].RxnFY['Combo 1']
    #n1 = beam_model1.Nodes['N1'].RxnFY['Combo 1']

    #assert math.isclose (n0, 0, abs_tol=1e-6)
    #assert math.isclose(n1, 200, abs_tol=1e-6)

################## End of Workbook 1 #####################

#def test_read_beam_file():
    #beam1_data = beams.read_beam_file('eng_module/test_data/beam_1.txt')
    #assert beam1_data == '4800, 200000, 437000000\n0, 3000\n-10'

#def test_separate_lines():
    #beam_1 = beams.read_beam_file('eng_module/test_data/WB_2_beam_1.txt')
    #beam_1_line = beams.separate_lines(beam_1)
    #assert beam_1_line == ['4800, 200000, 437000000', '0, 3000', '-10']

#def test_extract_data():
    #beam_1 = beams.read_beam_file('eng_module/test_data/beam_1.txt')
    #beam_1_line = beams.separate_lines(beam_1)
    #beam_1_str_0 = beams.extract_data(beam_1_line, 0)
    #beam_1_str_1 = beams.extract_data(beam_1_line, 1)
    #assert beam_1_str_0 == ['4800', '200000', '437000000']
    #assert beam_1_str_1 == ['0', '3000']

def test_get_spans():
    beam_length_1 = 10
    cant_support_loc_1 = 7
    spans_1 = beams.get_spans(beam_length_1, cant_support_loc_1)
    beam_length_2 = 4000
    cant_support_loc_2 = 2500
    spans_2 = beams.get_spans(beam_length_2, cant_support_loc_2)
    assert spans_1 == (7, 3)
    assert spans_2 == (2500, 1500)

#def test_read_beam_file():
#    beam1_data = beams.read_beam_file('eng_module/test_data/WB_3_beam_1.txt')
#    assert beam1_data == ['Roof beam', '4800, 19200, 1000000000', '0, 3000, 4800', '-100, 500, 4800', '-200, 3600, 4800']

#def test_separate_data():
#    raw_data = ['Roof beam',  '4800, 19200, 1000000000', '0, 3000', '100, 500, 4800', '200, 3600, 4800']
#    New_data = beams.separate_data(raw_data)
#
#    assert New_data == [['Roof beam'],  ['4800', '19200', '1000000000'], ['0', '3000'], ['100', '500', '4800'], ['200', '3600', '4800']]

def test_convert_to_numeric():
    Str = [['4800', '19200', '1000000000'], ['0', '3000'], ['100', '500', '4800'], ['200', '3600', '4800']]
    num = beams.convert_to_numeric(Str)

    assert num == [[4800.0, 19200.0, 1000000000.0], [0.0, 3000.0], [100.0, 500.0, 4800.0], [200.0, 3600.0, 4800.0]]

#def test_get_structured_beam_data():
#    str_data_raw = [['Roof beam'], ['4800', '19200', '1000000000'], ['0', '3000'], ['100', '500', '4800'], ['200', '3600', '4800']]
#    str_data_new = beams.get_structured_beam_data(str_data_raw)
#    assert str_data_new == {'Name': 'Roof beam', 'L': 4800.0, 'E': 19200.0, 'Iz': 1000000000.0, 'Supports': [0.0, 3000.0], 'Loads': [[100.0, 500.0, 4800.0], [200.0, 3600.0, 4800.0]]}

#def test_get_node_locations():
#    supports =  [0.0, 3000.0, 4800.0]
#    support = beams.get_node_locations(supports)
#
#    assert support == {"N0": 0.0, "N1": 3000.0, "N2": 4800.0}

################## End of Workbook 3 #####################

#def test_read_beam_file():
#    raw_data = beams.read_beam_file('eng_module/test_data/beam_1.txt')
#    assert raw_data == [['Balcony transfer'], ['4800', '24500', '1200000000', '1', '1'], ['1000:P', '3800:R'], ['POINT:Fy', '-10000', '4800', 'case:Live'], ['DIST:Fy', '30', '30', '0', '4800', 'case:Dead']]

def test_parse_supports():
    raw = ['1000:P', '3800:R', '4800:F', '8000:R']
    new = beams.parse_supports(raw)
    assert new == {1000: 'P', 3800: 'R', 4800: 'F', 8000: 'R'}

def test_parse_loads():
    raw =[['POINT:Fy', -10000.0, 4800.0, 'case:Live'],
    ['DIST:Fy', 30.0, 30.0, 0.0, 4800.0, 'case:Dead']]
    new = beams.parse_loads(raw)
    assert new == [
                    {
                        "Type": "Point", 
                        "Direction": "Fy", 
                        "Magnitude": -10000.0, 
                        "Location": 4800.0, 
                        "Case": "Live"
                    },
                    {
                        "Type": "Dist", 
                        "Direction": "Fy",
                        "Start Magnitude": 30.0,
                        "End Magnitude": 30.0,
                        "Start Location": 0.0,
                        "End Location": 4800.0,
                        "Case": "Dead"
                    }
                ]
    
def test_parse_beam_attributes():
    input_1 = [20e3, 200e3, 6480e6, 390e6, 43900, 11900e3, 0.3]
    output_1 = beams.parse_beam_attributes(input_1)
    assert output_1 == {'L': 20000.0,
                        'E': 200000.0,
                        'Iz': 6480000000.0,
                        'Iy': 390000000.0,
                        'A': 43900,
                        'J': 11900000.0,
                        'nu': 0.3,
                        'rho': 1}
    
def test_get_structured_beam_data():
    raw_beam = [['Balcony transfer'],
                ['4800', '24500', '1200000000', '1', '1'],
                ['1000:P', '3800:R'],
                ['POINT:Fy', '-10000', '4800', 'case:Live'],
                ['DIST:Fy', '30', '30', '0', '4800', 'case:Dead']]
    new_beam = beams.get_structured_beam_data(raw_beam)
    assert new_beam == {'Name': 'Balcony transfer',
                        'L': 4800.0,
                        'E': 24500.0,
                        'Iz': 1200000000.0,
                        'Iy': 1.0,
                        'A': 1.0,
                        'J': 1.0,
                        'nu': 1.0,
                        'rho': 1.0,
                        'Supports': {1000.0: 'P', 3800.0: 'R'},
                        'Loads': [{'Type': 'Point',
                        'Direction': 'Fy',
                        'Magnitude': -10000.0,
                        'Location': 4800.0,
                        'Case': 'Live'},
                        {'Type': 'Dist',
                        'Direction': 'Fy',
                        'Start Magnitude': 30.0,
                        'End Magnitude': 30.0,
                        'Start Location': 0.0,
                        'End Location': 4800.0,
                        'Case': 'Dead'}]}

def test_get_node_locations():
    beam_length_1 = 10000.0
    supports_1 = [1000.0, 4000.0, 8000.0]

    beam_length_2 = 210.0
    supports_2 = [0.0, 210.0]

    node_1 = beams.get_node_locations(supports_1, beam_length_1)
    node_2 = beams.get_node_locations(supports_2, beam_length_2)
    assert node_1 == {"N0": 0.0, "N1": 1000.0, "N2": 4000.0, "N3": 8000.0, "N4": 10000.0}
    assert node_2 == {"N0": 0.0, "N1": 210.0}