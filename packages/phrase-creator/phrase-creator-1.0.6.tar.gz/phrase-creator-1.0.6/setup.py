from setuptools import setup, find_packages

setup(
    name="phrase-creator",
    py_modules=['phrase'],
    version="1.0.6",
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
