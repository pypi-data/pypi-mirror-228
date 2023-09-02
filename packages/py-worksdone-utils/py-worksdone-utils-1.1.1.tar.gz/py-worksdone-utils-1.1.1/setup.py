from setuptools import setup, find_packages

# Setting up
setup(
    name="py-worksdone-utils",
    version="1.1.1",
    author="KE",
    author_email="",
    description="Utilities with Keycloak",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["python-keycloak==3.3.0"],
    keywords=["python", "decorator", "token", "keycloak"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
