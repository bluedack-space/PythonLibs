import numpy as np

class ConvertTable():
    
    def __init__(self):
        print("This is constructor of ConvertTable")
        
    @staticmethod
    def getNumpyTable(tab):
        if type(tab) is np.ndarray:
            tab_np = tab
        elif type(tab) is pd.core.frame.DataFrame:
            tab_np = np.zeros(tab.shape[0], dtype=[(tab.columns[i],'f8') for i in range(tab.shape[1])])
            for irow in range(tab.shape[0]):
                for icol in range(tab.shape[1]):
                    tab_np[irow][icol] = tab.values[irow][icol]
        else:
            tab_np = None
        return tab_np
    
    @staticmethod
    def getPandasTable(tab):
        if type(tab) is np.ndarray:
            tab_pd = pd.DataFrame(tab)
        elif type(tab) is pd.core.frame.DataFrame:
            tab_pd = tab
        else:
            tab_pd = None
        return tab_pd
    
#_/_/_/_/ Initialize Numpy Array with Column Name
# (1) Initialize Matrix
tab = np.zeros(3, dtype=[('V1','f8'), ('V2','f8'), ('V3','f8')])
# (2) Read from file
#tab = np.genfromtxt( "test.csv", skip_header=1, delimiter=",", dtype=[('V1', 'f8'), ('V2', 'f8'), ('V3', 'f8')] )
tab[0][0] = 1.0
tab[1][1] = 2.0
tab[2][2] = 3.0

# Display Table Contents
print(tab)
# Display Table Column Names
print(tab.dtype.names)

#_/_/_/_/ Convert to Pandas DataFrame
import pandas as pd
# Convet to pandas table
df = pd.DataFrame(tab)
# Display Pandas Dataframe
print(df)

#_/_/_/_/ Convert Pandas DataFrame to Numpy Table
tab_np = ConvertTable.getNumpyTable(df)
print("\n >>Converted to Numpy Table:\n")
print(tab_np)
print(tab_np.dtype.names)

#_/_/_/_/ Convert Numpy Table to Pandas DataFrame
tab_pd = ConvertTable.getPandasTable(tab)
print("\n >>Converted to Pandas Dataframe:\n")
print(tab_pd)
