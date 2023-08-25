# GeoNames - Find City Name with a Population > 1000

[Opendatasoft](https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en&sort=name) has as a dataset from [GeoNames](https://www.geonames.org/about.html) which contains all cities with a population greater than a thousand people. This dataset will be used to create a reverse geocode function, called `search`. This project has been inspired by Richard Penman's [reverse-geocode](https://pypi.org/project/reverse-geocode/) project. Like Richard Penman's approach, I am also using a [k-d tree](https://en.wikipedia.org/wiki/K-d_tree) which is implemented using the [SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html) library.

This package will take a latitude and longitude coordinate which will return the country, city name, alternate name(s), population, timezone, and exact coordinates for that city. 

## Dependencies
  * Python 3.11.4
  * Numpy 1.25.0
  * Pandas 2.0.3
  * SciPy 1.11.1

## Install

    pip install pygeocity

Make sure you install version 0.2.0

Use:

    pip install pygeocity==0.2.0

## Example usage:

This package only has one function `search` and it has a three parameters: 
- `coordinate` Required - list or list(list)
  - Search query allows a list of Latitude and Longitude, or a single pair which must be passed as list. It will return name of the nearest city in the same order which the coordinates were passed
    
    Example:
    - single location: coordinates = [11.86, -86.24]
    - multiple locations: coordinates = [[11.86, -86.24], [42, 49]]
    
- `k`: Optional - int > 1, Default: int = 1
    - Number of of nearest neighbours to find for each set of coordinates. Must be a value greater than zero.
    
- `output`: Optional - 'df' or 'dict', default: output = 'df'
    - Which format to return to users. Either pandas DataFrame or dictionary.
    
- `ascending`: Optional - True or False, default: None
  - If the format should be sorted by ascending, descending population, or no sorting at all. This can help in finding the nearest city with the largest population (might need to increase k).

### Code Examples

- Enter latitude and longitude into the `search` function, as a list, to get your results.

```python
>>> import geonames
>>> geonames.search([11.85812, -86.23922], output='dict')

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
```



- One can also enter a list of multiple latitudes and longitudes into the `search` function to get your results.

```python
>>> geonames.search([[11.85812, -86.23922],[12.4825, -87.17304]], output='dict')

Outputs:
{'CoordIndex': {0: 1, 1: 0},
 'Geoname ID': {0: 3620269, 1: 3620170},
 'Name': {0: 'Corinto', 1: 'Diriamba'},
 'ASCII Name': {0: 'Corinto', 1: 'Diriamba'},
 'Alternate Names': {0: 'Corinto', 1: 'Diriamba,Diriambo'},
 'Country Code': {0: 'NI', 1: 'NI'},
 'Country name EN': {0: 'Nicaragua', 1: 'Nicaragua'},
 'Population': {0: 19183, 1: 35008},
 'Timezone': {0: 'America/Managua', 1: 'America/Managua'},
 'Modification date': {0: '2018-08-08', 1: '2018-08-08'},
 'LABEL EN': {0: 'Nicaragua', 1: 'Nicaragua'},
 'Coordinates': {0: '12.4825, -87.17304', 1: '11.85812, -86.23922'},
 'Longitude': {0: '-87.17304', 1: '-86.23922'},
 'Latitude': {0: '12.4825', 1: '11.85812'}}
```

- You can also search for more than one nearest neighbour for each Latitude & Longitude pair entered. Here we search for two nearest neighbours.

```python
>>> geonames.search([[11.85812, -86.23922],[12.4825, -87.17304]], output='dict', k=2)

Outputs:
{'CoordIndex': {0: 0, 1: 0, 2: 1, 3: 1},
 'Geoname ID': {0: 3620163, 1: 3620170, 2: 3619451, 3: 3620269},
 'Name': {0: 'Dolores', 1: 'Diriamba', 2: 'El Realejo', 3: 'Corinto'},
 'ASCII Name': {0: 'Dolores', 1: 'Diriamba', 2: 'El Realejo', 3: 'Corinto'},
 'Alternate Names': {0: 'Dolores',
  1: 'Diriamba,Diriambo',
  2: 'El Realejo,Realejo',
  3: 'Corinto'},
 'Country Code': {0: 'NI', 1: 'NI', 2: 'NI', 3: 'NI'},
 'Country name EN': {0: 'Nicaragua',
  1: 'Nicaragua',
  2: 'Nicaragua',
  3: 'Nicaragua'},
 'Population': {0: 7065, 1: 35008, 2: 6208, 3: 19183},
 'Timezone': {0: 'America/Managua',
  1: 'America/Managua',
  2: 'America/Managua',
  3: 'America/Managua'},
 'Modification date': {0: '2018-08-08',
  1: '2018-08-08',
  2: '2018-08-08',
  3: '2018-08-08'},
 'LABEL EN': {0: 'Nicaragua', 1: 'Nicaragua', 2: 'Nicaragua', 3: 'Nicaragua'},
 'Coordinates': {0: '11.85672, -86.21552',
  1: '11.85812, -86.23922',
  2: '12.54333, -87.16517',
  3: '12.4825, -87.17304'},
 'Longitude': {0: '-86.21552', 1: '-86.23922', 2: '-87.16517', 3: '-87.17304'},
 'Latitude': {0: '11.85672', 1: '11.85812', 2: '12.54333', 3: '12.4825'}}
```

- You can also search for more than one nearest neighbour for each Latitude & Longitude pair entered. Here we search for two nearest neighbours, and sort by the cities population in descending order.

```python
>>> geonames.search([[11.85812, -86.23922],[12.4825, -87.17304]], output='dict', k=2, ascending=False)

Outputs:
{'CoordIndex': {0: 0, 1: 0, 2: 1, 3: 1},
 'Geoname ID': {0: 3620170, 1: 3620163, 2: 3620269, 3: 3619451},
 'Name': {0: 'Diriamba', 1: 'Dolores', 2: 'Corinto', 3: 'El Realejo'},
 'ASCII Name': {0: 'Diriamba', 1: 'Dolores', 2: 'Corinto', 3: 'El Realejo'},
 'Alternate Names': {0: 'Diriamba,Diriambo',
  1: 'Dolores',
  2: 'Corinto',
  3: 'El Realejo,Realejo'},
 'Country Code': {0: 'NI', 1: 'NI', 2: 'NI', 3: 'NI'},
 'Country name EN': {0: 'Nicaragua',
  1: 'Nicaragua',
  2: 'Nicaragua',
  3: 'Nicaragua'},
 'Population': {0: 35008, 1: 7065, 2: 19183, 3: 6208},
 'Timezone': {0: 'America/Managua',
  1: 'America/Managua',
  2: 'America/Managua',
  3: 'America/Managua'},
 'Modification date': {0: '2018-08-08',
  1: '2018-08-08',
  2: '2018-08-08',
  3: '2018-08-08'},
 'LABEL EN': {0: 'Nicaragua', 1: 'Nicaragua', 2: 'Nicaragua', 3: 'Nicaragua'},
 'Coordinates': {0: '11.85812, -86.23922',
  1: '11.85672, -86.21552',
  2: '12.4825, -87.17304',
  3: '12.54333, -87.16517'},
 'Longitude': {0: '-86.23922', 1: '-86.21552', 2: '-87.17304', 3: '-87.16517'},
 'Latitude': {0: '11.85812', 1: '11.85672', 2: '12.4825', 3: '12.54333'}}
```