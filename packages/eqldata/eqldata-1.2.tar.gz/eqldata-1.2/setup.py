from setuptools import setup, find_packages

setup(
    name='eqldata',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        'websockets',
    ],
    description='A Python package for subscribing to instruments data.',
    author='EQLSOLUTION',
    author_email='info@equalsolution.com',
    url='http://equalsolution.com/',
    license='MIT',
)
