from setuptools import setup, find_packages

setup(
    name='deseqpyodide',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        "anndata>=0.8.0",
        "numpy>=1.23.0",
        "pandas>=1.4.0",
        "scikit-learn>=1.1.0",
        "scipy>=1.8.0",
        "statsmodels",
        "matplotlib>=3.6.2",
    ]
)