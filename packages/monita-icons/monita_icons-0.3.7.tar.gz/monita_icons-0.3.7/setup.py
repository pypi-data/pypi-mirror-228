import setuptools

setuptools.setup(
    name="monita_icons",
    packages=["monita_icons"],
    package_data={"monita_icons": ["vendor_map.json"]},
    include_package_data=True,
    version="0.3.7",
)
