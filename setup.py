import setuptools


setuptools.setup(
    name="my_utils",
    version="0.0.0",
    author="Rajbir Singh Nirwan",
    author_email="rajbir.nirwan@gmail.com",
    description="Utility functions",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pathos>=0.2.8",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov==2.10.1",
            "black>=21.7b0",
        ],
    },
)
