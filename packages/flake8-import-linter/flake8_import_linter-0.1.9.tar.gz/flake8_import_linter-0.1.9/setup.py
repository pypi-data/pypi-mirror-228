# Third party
from setuptools import setup

# Read the content of your README.md file for long_description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flake8_import_linter',
    description='Flake8 plugin that checks for forbidden imports in your code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Console',
        'Framework :: Flake8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    keywords='flake8 import linter',
    version='0.1.9',
    author='Dan Milgram',
    author_email='ddmilgram@gmail.com',
    install_requires=['flake8', 'wheel'],
    entry_points={
        'flake8.extension': [
            'IMP=flake8_import_linter:Plugin',
        ],
    },
    url='https://github.com/danmilgram/flake8-import-linter',
    license='MIT',
    py_modules=['flake8_import_linter'],
    zip_safe=False,
)
