import sys
from cx_Freeze import setup, Executable

import os.path
import matplotlib
import numpy
import tkinter
import pandas 
import selenium


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')



buildOptions = dict(
        packages = ["os","sys","time","bs4",'tkinter',"numpy","pandas","selenium"],
        includes = ['numpy.core._methods',"matplotlib.backends.backend_tkagg",
                    "matplotlib.pyplot","tkinter.filedialog","numpy","selenium"],
#        excludes = ['tkinter',"html"],
        zip_include_packages=['*'],
        zip_exclude_packages=['numpy', 'numpy.core._methods'],
        include_msvcr=True,
        include_files = [
                matplotlib.get_data_path(),
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'sqlite3.dll')
                ]
            )

base = None

DLLS_FOLDER = os.path.join(PYTHON_INSTALL_DIR, 'Library', 'bin')

dependencies = ['libiomp5md.dll', 'mkl_core.dll', 'mkl_def.dll', 'mkl_intel_thread.dll']


executables = [Executable('crawler.py', base=base)]


setup(name = 'HSH',
      version = '0.1',
      description = 'Naver Band',
      options = dict(build_exe = buildOptions),
      executables = executables
      )


