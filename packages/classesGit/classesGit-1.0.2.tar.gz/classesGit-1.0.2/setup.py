from setuptools import setup, find_packages

setup(
    name="classesGit",
    version="1.0.2",
    author="Bogdan Marcu",
    author_email="bogdan.marcu@tss-yonder.com",
    description="Classes for scripts",
    packages=["Fetch", "gitGet", "gitPut", "gitHead", "optionsRepository", "pushRules"],
    package_dir={
        "": ".",
        "Fetch": "./httpReq/Fetch",
        "gitGet": "./httpReq/gitGet",
        "gitHead": "./httpReq/gitHead",
        "gitPut": "./httpReq/gitPut",
        "optionsRepository": "./objectModels/optionsRepository",
        "pushRules": "./objectModels/pushRules",
    }
)
