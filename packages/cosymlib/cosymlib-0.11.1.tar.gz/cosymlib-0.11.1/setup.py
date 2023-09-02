from numpy.distutils.core import setup, Extension
import os


def get_version_number():
    main_ns = {}
    for line in open('cosymlib/__init__.py', 'r').readlines():
        if not(line.find('__version__')):
            exec(line, main_ns)
            return main_ns['__version__']


shape = Extension('cosymlib.shape.shp',
                  extra_f90_compile_args=['-static-libgcc'],
                  #include_dirs=include_dirs_numpy,
                  sources=['fortran/shp.pyf', 'fortran/shp.f90'])

on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    ext_modules = []
else:
    ext_modules = [shape]

setup(name='cosymlib',
      version=get_version_number(),
      description='Continuous measures of shape and symmetry',
      author='Efrem Bernuz',
      author_email='komuisan@gmail.com',
      packages=['cosymlib',
                'cosymlib.shape',
                'cosymlib.molecule',
                'cosymlib.molecule.geometry',
                'cosymlib.molecule.electronic_structure',
                'cosymlib.file_io',
                'cosymlib.symmetry',
                'cosymlib.tools',
                'cosymlib.simulation',
                'cosymlib.gui'],
      package_data={'': ['ideal_structures_center.yaml',
                         'periodic_table.yaml']},
      include_package_data=True,
      install_requires=['numpy', 'matplotlib', 'symgroupy', 'wfnsympy', 'PyYAML', 'huckelpy', 'pointgroup'],
      scripts=['scripts/cosym',
               'scripts/shape',
               'scripts/gsym',
               'scripts/cchir',
               'scripts/esym',
               'scripts/mosym',
               'scripts/shape_map',
               'scripts/shape_classic'],
      ext_modules=ext_modules,
      url='https://github.com/GrupEstructuraElectronicaSimetria/cosymlib',
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License"]
      )
