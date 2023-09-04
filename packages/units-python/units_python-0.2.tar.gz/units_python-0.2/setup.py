from distutils.core import setup

setup(
  name = 'units_python',
  packages = ['units_python'], 
  version = '0.2',      # Update with new release
  license='MIT',
  description = 'Package for automatically managing units when doing calculations in python.',
  author = 'Lucas Vilsen',          
  author_email = 'lucas.vilsen@gmail.com',    
  url = 'https://github.com/Apros7/python-units',
  download_url = 'https://github.com/Apros7/python-units/archive/refs/tags/v0.2.0.tar.gz', # update with new release
  keywords = ['units', 'physics', 'math'],
#   install_requires=[],
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
# python setup.py sdist
# twine upload dist/*