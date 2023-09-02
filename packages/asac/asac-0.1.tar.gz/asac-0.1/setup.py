from setuptools import setup, find_packages

setup(
    name='asac',
    version='0.1',
    packages=find_packages(),
    package_data={
    },
    install_requires=[
        'os',
        'time',
        'curses',
        'moviepy',
        'Pillow',  # PIL 是 Pillow 的一部分
    ],
)
