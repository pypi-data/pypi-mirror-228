from setuptools import setup, find_packages

setup(
    name="laulec-super-lib-test-485930284",
    version="0.3.0",
    description="Your package description",
    author="Lautaro",
    author_email="lautarolecumberry@users.noreply.github.com",
    packages=find_packages(),
    extras_require={
        'partA': ['partA'],
        'partB': ['partB'],
    },
)
