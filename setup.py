from setuptools import find_packages, setup

setup(
    name='cowshed',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'run-cowshed=cowshed.app:app.run',
        ],
    },
    author='Pablo Sánchez',
    author_email='pablo.sanchez.armas@nn-group.com',
    description='NNDAP Assignment, manage the farm of Ingrid',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
