from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="numequate",
    version="0.0.2",
    author="TuberAsk",
    description="A Mathematics Python PyPi Library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Homepage": "https://github.com/TuberAsk/numequate",
        "Bug Tracker": "https://github.com/TuberAsk/numequate/issues",
        "Funding": "https://patreon.com/numequate",
        "Documentation": "https://github.com/TuberAsk/numequate/wiki",
    },
)
