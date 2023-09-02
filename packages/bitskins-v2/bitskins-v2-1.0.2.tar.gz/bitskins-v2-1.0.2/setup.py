from setuptools import setup

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name="bitskins-v2",
    version="1.0.2",
    description="An unofficial wrapper for the Bitskins V2 API in Python.",
    long_description=long_desc,
    long_description_content_type="text/x-rst",
    url="https://github.com/kasperlindau/bitskins-v2-wrapper",
    packages=["bitskins"],
    keywords="bitskins v2 api rest websockets"
)
