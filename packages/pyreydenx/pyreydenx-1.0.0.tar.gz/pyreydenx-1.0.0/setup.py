import os
from distutils.core import setup

from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='pyreydenx',
    packages=find_packages(),
    python_requires='>=3.9',
    version='1.0.0',
    license='Apache Software License',
    description='Reyden-X is an automated service for promoting live broadcasts on external '
                'sites with integrated system of viewers and views management.',
    long_description=README,
    author='pixel365',
    author_email='pixel.365.24@gmail.com',
    url='https://github.com/pixel365/pyreydenx',
    download_url='https://github.com/pixel365/pyreydenx/archive/master.zip',
    project_urls={
        'Documentation': 'https://api.reyden-x.com/docs',
        'Source': 'https://github.com/pixel365/pyreydenx',
    },
    keywords=['reydenx', 'twitch', 'trovo', 'youtube', 'vkplay', 'goodgame'],
    install_requires=[
        'requests',
        'pydantic',
    ],
    setup_requires=[
        'requests',
        'pydantic',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
