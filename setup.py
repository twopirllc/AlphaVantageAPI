from setuptools import setup, find_packages

long_description = 'An Opinionated AlphaVantage API Wrapper in Python 3.7'

setup(
    name='alphaVantage_api',
    version='1.0.10',
    description=long_description,
    long_description=long_description,
    author='Kevin Johnson',
    author_email='appliedmathkj@gmail.com',
    keywords='AlphaVantage, API, Equities, FOREX, Digital/Crypto, TA, Technicals, Sectors',
    url='https://github.com/twopirllc/AlphaVantageAPI',
    license='MIT',
    packages=['alphaVantageAPI'],
    install_requires=['requests', 'pandas'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Utilities',
    ],
    extras_requires={
        'openpyxl': ['openpyxl'],
    },
    package_data={
        'alphaVantageAPI': {'alphaVantageAPI':['data/api.json','data/treasury_curves.csv']},
    },
    zip_safe=False
)