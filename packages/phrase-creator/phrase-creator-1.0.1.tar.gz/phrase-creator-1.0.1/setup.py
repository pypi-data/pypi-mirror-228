from setuptools import setup, find_packages

setup(
    name="phrase-creator",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'phrasemagic = phrase_statement_convertor.main:main',
        ],
    },
    install_requires=[
        "pandas",
        "openpyxl"
    ],
)
