from setuptools import setup, find_packages

setup(
    name='genetic-optimization',
    version='0.1',
    description='Genetic Optimization package',
    long_description="A genetic optimization package for hyperparameter tuning.",
    python_requires='>= 3.7',
    author='Gaurav Srivastava',
    author_email='gauravhhh30@gmail.com',
    url='https://github.com/ctrl-gaurav/genetic-optimization',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'lightgbm',
        'xgboost',
        'scikit-learn',
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
