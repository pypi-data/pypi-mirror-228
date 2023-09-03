from setuptools import find_packages, setup

PACKAGE_NAME = "pffabric"

setup(
    name="pffabric",
    version="0.0.2",
    description="This package contains promptflow tools for working with Microsoft Fabric Lakehouse.",
    packages=find_packages(),
    entry_points={
        "package_tools": ["lakehouse = fabric.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)