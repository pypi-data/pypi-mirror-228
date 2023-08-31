from setuptools import setup, find_packages

setup(
    name='walnutmod',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pyfiglet',
        'colorama',
        'qrcode',
        'Pillow',  # PIL 是 Pillow 的一部分
        'tqdm',
        'wget',
        'numpy',
        'matplotlib',
        'rarfile'
    ],
)
