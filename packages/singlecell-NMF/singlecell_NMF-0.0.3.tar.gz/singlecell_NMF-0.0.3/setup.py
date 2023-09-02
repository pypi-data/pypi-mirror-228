import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="singlecell_NMF",
    version="0.0.3",
    author="Wangchen",
    author_email="wch_bioinformatics@163.com",
    description="NMF for single cell dataset  .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangzichenbioinformatics/singlecell-NMF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
