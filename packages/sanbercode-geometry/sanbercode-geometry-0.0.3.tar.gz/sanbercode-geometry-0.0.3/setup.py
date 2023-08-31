import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "sanbercode-geometry",
    version = "0.0.3",
    author = "putuhendrawd",
    author_email = "putuhendrawd@gmail.com",
    description = "geometry package tugas sanbercode",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/putuhendrawd/sanbercode_geometry",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.9",
    install_requires = [ 
        "numpy>=1.21",
        "matplotlib>=3.7.2"      
      ]
)