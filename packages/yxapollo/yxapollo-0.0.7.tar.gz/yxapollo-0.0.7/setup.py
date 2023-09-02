import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yxapollo",
    version="0.0.7",
    author="Yanxuan",
    author_email="zhuxulv@corp.netease.com",
    description="python apollo connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://you.163.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)