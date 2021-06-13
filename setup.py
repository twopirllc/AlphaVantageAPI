from setuptools import setup

long_description = "An Opinionated AlphaVantage API Wrapper in Python 3.9 and compatible with Pandas TA"

setup(
    name="alphaVantage_api",
    version="1.0.33",
    description=long_description,
    long_description=long_description,
    author="Kevin Johnson",
    author_email="appliedmathkj@gmail.com",
    keywords="AlphaVantage, API, Equities, FOREX, Digital/Crypto, Technical Analysis, Technicals, Fundamentals, Earnings Calendar, IPO Calendar, Listing Status",
    url="https://github.com/twopirllc/AlphaVantageAPI",
    license="MIT",
    packages=["alphaVantageAPI"],
    install_requires=["requests", "pandas"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Utilities",
    ],
    extras_requires={
        "openpyxl": ["openpyxl"],
    },
    package_data={
        "alphaVantageAPI":["data/api.json"],
    },
    zip_safe=False
)