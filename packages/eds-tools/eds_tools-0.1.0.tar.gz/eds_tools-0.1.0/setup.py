from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
   name='eds_tools',
   version='0.1.0',
   python_requires='>=3.9.10', 
   description='EDSTools: designed to combined variant calls from peaked data with the reference genome. Returns the genomic sequence of the allele most present in the peak.',
   long_description=long_description,
   long_description_content_type="text/markdown",
   project_urls={
       "Bug Tracker": "https://github.com/Genome-Function-Initiative-Oxford/EdTools/issues",
       "Source": "https://github.com/Genome-Function-Initiative-Oxford/EdTools"},
   author='Simone G. Riva, Edward Sanders',
   author_email='simo.riva15@gmail.com',
   packages=['eds_tools'],  
   install_requires = [
      "pysam"
   ]
)