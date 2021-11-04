# sets up the CLI

from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='Reisen',
    version='0.3.6',
    author='Joey Wu',
    author_email='joeywu99@gmail.com',
    license = 'MIT',
    description='CLI tool to parse & move media files in a folder to another folder',
    url='https://github.com/joeypoyiwu/anime-video-file-renamer-and-mover',
    py_modules=['reisen', 'app'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'reisen = reisen:cli',
        ],
    },
)
