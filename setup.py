from setuptools import setup, find_packages

setup(
    name='kcleaner',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['kcleaner'],
    install_requires=[
        'Click',
        'iterfzf',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        kcleaner=kcleaner:main
    ''',
)