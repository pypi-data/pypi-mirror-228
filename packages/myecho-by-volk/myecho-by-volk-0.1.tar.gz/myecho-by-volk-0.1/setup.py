from setuptools import setup, find_packages

setup(
    name="myecho-by-volk",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'myecho = my_custom_package.myecho:main',
        ],
    },
    install_requires=[
        # Your package dependencies
    ],
)