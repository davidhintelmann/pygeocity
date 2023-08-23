from distutils.core import setup

setup(
    name='pygeocity',
    version='0.1.1',
    packages=['pygeocity','pygeocity.geonames'],
    package_dir={'pygeocity': '.'},  # look for package contents in current directory
    package_data={'pygeocity': ['geonames/geonames.csv']}, #package_data={"": ['geonames/geonames.csv']},
    include_package_data=True,
    author='David Hintelmann',
    author_email='davidhin@mac.com',
    description='Reverse geocode with the given longitude and latitude',
    long_description='README.md',
    url='https://github.com/davidhintelmann/pygeocity',
    license='MIT',
    install_requires=['pandas', 'scipy']
)