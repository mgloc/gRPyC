from setuptools import setup,find_packages

setup(
    name="grpyc",
    version='0.1',
    license='MIT',
    author="gloxounet",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Gloxounet/gRPyC',
    keywords='gRPC framework',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        grpyc=cli:cli
    ''',
)