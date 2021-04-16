import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="remove_dagmc_tags",
    version="0.0.2",
    author="Jonathan Shimwell",
    author_email="mail@jshimwell.com",
    description="A tool for selectively removing tags such as the graveyard from DAGMC h5m files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shimwell/remove_dagmc_tags",
    packages=setuptools.find_packages(),
    zip_safe=True,
    package_dir={"remove_dagmc_tags": "remove_dagmc_tags"},
    scripts=['remove_dagmc_tags/remove-dagmc-tags'],
    package_data={
        "remove_dagmc_tags": [
            "requirements.txt",
            "README.md",
            "LICENSE",
        ]
    },
    tests_require=["pytest-cov"],
    # install_requires=[
    #     # 'pymoab' is is required for this package but is not available via pip install at the moment
    # ],
)
