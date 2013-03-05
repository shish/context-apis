from setuptools import setup, find_packages

setup(
    name='context.api',
    version='0.0',
    description='A Python API for the Context profiler',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Shish',
    author_email='shish+context@shishnet.org',
    url='http://code.shishnet.org/context',
    keywords='profile',
    packages=["context"],
    namespace_packages=["context"],
    test_suite = "context.tests.api",
    zip_safe=True,
    install_requires=[
        "decorator",
    ],
)

