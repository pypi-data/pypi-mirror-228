from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='numequate',
    version='0.3.0',
    license="MIT License (MIT)",
    description="A Python Mathematics Library.",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TuberAsk/numequate",
    project_urls={
        'Source': 'https://github.com/TuberAsk/numequate',
        'Bug Reports': 'https://github.com/TuberAsk/numequate/issues',
        'Documentation': 'https://github.com/TuberAsk/numequate/wiki',
        'Funding': 'https://patreon.com/numequate',
    },
)
