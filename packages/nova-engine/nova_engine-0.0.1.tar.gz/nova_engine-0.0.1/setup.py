from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Un framework de création de jeu vidéo basé sur Pygame.'

setup(
    name="nova_engine",
    version=VERSION,
    author="Meziane Ayoub",
    author_email="<meziane.ayoub2006@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pygame-ce', 'pillow'],
    keywords=['python', 'videogame', 'powerfull'],
    classifiers=[
        "Development Status :: 1 - Planning",
    ]
)
