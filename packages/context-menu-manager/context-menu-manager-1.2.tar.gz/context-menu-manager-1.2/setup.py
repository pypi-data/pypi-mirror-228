from setuptools import setup, find_packages

setup(
	name = 'context-menu-manager',
	version = '1.2',
	package_dir = {'': 'src'},
	packages = find_packages(where = 'src'),
	license = 'MIT',
	classifiers = [
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 3.11',
		'Operating System :: Microsoft :: Windows'
	],
	python_requires = ">=3.11"
)
