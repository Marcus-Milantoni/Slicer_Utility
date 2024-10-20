from setuptools import find_packages, setup

VERSION = "0.1.4"
with open(r"README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="slicerutil",
    version="0.2.2",
    description="A package created for ease of use working with NumPy in 3D Slicer",
    packages = find_packages(),
    include_package_data=True,  # This ensures that package_data is included
    package_data={
        'slicerutil': ['assets/*.png', 'assets/*.jpeg'],  # Include image files
    },
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
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "matplotlib"], 
    keywords=["3D slicer", "Utility", "Image Processing", "NumPy"]
)

