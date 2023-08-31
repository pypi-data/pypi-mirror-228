import setuptools
from setuptools import setup
from glob import glob

setuptools.setup(
    name="hjlc3",
    version="1.2.7",
    author="bug404",
    author_email="z19040042@s.upc.edu.cn",
    description="Some environments for reinforcement learning.",
    long_description="Some environments for reinforcement learning.",
    long_description_content_type="text/markdown",
    include_package_data = True,
    packages=['.'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)