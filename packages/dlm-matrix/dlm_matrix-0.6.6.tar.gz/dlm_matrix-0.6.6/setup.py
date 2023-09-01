from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dlm_matrix",
    version="0.6.6",
    author="Mohamed Diomande",
    author_email="gdiomande7907@gmail.com",
    description="Divergent Language Matrix",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/diomandeee/dl_matrix",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.6",
    install_requires=requirements,
)
