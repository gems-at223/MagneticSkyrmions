from setuptools import setup, find_packages

setup(
    name="mcsim",  # Package name must be mcsim.
    version="1.0.0",  # Extend setup.py file as required.
    packages=find_packages(),
    description='A package to simulate spin states using Metropolis Monte Carlo',
    author="gems-at223",
    install_requires=["numpy>=1.25.2",
                      "matplotlib>=3.7.2",
                      "pytest>=7.4.2"
                      ]
)
