import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "rh_calculator",
    version = "0.0.1",
    author = "Ratna",
    author_email = "ratnasat@gmail.com",
    description = "relative humidity calculator",
    long_description = "README.md",
    long_description_content_type = "text",
    url= "https://github.com/ratnasatya/training_bmkg/",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.8",
    install_requires = [
        #   "matplotlib",
          "requests",
      ]
)