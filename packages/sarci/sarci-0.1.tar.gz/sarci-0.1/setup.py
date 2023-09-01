from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name='sarci',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    authors=['Gui507', 'SoyElDvD', 'Matheus Willamy', 'AmandaPaulaV', 'Levy Pinheiro', 'Brenda Tavares'],
    description='Uma descrição da minha biblioteca',
    url='https://github.com/Gui507/Projeto-SARCI/tree/biblioteca',
)
