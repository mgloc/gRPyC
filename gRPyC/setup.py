from setuptools import setup,find_packages


from pip._internal.req import parse_requirements

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

#Actual setup
setup(
    name="grpyc",
    version='0.1.2',
    description='Framework for grpcio (gRPC for python)',
    long_description="To ease compilation, project structure and tests",
    long_description_content_type='text/plain',
    license='MIT',
    author="gloxounet",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Gloxounet/gRPyC',
    keywords='gRPC framework',
    py_modules=['cli','compilation'],
    install_requires=['grpcio-tools>=1.49.1','Click'],
    python_requires='>=3',
    entry_points='''
        [console_scripts]
        grpyc=cli:cli
    ''',
)