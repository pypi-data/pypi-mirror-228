from setuptools import setup, find_packages

setup(
    name="phrase-creator",
    version="1.0.5",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'phrasemagic=phrase:main'
        ],
    },
    install_requires=[
        "pandas",
        "openpyxl"
    ],
)
