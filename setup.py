# sets up the CLI

from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='reisen',
    version='0.1.2',
    author='Joey Wu',
    author_email='joeywu99@gmail.com',
    short_description='CLI tool to parse & move media files in a folder to another folder',
    url='https://github.com/joeypoyiwu/anime-video-file-renamer-and-mover',
    py_modules=['main'],
    packages=find_packages(),
    install_requires=[
        requirements
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'reisen = reisen:main',
        ],
    },
)