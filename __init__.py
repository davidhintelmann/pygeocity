import pandas as pd
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
def search(coordinates:[float,float]) -> pd.DataFrame:
    """
    Function will search geonames data for closest city for the inputted Longitude and Latitude

    PARAMETERS
    ----------
    coordinates: (Required) Search query allows a list of Latitude and Longitude, or a single pair which must be passed as list. It will return name of the nearest city in the same order which the coordinates were passed.
    
    RETURNS
    ----------
    Dictionary{Dictionary}: Key:Value{Dictionary} - info
        'Geoname ID':
        'Name': - (City Name)
        'ASCII Name': - (City Name in ASCII)
        'Alternate Names': - (Alternate names for the city, or a list of alternate names)
        'Country Code':
        'Country name EN':
        'Population':
        'Timezone':
        'Modification date': - (Date this data point was updated)
        'LABEL EN':
        'Coordinates':
        'Longitude':
        'Latitude':

    EXAMPLES
    ----------
    >>> import pygeocity
    >>> pygeocity.search([11.85812, -86.23922])

    Outputs:
        {
            0: 3620170,
            1: 'Diriamba',
            2: 'Diriamba',
            3: 'Diriamba,Diriambo',
            4: 'NI',
            5: 'Nicaragua',
            6: 35008,
            7: 'America/Managua',
            8: '2018-08-08',
            9: 'Nicaragua',
            10: '11.85812, -86.23922',
            11: ' -86.23922',
            12: '11.85812'
        }

    >>> pygeocity.search([11.85812, -86.23922],[12.4825, -87.17304])

    Outputs:
        {
            'Geoname ID': {0: 3620170, 1: 3620269},
            'Name': {0: 'Diriamba', 1: 'Corinto'},
            'ASCII Name': {0: 'Diriamba', 1: 'Corinto'},
            'Alternate Names': {0: 'Diriamba,Diriambo', 1: 'Corinto'},
            'Country Code': {0: 'NI', 1: 'NI'},
            'Country name EN': {0: 'Nicaragua', 1: 'Nicaragua'},
            'Population': {0: 35008, 1: 19183},
            'Timezone': {0: 'America/Managua', 1: 'America/Managua'},
            'Modification date': {0: '2018-08-08', 1: '2018-08-08'},
            'LABEL EN': {0: 'Nicaragua', 1: 'Nicaragua'},
            'Coordinates': {0: '11.85812, -86.23922', 1: '12.4825, -87.17304'},
            'Longitude': {0: ' -86.23922', 1: ' -87.17304'},
            'Latitude': {0: '11.85812', 1: '12.4825'}
        }
    """
    _, index = tree.query(coordinates, k=1)
    return df.iloc[index].reset_index(drop=True).to_dict()