from cx_Freeze import setup, Executable

executables = [Executable('MainWindow.py', targetName='Comparator.exe')]

excludes = ['unicodedata', 'logging', 'unittest', 'email', 'html', 'http', 'urllib',
            'xml', 'pydoc', 'doctest', 'argparse', 'datetime', 'zipfile',
            'subprocess', 'pickle', 'threading', 'locale', 'calendar', 'functools',
            'weakref', 'tokenize', 'base64', 'gettext', 'heapq', 're', 'operator',
            'bz2', 'fnmatch', 'getopt', 'reprlib', 'string', 'stringprep',
            'contextlib', 'quopri', 'copy', 'imp', 'keyword', 'linecache']

zip_include_packages = ['collections', 'encodings', 'importlib',]

options = {
    'build_exe': {
        'include_msvcr': True,
        # 'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
    }
}

setup(name='Comparator',
      version='3.0.1',
      description='',
      executables=executables,
      options=options)