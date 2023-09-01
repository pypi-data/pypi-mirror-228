import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pelatihan-bmkg",
    version = "0.0.2",
    author = "ummu",
    author_email = "author@example.com",
    description = "aplikasi pertama",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/ummumf/pelatihan_bmkg",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.9",
    install_requires = [
       ]
)