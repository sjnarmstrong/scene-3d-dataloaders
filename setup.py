from setuptools import setup, find_packages
setup(
    name='dataloader-lib',
    version='0.0.1',
    packages=find_packages(include=["datalib*"]),
    url='https://github.com/sjnarmstrong/scene-3d-dataloaders',
    license='MIT',
    author='sholto',
    author_email='sjnarmstrong@gmail.com',
    description='Project to load and abstract common scene understanding datasets.',
    install_requires=[
    ],
)
