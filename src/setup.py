from distutils.core import setup
import py2exe

import os
import sys; sys.argv.append('py2exe')

#http://www.py2exe.org/index.cgi/ListOfOptions

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/reverseastar')

py2exe_options = dict(
                      #optimize=2,
                      ascii=True,  # Exclude encodings
                      excludes=['_ssl', 'pdb', 'unittest', 'inspect',
                                'pyreadline', 'difflib', 'doctest', 'locale', 
                                'optparse', 'pickle', 'calendar'],
                      dll_excludes=['msvcr71.dll'],
                      #compressed=True,  # Compress library.zip
                      #includes=['reverseastar/algorithm', 'reverseastar/gui'],
                      includes=['gui', 'model', 'algorithm'],
                      #bundle_files = 2, # This tells py2exe to bundle everything
                      #build = {'build_base': '../build'},
                      dist_dir='../dist'
                      )

setup(name='ReverseAStar',
      version='1.0',
      description='Class project for UAV 803',
      author='Charles Tullock',

      console=['reverseastar/reverseastar.py'],
      options={'py2exe': py2exe_options},
      )
