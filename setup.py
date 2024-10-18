from setuptools import find_packages, setup

with open(r"app\Readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="slicerutil",
    version="0.1.1",
    description="A package created for ease of use working with NumPy in 3D Slicer",
    package_dir={"": "app"},
    packages = find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marcus-Milantoni/Slicer_Utility",
    author="Marcus Milantoni",
    author_email="mmilanto@uwo.ca", 
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "matplotlib"]
)