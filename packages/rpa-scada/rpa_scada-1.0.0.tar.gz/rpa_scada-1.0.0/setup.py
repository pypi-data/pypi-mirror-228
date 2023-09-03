from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rpa_scada",
    version="1.0.0",
    packages=find_packages(),
    author="Daniel Taiba",
    author_email="danielt.dtr@gmail.com",
    description="Scraper of SCADAs without browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Scraper SCADA',
    url='https://github.com/oym-tritec/rpa_scada',
    install_requires=[
        "numpy==1.25.2",
        "pandas==2.1.0",
        "requests==2.31.0",
        "python-dotenv==1.0.0"
    ],
)
