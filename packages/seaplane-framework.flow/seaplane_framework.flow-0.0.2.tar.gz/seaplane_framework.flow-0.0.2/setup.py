from setuptools import setup, find_namespace_packages


setup(
    name="seaplane_framework.flow",
    version="0.0.2",
    description="",
    long_description="",
    author="Seaplane.IO",
    author_email="carrier-eng@seaplane.io",
    license="Apache Software License",
    packages=find_namespace_packages(include=["seaplane_framework.*"]),
    install_requires=[
        "msgpack>=1.0.5",
    ],
    zip_safe=False,
)
