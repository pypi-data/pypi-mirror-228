from setuptools import setup

setup(
    name='ismeowix',
    version='0.4',
    author='Nekosis',
    description='Library for Meowix Python applications to check if the intended operating system is being used',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Meowix-Linux/python-ismeowix',
    project_urls={
        'Bug Tracker': 'https://github.com/Meowix-Linux/python-ismeowix/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    packages=['ismeowix'],
    install_requires=[
        'distro',
        'colorama',
    ],
)
