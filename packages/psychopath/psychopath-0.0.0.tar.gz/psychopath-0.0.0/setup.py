from setuptools import find_packages, setup
from pathlib import Path

cwd = Path.cwd()
about = {}
exec((cwd / 'psychopath' / '__version__.py').read_text(), about)

install_requires = [
    'httpx[http2]',
    'uvloop; platform_system != "Windows"',
    'nest-asyncio',
    'aiofiles',
    'tqdm',
    'orjson',
]

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    description=about['__description__'],
    license=about['__license__'],
    long_description=(cwd / 'README.md').read_text(),
    python_requires=">=3.10.10",
    long_description_content_type='text/markdown',
    author_email='trevorhobenshield@gmail.com',
    url='https://github.com/trevorhobenshield/psychopath',
    install_requires=install_requires,
    keywords='data science ml machine learning deep learning utility tools helpers images videos text audio',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
