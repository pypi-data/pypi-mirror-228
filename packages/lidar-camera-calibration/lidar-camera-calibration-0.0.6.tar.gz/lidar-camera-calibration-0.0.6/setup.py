from setuptools import find_packages, setup

VERSION = "0.0.6"
DESCRIPTION = "LiDAR camera calibration"
LONG_DESCRIPTION = "A PyTorch LiDAR camera calibration project that maximises the mutual information between LiDAR and image intensities."

# Setting up
setup(
    # the name must match the folder name 'image_based_malware_dataloader'
    name="lidar-camera-calibration",
    version=VERSION,
    author="Timothy Farnworth",
    author_email="tkfarnworth@gmail.com",
    description=DESCRIPTION,
    url="https://github.com/kiakahabro/lidar-camera-calibration",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "pathlib2",
        "pyqt5",
        "pyyaml",
        "scikit-learn",
        "scipy",
        "torch",
    ],
    keywords=["python", "calibration", "LiDAR", "camera"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
