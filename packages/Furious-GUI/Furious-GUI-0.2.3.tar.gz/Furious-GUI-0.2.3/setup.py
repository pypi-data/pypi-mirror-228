from Furious.Version import __version__

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='Furious-GUI',
    version=__version__,
    license='GPL v3.0',
    description='A PySide6-based cross platform GUI client that launches your beloved GFW to outer space.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Loren Eteval',
    author_email='loren.eteval@proton.me',
    url='https://github.com/LorenEteval/Furious',
    packages=find_packages(),
    package_data={'Furious': ['Data/**']},
    include_package_data=True,
    install_requires=[
        'PySide6-Essentials',
        'Xray-core',
        'hysteria',
        'ujson',
        'pybase64',
        'pyqrcode',
        'pypng',
        'sysproxy; sys_platform == "win32"',
        'darkdetect; sys_platform != "darwin"',
        'darkdetect[macos-listener]; sys_platform == "darwin"',
    ],
    entry_points={
        'gui_scripts': [
            'Furious = Furious.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
    ],
)
