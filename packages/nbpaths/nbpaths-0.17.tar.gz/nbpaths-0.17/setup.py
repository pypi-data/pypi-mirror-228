from setuptools import setup, find_packages

setup(
    name="nbpaths",
    version="0.17",
    description="Import package to add parent folders to path for Jupyter notebooks. Will not go higher up tree than .gitignore if found.",
    author="auth",
    author_email="author@email.com",
    license="MIT",
    packages=["nbpaths"],
    zip_safe=False,
)
