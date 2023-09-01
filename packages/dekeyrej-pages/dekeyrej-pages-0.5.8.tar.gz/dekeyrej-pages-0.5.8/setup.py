from setuptools import find_packages, setup

setup(
    name='pages',
    packages=find_packages(include=['pages']),
    version='0.5.8',
    description='Matrix Microservice and Client page superclasses',
    author='J.DeKeyrel',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)