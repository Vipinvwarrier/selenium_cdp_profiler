from setuptools import setup, find_packages

setup(
    name="selenium_cdp_profiler",
    version="0.1.0",
    author="Vipin",
    author_email="vipinvwarrier@gmail.com",
    description="Chrome CDP integration for selenium",
    long_description="Repo provides a reporting of all the network activities and console errors occurred during the execution",
    packages=find_packages(),
    package_data={
        "selenium_cdp_profiler": ["**/*.py"],
    },
    install_requires=[
        "pandas",
        "sqlalchemy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
