from setuptools import setup, find_packages

setup(
    name='kcleaner',
    version='0.3.0',
    author='Gui Martins',
    url='https://fancywhale.ca/',
    author_email='gui.martins.94@outlook.com',
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
        kcleaner=kcleaner:cli
    ''',
)
