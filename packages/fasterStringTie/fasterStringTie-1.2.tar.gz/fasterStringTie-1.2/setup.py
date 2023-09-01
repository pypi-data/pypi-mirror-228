from setuptools import setup, find_packages

setup(
    name='fasterStringTie',
    author="Waqar Hanif",
    description="A three times faster version of StringTie.",
    version='1.2',
    packages=find_packages(),
entry_points={
        'console_scripts': [
            'fasterStringTie = fasterStringTie.script:main'
        ]
    }
)
