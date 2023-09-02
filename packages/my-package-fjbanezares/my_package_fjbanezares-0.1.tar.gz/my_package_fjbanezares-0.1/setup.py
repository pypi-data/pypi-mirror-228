from setuptools import setup, find_packages

setup(
    name='my_package_fjbanezares',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    entry_points={
        'console_scripts': [
            # If you want to create any executable scripts
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple example package',
)
