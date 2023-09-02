from setuptools import setup, find_packages

setup(
    name='nrodataset',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scipy',
        'networkx'
    ],
    author='Chengpei Wu',
    author_email='chengpei.wu@hotmail.com',
    description='A dataset contains multiple network data samples, each of which includes the original network and '
                'the network after robustness optimization',
)
