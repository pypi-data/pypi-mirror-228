from setuptools import setup, find_packages

setup(
    name='walnutmod',
    version='0.2',
    packages=find_packages(),
    package_data={
        'module': ['fakehacker.txt', 'ascii_art.txt'],
    },
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
