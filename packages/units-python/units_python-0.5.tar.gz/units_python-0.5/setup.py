from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'units_python',
  packages = ['units_python'], 
  version = '0.5',      # Update with new release
  license='MIT',
  description = 'Package for automatically managing units when doing calculations in python.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Lucas Vilsen',          
  author_email = 'lucas.vilsen@gmail.com',    
  url = 'https://github.com/Apros7/python-units',
  download_url = 'https://github.com/Apros7/python-units/archive/refs/tags/v0.5.0.tar.gz', # update with new release
  keywords = ['units', 'physics', 'math'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta", "5 - Production/Stable"
    'Intended Audience :: Developers', 
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
  ],
)

# For updating package run:
# python3 setup.py sdist
# twine upload dist/*