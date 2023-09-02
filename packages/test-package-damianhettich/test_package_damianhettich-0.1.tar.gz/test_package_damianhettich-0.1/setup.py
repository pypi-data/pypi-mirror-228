from setuptools import setup, find_packages

setup(
    name='test_package_damianhettich',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "pandas==2.1.0"
    ],
)