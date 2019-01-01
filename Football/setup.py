# https://docs.python.org/3/distutils/setupscript.html

from distutils.core import setup

setup(name='Football',
      version='1.0',
      description='Football example',
      author='Martin Stan',
      author_email='...',
      url='...',
      packages=['flask', 
                'flask_bootstrap', 
                'requests', 
                'bs4', 
                'pandas', 
                'numpy', 
                'scipy', 
                'matplotlib'],
     )