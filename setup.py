from distutils.core import setup

setup(
    name='house',
    version='',
    packages=['house'],
    scripts=['bin/house_web'],
    data_files=[('house/config', ['house.json'])],
    url='http://home.homb.it',
    license='',
    author='Konstantin Malanchev',
    author_email='hombit@gmail.com',
    description=''
)
