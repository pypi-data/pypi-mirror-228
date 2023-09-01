from setuptools import setup, find_packages

setup(
    name="phrase-creator",
    version="1.0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'phrasemagic = phrasestatementconvertor.main:main',
        ],
    },
    install_requires=[
        "pandas",
        "openpyxl"
    ],
)
