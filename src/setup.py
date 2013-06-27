from distutils.core import setup
import py2exe

import os
import sys; sys.argv.append('py2exe')

#http://www.py2exe.org/index.cgi/ListOfOptions

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/reverseastar')

py2exe_options = dict(
                      ascii=True,  # Exclude encodings
                      excludes=['_ssl', 'pdb', 'unittest', 'inspect',
                                'pyreadline', 'difflib', 'doctest', 'locale', 'optparse', 'pickle', 
                                'calendar',  '_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 
                                'pywin.debugger','pywin.debugger.dbgcon', 'pywin.dialogs', 
                                'tcl','Tkconstants', 'Tkinter'],                      
                      dll_excludes=['msvcr71.dll', 'libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                                'tk84.dll'],
                      compressed=True,
                      includes=['gui', 'model', 'algorithm'],
                      bundle_files=1,
                      #build = {'build_base': '../build'},
                      dist_dir='../dist'
                      )

setup(name='ReverseAStar',
      version='1.0',
      description='Class project for UAV 803',

      zipfile = None,

      console=['reverseastar/reverseastar.py'],
      options={'py2exe': py2exe_options},
      )
