import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="json-editor-pyside6",
    version="1.0.3",
    author="Richard Brenick, Eyal Karni",
    author_email="RichardBrenick@gmail.com, eyalk5@gmail.com",
    description="Visual JSON Editor written in Qt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eyalk11/json-editor-pyside6",
    packages=setuptools.find_packages(),
    package_data={'': ['*.*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    install_requires=[
    "PySide6",
    ]
)


