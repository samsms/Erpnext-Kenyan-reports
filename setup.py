from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in techsavanna_payroll/__init__.py
from techsavanna_payroll import __version__ as version

setup(
	name="techsavanna_payroll",
	version=version,
	description="Paayroll Reports",
	author="samson",
	author_email="samsaf674@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
