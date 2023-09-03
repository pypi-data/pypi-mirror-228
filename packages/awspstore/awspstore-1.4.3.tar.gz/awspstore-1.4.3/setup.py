import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="awspstore",
    version="1.4.3",
    author="Eldad Bishari",
    author_email="eldad@1221tlv.org",
    description="Vault for your software project using AWS Parameter Store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eldad1221/aws-vault",
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3>=1.26.3',
        'quickbelog>=1.1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
