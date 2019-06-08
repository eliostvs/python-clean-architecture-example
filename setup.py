import setuptools

REQUIRED = ["click==6.7", "marshmallow==2.15.4"]

setuptools.setup(
    name="example-customer-find-system",
    version="0.1.0",
    author="Elio Esteves Duarte",
    author_email="elio.esteves.duarte@gmail.com",
    description="Example Python Clean Architecture",
    long_description=open("README.md").read(),
    packages=setuptools.find_packages(),
    install_requires=REQUIRED,
    entry_points={"console_scripts": ["find-customers=example.cli.controller:run"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
