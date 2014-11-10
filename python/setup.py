from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='context',
    version='0.0',
    description='A Python API for the Context profiler',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Shish',
    author_email='shish+context@shishnet.org',
    url='http://code.shishnet.org/context',
    keywords='profile',
    packages=["context"],
    namespace_packages=["context"],
    test_suite="context.tests",
    zip_safe=True,
    install_requires=[
        "decorator",
    ],
)

