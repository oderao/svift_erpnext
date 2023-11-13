from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in svift_erpnext/__init__.py
from svift_erpnext import __version__ as version

setup(
	name="svift_erpnext",
	version=version,
	description="customization for the svift app[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D[D",
	author="Odera Inc",
	author_email="tripleo4u@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
