﻿import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'mynameischarkkich',      
  packages = ['mynameischarkkich'], 
  version = '0.0.2', 
  license='MIT', 
  description = 'Who is Charkkich',
  long_description=DESCRIPTION,
  author = 'Charkkich',                 
  author_email = 'test@gmail.com',     
  url = 'https://github.com/charkkich/mynameischarkkich',  
  download_url = 'https://github.com/charkkich/mynameischarkkich',  
  keywords = ['charkkich', 'ASCII ART'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)