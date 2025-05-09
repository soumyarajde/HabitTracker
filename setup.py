from setuptools import setup, find_packages

setup(
    name="habittracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[], 
    python_requires='>=3.13',
    author="Soumya Raj",
    description="habit tracking app developed for iu python course",
    include_package_data=True,
)
