# GeoNames - Find City Name with Population > 1000

[Opendatasoft](https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en&sort=name) has as a dataset from [GeoNames](https://www.geonames.org/about.html) which contains all cities with a population greater than a thousand people. This dataset will be used to create a reverse geocode function, called `search`. This project has been inspired by Richard Penman's [reverse-geocode](https://pypi.org/project/reverse-geocode/) project. Like Richard Penman's approach, I too am using a [k-d tree](https://en.wikipedia.org/wiki/K-d_tree) which is implemented using the [SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html) library.

This package will take a latitude and longitude coordinate which will return the country, city name, alternate name(s), population, timezone, and exact coordinates of the city. 

## Dependencies
  * Python 3.11.4
  * Pandas 2.0.3
  * SciPy 1.11.1

## Example usage:

This package only has one function `search` and it has a single parameter `coordinate`.

Enter latitude and longitude into the `search` function, as a list, to get your results.

    >>> import geonames
    >>> geonames.search([11.85812, -86.23922])

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

One can also enter a list of multiple latitudes and longitudes into the `search` function to get your results.

    >>> geonames.search([[11.85812, -86.23922],[12.4825, -87.17304]])

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

## Install

    pip install pygeocity
    pip3 install pygeocity

And make sure you install version 0.1.2

Use:

    pip install pygeocity==0.1.2