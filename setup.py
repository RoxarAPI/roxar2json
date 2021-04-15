import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="roxar2json",
    version="0.0.1",
    author="Havard Bjerke",
    author_email="havard.bjerke@emerson.com",
    description="Roxar project Json encoding.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RoxarAPI/roxar2json",
    project_urls={
        "Bug Tracker": "https://github.com/RoxarAPI/roxar2json/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    packages=["roxar2json"],
    python_requires=">=3.7",
)
