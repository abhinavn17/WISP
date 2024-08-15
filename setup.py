from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='uCAPTURE',  
    version='0.1.0',  
    author='Abhinav Narayan',
    description='Imaging/selfcal pipeline for GMRT and uGMRT data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),    
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ucapture = uCAPTURE.capture:main',
            'make_config = uCAPTURE.make_config:main'
        ]
    },
    include_package_data=True
)