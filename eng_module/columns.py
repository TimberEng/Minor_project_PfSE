from dataclasses import dataclass
from eng_module import utils
from eng_module import load_factors
import math

@dataclass
class Column:
    """
    A data type to describe the column details.
    
    h: Clear height of column
    E: Elastic modulus
    A: Cross-sectional area
    Ix: Second moment of area about the x-axis
    Iy:Second moment of area about the y-axis
    Lex: The (Euler) effective length factor about the x-axis
    Ley: The (Euler) effective length factor about the y-axis
    """
    h: int
    E: int
    A: float
    Ix: float
    IY: float
    kx: float
    ky: float
    def critical_buckling_load (self, axis: str):
        """
        Returns the buckling load about the requested 'axis'.
        'axis': one of either 'x' or 'y'
        """
        if axis == 'x':
            return euler_buckling_load(self.h, self.E, self.Ix, self.kx)
        elif axis == 'y':
            return euler_buckling_load(self.h, self.E, self.IY, self.ky)
        else:
            raise ValueError(f"Axis must be one of 'x' or 'y', not {axis}")
        
    def radius_of_gyration (self, axis: str):
        """
        Returns the buckling load about the requested 'axis'.
        'axis': one of either 'x' or 'y'
        """
        if axis == 'x':
            return radius__gyration(self.Ix, self.A)
        elif axis == 'y':
            return radius__gyration(self.IY, self.A)
        else:
            raise ValueError(f"Axis must be one of 'x' or 'y', not {axis}")       



def euler_buckling_load (h: float, E: float, I: float, k: float) -> float:
    """
    Calculate the critical Euler buckling load for a certain column.
    """
    return ((math.pi) ** 2 * E * I) / (k * h)**2

def radius__gyration (I: float, A: float) -> float:
    """
    Calculate the radius of gyration
    """
    return math.sqrt(I/A)

@dataclass
class SteelColumn(Column):
    """
     inherit from Column
    """
    tag: str
    fy: float
    n: float
    phi:float = 0.9

    def factored_crushing_load(self):
        return crushing_load(self.A, self.fy)

    def factored_compressive_resistance (self):
        return compressive_resistance(self.A, self.fy)
    
def crushing_load(A: float, fy: float) -> float:
    """
    calculate the axial compressive resistance for a short column
    """
    return A * fy
 
def compressive_resistance(A: float, fy: float, t: float = 10, lamb_ey: float = 45) -> float:
    """
    calculate the axial compressive resistance including slenderness effects
    """
    b = A / t
    lamb_e = (b / t)*math.sqrt(fy/252)
    be = b * (lamb_ey / lamb_e)
    if be <= b:
        be = be
    else:
        be = b

    Ae = be * t
    Ag = b * t
    kf = Ae / Ag

    An = b * t
    return kf * An * fy

def csv_record_to_steelcolumn(record: list[str], **kwargs) -> SteelColumn:
    """
    Returns a SteelColumn populated with the data in 'record' and **kwargs
    """
    sc = SteelColumn(
        h=utils.str_to_float(record[2]), 
        A=utils.str_to_float(record[1]), 
        E=utils.str_to_float(record[6]), 
        Ix=utils.str_to_float(record[3]), 
        Iy=utils.str_to_float(record[4]), 
        kx=utils.str_to_float(record[7]), 
        ky=utils.str_to_float(record[8]), 
        fy=utils.str_to_float(record[5]),
        tag = utils.str_to_float(record[0]),
        dead_load = utils.str_to_float(record[9]),
        live_load = utils.str_to_float(record[10]),
        **kwargs
    )

    return sc

def convert_csv_data_to_steelcolumns(csv_data: list[list[str]], **kwargs) -> list[SteelColumn]:
    """
    Converts all of the data in the csv file into a list of SteelColumn that are ready to do further work.
    """
    
    steel_column=[]
    for line_data in csv_data:
        steel_column.append(csv_record_to_steelcolumn(line_data, **kwargs))
        
    return steel_column

def calculate_factored_csv_load(record: list[str]) -> float:
    """
    To calculate a maximum factored load, according to your load combinations and assumptions, based on the dead load and live load data present in one row of the csv file
    """
    loads={"D_load":utils.str_to_float(record[-2]),
          "L_load":utils.str_to_float(record[-1])}
    max_load = load_factors.max_factored_load(loads, load_factors.NBCC_2020_COMBINATIONS)
    return max_load

def run_all_columns(filename, **kwargs) -> list[SteelColumn]:
    """
    This function will read the data in the CSV file and will return a list of SteelColumn based on the data in the CSV file but also with two additional attributes added that are populated with a factored load and demand/capacity ratio of each column under the applied loading
    """
    SteelColumn = []
    raw_data = utils.read_csv_file(filename)[1:]
    for data in raw_data:
        max_load = calculate_factored_csv_load(data)
        test = csv_record_to_steelcolumn(data, max_load = 100)

    return SteelColumn