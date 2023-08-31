from setuptools import setup

with open("requirements.txt","r") as f:
    pkgs = [l for l in f.readlines() if len(l)>0]
    
setup(
    name='VNPT',
    version='0.7.1',
    description='A toolkit for noise project on python',
    url='https://github.com/Viyyy/NPT',
    author='Re.VI',
    author_email='another91026@gmail.com',
    license='MIT',
    packages=['vnpt','vnpt.engine'],
    install_requires=pkgs,
    zip_safe=False
)
