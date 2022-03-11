import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inxt-data-loaders",
    version="0.0.1",
    author="Joan Mora",
    author_email="joanmoragrau@gmail.com",
    description="Internxt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/internxt/inxt-data-loaders",
    project_urls={
        "Bug Tracker": "https://github.com/internxt/inxt-data-loaders/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AFFERO GENERAL :: PUBLIC LICENSE",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
