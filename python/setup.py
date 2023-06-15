from setuptools import setup
from content_apis.version import VERSION

setup(
    name="kadalu_content_apis",
    version=VERSION,
    packages=["kadalu_content_apis"],
    install_requires=['urllib3'],
    author="Kadalu Technologies Private Limited",
    author_email="packages@kadalu.tech",
    description="",
    license="GPL-v3",
    keywords="content apis",
    url="https://github.com/kadalu-tech/content-apis-sdk",
    long_description="""
    Python bindings for Kadalu Content ReST APIs
    """,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only"
    ],
)
