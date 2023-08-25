import pandas as pd
import numpy as np
from scipy.spatial import KDTree
from importlib.resources import files

# get data from package so we do not need
# to read csv directly, data comes from geonames
data = files("geonames").joinpath("geonames.csv").open('rb')
df = pd.read_csv(data, sep=";")[['Geoname ID', 'Name', 'ASCII Name', 'Alternate Names','Country Code',
        'Country name EN', 'Population', 'Timezone','Modification date', 'LABEL EN', 'Coordinates']]

# create two columns for Longitude and Latitude
# this comes from splitting the coordinates column
latLong = df['Coordinates'].str.split(",", expand=True).iloc[:, ::-1]
latLong.rename(columns={0:"Latitude", 1:"Longitude"}, inplace=True)
latLong["Longitude"] = latLong["Longitude"].str.lstrip()
df = pd.concat([df,latLong], axis=1)

# Create a KDTree from Longitude and Latitude
tree = KDTree(df[["Latitude","Longitude"]].values)

# Function for finding the closest city given
# [Longitude, Latitude]
# can also input a list of Longitude and Latitude
# [[Longitude1, Latitude1], [Longitude2, Latitude2]]
def search(coordinates:[list], k:int=1, output:dict | pd.DataFrame='df', ascending:bool=None) -> dict | pd.DataFrame:
    """
    This function will search GeoNames dataset for the closest city given the inputted Longitude and Latitude coordinates.

    PARAMETERS
    ----------
    - coordinates: Required - list or list(list) 
        
        Search query allows a list of Latitude and Longitude, or a single pair which must be passed as list. It will return name of the nearest city in the same order which the coordinates were passed.
        
        Example:

        single location: coordinates = [11.86, -86.24]

        multiple locations: coordinates = [[11.86, -86.24], [42, 49]]
    
    - k: Optional - int > 1, Default: int = 1
        
        Number of of nearest neighbours to find for each set of coordinates. Must be a value greater than zero.
    
    - output: Optional - 'df' or 'dict', default: output = 'df'
        
        Which format to return to users. Either pandas DataFrame or dictionary.
    
    - ascending: Optional - True or False, default: None

        If the format should be sorted by ascending, descending population, or no sorting at all. This can help in finding the nearest city with the largest population (might need to increase k).
        
    RETURNS
    ----------
    - Dictionary{Dictionary}: Key:Value{Dictionary} - info
        
    - 'Geoname ID'
    - 'Name' - (City Name)
    - 'ASCII Name' - (City Name in ASCII)
    - 'Alternate Names' - (Alternate names for the city, or a list of alternate names)
    - 'Country Code'
    - 'Country name EN'
    - 'Population'
    - 'Timezone'
    - 'Modification date' - (Date this data point was updated)
    - 'LABEL EN'
    - 'Coordinates'
    - 'Longitude'
    - 'Latitude'

    EXAMPLES
    ----------

    - Search for the nearest city's name from a single coordinate.

    >>> import pygeocity
    >>> geonames.search([11.85812, -86.23922])

    Outputs:

    {'Geoname ID': {0: 3620170},

    'Name': {0: 'Diriamba'},

    'ASCII Name': {0: 'Diriamba'},

    'Alternate Names': {0: 'Diriamba,Diriambo'},

    'Country Code': {0: 'NI'},

    'Country name EN': {0: 'Nicaragua'},

    'Population': {0: 35008},

    'Timezone': {0: 'America/Managua'},

    'Modification date': {0: '2018-08-08'},

    'LABEL EN': {0: 'Nicaragua'},

    'Coordinates': {0: '11.85812, -86.23922'},

    'Longitude': {0: '-86.23922'},

    'Latitude': {0: '11.85812'}}

    - Search for the nearest city's name from two coordinates.

    >>> geonames.search([11.85812, -86.23922],[12.4825, -87.17304])

    Outputs:
    {'CoordIndex': {0: 1, 1: 0},

    'Geoname ID': {0: 584715, 1: 3620170},

    'Name': {0: 'Xudat', 1: 'Diriamba'},

    'ASCII Name': {0: 'Xudat', 1: 'Diriamba'},

    'Alternate Names': {0: 'Khudaf,Khudat,Xudat,Худат', 1: 'Diriamba,Diriambo'},

    'Country Code': {0: 'AZ', 1: 'NI'},

    'Country name EN': {0: 'Azerbaijan', 1: 'Nicaragua'},

    'Population': {0: 13625, 1: 35008},

    'Timezone': {0: 'Asia/Baku', 1: 'America/Managua'},

    'Modification date': {0: '2014-06-26', 1: '2018-08-08'},

    'LABEL EN': {0: 'Azerbaijan', 1: 'Nicaragua'},

    'Coordinates': {0: '41.63052, 48.68161', 1: '11.85812, -86.23922'},

    'Longitude': {0: '48.68161', 1: '-86.23922'},

    'Latitude': {0: '41.63052', 1: '11.85812'}}

    - Search for the two nearest cities name from two coordinates.

    >>> geonames.search([[11.85812, -86.23922],[12.4825, -87.17304]], k=2)

    Outputs:

    {'CoordIndex': {0: 0, 1: 0, 2: 1, 3: 1},

    'Geoname ID': {0: 3620163, 1: 3620170, 2: 498904, 3: 584715},

    'Name': {0: 'Dolores', 1: 'Diriamba', 2: 'Samur', 3: 'Xudat'},

    'ASCII Name': {0: 'Dolores', 1: 'Diriamba', 2: 'Samur', 3: 'Xudat'},

    'Alternate Names': {0: 'Dolores',

    1: 'Diriamba,Diriambo',

    2: 'Samur,Самур',

    3: 'Khudaf,Khudat,Xudat,Худат'},
    'Country Code': {0: 'NI', 1: 'NI', 2: 'RU', 3: 'AZ'},

    'Country name EN': {0: 'Nicaragua',

    1: 'Nicaragua',

    2: 'Russian Federation',

    3: 'Azerbaijan'},

    'Population': {0: 7065, 1: 35008, 2: 3730, 3: 13625},

    'Timezone': {0: 'America/Managua',

    1: 'America/Managua',

    2: 'Europe/Moscow',

    3: 'Asia/Baku'},

    'Modification date': {0: '2018-08-08',

    1: '2018-08-08',

    2: '2012-01-17',

    3: '2014-06-26'},

    'LABEL EN': {0: 'Nicaragua',

    1: 'Nicaragua',

    2: 'Russian Federation',

    ...

    1: '11.85812, -86.23922',

    2: '41.82527, 48.48597',

    3: '41.63052, 48.68161'},

    'Longitude': {0: '-86.21552', 1: '-86.23922', 2: '48.48597', 3: '48.68161'},

    'Latitude': {0: '11.85672', 1: '11.85812', 2: '41.82527', 3: '41.63052'}}

    - Search for the two nearest cities name from two coordinates and return the output with the cities population in descending order.

    >>> geonames.search([[11.85812, -86.23922],[12.4825, -87.17304]], k=2, ascending=False)

    {'CoordIndex': {0: 0, 1: 0, 2: 1, 3: 1},

    'Geoname ID': {0: 3620170, 1: 3620163, 2: 584715, 3: 498904},

    'Name': {0: 'Diriamba', 1: 'Dolores', 2: 'Xudat', 3: 'Samur'},

    'ASCII Name': {0: 'Diriamba', 1: 'Dolores', 2: 'Xudat', 3: 'Samur'},

    'Alternate Names': {0: 'Diriamba,Diriambo',

    1: 'Dolores',

    2: 'Khudaf,Khudat,Xudat,Худат',

    3: 'Samur,Самур'},

    'Country Code': {0: 'NI', 1: 'NI', 2: 'AZ', 3: 'RU'},

    'Country name EN': {0: 'Nicaragua',

    1: 'Nicaragua',

    2: 'Azerbaijan',

    3: 'Russian Federation'},

    'Population': {0: 35008, 1: 7065, 2: 13625, 3: 3730},

    'Timezone': {0: 'America/Managua',

    1: 'America/Managua',

    2: 'Asia/Baku',

    3: 'Europe/Moscow'},

    'Modification date': {0: '2018-08-08',

    1: '2018-08-08',

    2: '2014-06-26',
    
    3: '2012-01-17'},

    'LABEL EN': {0: 'Nicaragua',

    1: 'Nicaragua',

    2: 'Azerbaijan',

    ...

    1: '11.85672, -86.21552',

    2: '41.63052, 48.68161',

    3: '41.82527, 48.48597'},

    'Longitude': {0: '-86.23922', 1: '-86.21552', 2: '48.68161', 3: '48.48597'},

    'Latitude': {0: '11.85812', 1: '11.85672', 2: '41.63052', 3: '41.82527'}}
    """
    try:
        flat_list = np.array(coordinates).flatten()
    except ValueError as error:
        print(error)
    else:
        match output:
            case 'dict':
                if len(flat_list) == 2 and k == 1:
                    _, index = tree.query(coordinates, k=k)
                    if ascending != None:
                        return df.iloc[[index]].reset_index(drop=True).sort_values(by='Population', ascending=ascending).to_dict()
                    else:
                        return df.iloc[[index]].reset_index(drop=True).to_dict()
                elif len(flat_list) == 2 and k > 1:
                    _, index = tree.query(coordinates, k=k)
                    return df.iloc[index].reset_index(drop=True).to_dict()
                else:
                    placeData = pd.DataFrame()
                    _, nn = tree.query(coordinates, k=k)
                    if k == 1:
                        temp_Df = pd.DataFrame()
                        for i, index in enumerate(nn):
                            tempDf = df.iloc[[index]].copy(deep=False)
                            tempDf.insert(loc=0, column='CoordIndex', value=i)
                            if ascending != None:
                                temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population', ascending=ascending)
                            else:
                                temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population')
                        placeData = pd.concat([placeData, temp_Df])
                    else:
                        for i, indexes in enumerate(nn):
                            temp_Df = pd.DataFrame()
                            for index in indexes:
                                tempDf = df.iloc[[index]].copy(deep=False)
                                tempDf.insert(loc=0, column='CoordIndex', value=i)
                                if ascending != None:
                                    temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population', ascending=ascending)
                                else:
                                    temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population')
                            placeData = pd.concat([placeData, temp_Df])
                    placeData.reset_index(drop=True, inplace=True)
                    return placeData.to_dict()
            case 'df':
                if len(flat_list) == 2 and k == 1:
                    _, index = tree.query(coordinates, k=k)
                    if ascending != None:
                        return df.iloc[[index]].reset_index(drop=True).sort_values(by='Population', ascending=ascending)
                    else:
                        return df.iloc[[index]].reset_index(drop=True)
                elif len(flat_list) == 2 and k > 1:
                    _, index = tree.query(coordinates, k=k)
                    return df.iloc[index].reset_index(drop=True)
                else:
                    placeData = pd.DataFrame()
                    _, nn = tree.query(coordinates, k=k)
                    if k == 1:
                        temp_Df = pd.DataFrame()
                        for i, index in enumerate(nn):
                            tempDf = df.iloc[[index]].copy(deep=False)
                            tempDf.insert(loc=0, column='CoordIndex', value=i)
                            if ascending != None:
                                temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population', ascending=ascending)
                            else:
                                temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population')
                        placeData = pd.concat([placeData, temp_Df])
                    else:
                        for i, indexes in enumerate(nn):
                            temp_Df = pd.DataFrame()
                            for index in indexes:
                                tempDf = df.iloc[[index]].copy(deep=False)
                                tempDf.insert(loc=0, column='CoordIndex', value=i)
                                if ascending != None:
                                    temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population', ascending=ascending)
                                else:
                                    temp_Df = pd.concat([temp_Df, tempDf]).sort_values(by='Population')
                            placeData = pd.concat([placeData, temp_Df])
                    placeData.reset_index(drop=True, inplace=True)
                    return placeData
            # If an exact match is not confirmed, this last case will be used if provided
            case _:
                raise Exception("output parameter has to be of type string and either 'df' for pandas DataFrame or 'dict' for a dictionary.")