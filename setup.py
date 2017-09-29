from setuptools import setup

setup(
    name='stockapp',
    packages=['stockapp'],
    include_package_data=True,
    install_requires=[
        'flask', 'requests'
    ],
)
