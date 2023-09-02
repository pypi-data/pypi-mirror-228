from setuptools import setup, find_packages

setup(
        name="pyfzf-obj",
        version="0.1.1",
        packages=find_packages(),
        install_requires=[
            ],
        author="Max de Hoyos",
        description="Get actual python objects back from `pyfzf-iter`, not strings",
        )
