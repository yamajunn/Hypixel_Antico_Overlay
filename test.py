from cx_Freeze import setup, Executable

setup(name='Anti Cockroach',
      version='0.1',
      description='Anti Cockroach. ver 0.1',
      executables=[Executable('./overlay.py')])