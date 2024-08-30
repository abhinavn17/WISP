from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='WISP',  
    version='0.1.0',  
    author='Abhinav Narayan',
    description='WSCLEAN Imaging and Selfcal Pipeline for GMRT and uGMRT data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),    
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'wisp = WISP.__main__:main',
            'make_ini = WISP.make_ini:main'
        ]
    },
    include_package_data=True
)