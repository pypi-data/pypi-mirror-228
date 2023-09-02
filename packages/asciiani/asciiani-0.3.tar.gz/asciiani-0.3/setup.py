from setuptools import setup, find_packages

setup(
    name='asciiani',
    version='0.3',
    packages=find_packages(),
    package_data={
    },
    install_requires=[
        'windows-curses',
        'moviepy',
        'Pillow',  # PIL 是 Pillow 的一部分
    ],
)
