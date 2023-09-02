from setuptools import setup
setup(    
    name = 'fourZoneVehicleCab',     
    version = '0.1.0.3',    
    description = 'A zonal vehicle cabin climate model to estimate temperature, CO2 and humidity transport.',       
    py_modules = ["fourZoneVehicleCab"],    
    package_dir = {'':'src'},
    author = 'Anandh Ramesh Babu',
    author_email = 'anandh.rameshbabu@chalmers.se',        
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type = "text/markdown",    
    url='https://github.com/anandhSRB/fourZoneVehicleCab',    
    include_package_data=True,    
    classifiers  = [
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
    ],    
    install_requires = [

        'pandas',
		'numpy',		
		'jos3',		

    ],        
    keywords = ['Zonal cabin climate model', 'vehicle cabin thermal model'],
    
)
