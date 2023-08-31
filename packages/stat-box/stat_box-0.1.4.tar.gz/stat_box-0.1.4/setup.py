import pathlib
from setuptools import setup, find_packages
from os.path import join, dirname

try:
    long_description = pathlib.Path(join(dirname(__file__), 'readme.md')).read_text()

except:
    long_description = 'Convinient statistical description of dataframes and time series.'

setup(
    name="stat_box",
    packages=find_packages(),
    version="0.1.4",
    license="MIT",
    description="Convinient statistical description of dataframes and time series.",
    author="dmatryus",
    author_email="dmatryus.sqrt49@yandex.ru",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/dmatryus.sqrt49/stat_box",
    keywords=["STATICS", "TIME_SERIES"],
    install_requires=["numpy", "scipy", "pandas", "matplotlib"],
)
