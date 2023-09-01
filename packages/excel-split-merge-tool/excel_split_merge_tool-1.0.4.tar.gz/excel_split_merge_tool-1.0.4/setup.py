from setuptools import setup

__version__ = '1.0.4'
__authur__ = "Pongpol Prommacharoen"
__email__ = "pongpol095@gmail.com"
__github__ = "https://github.com/Armynous"

#----------------------------------------------------------------------------#

#-------#
# Setup #
#-----------------------------------------------------------------------------#

setup(
    name='excel_split_merge_tool',
    version=__version__,
    author=__authur__,
    author_email=__email__,
    packages=['excel_split_merge_tool'],
    package_dir={'excel_split_merge_tool': 'excel_split_merge_tool'},
    package_data={'excel_split_merge_tool': ['resources/*.py']},
    url='https://github.com/Armynous/split_n_merge_excelfile.git',
    install_requires=[
        'bleach>=6.0.0',
        'build>=0.10.0',
        'certifi>=2023.7.22',
        'charset-normalizer>=3.2.0',
        'colorama>=0.4.6',
        'docutils>=0.20.1',
        'et-xmlfile>=1.1.0',
        'idna>=3.4',
        'importlib-metadata>=6.8.0',
        'jaraco.classes>=3.3.0',
        'keyring>=24.2.0',
        'markdown-it-py>=3.0.0',
        'mdurl>=0.1.2',
        'more-itertools>=10.1.0',
        'numpy>=1.25.2',
        'openpyxl>=3.1.2',
        'packaging>=23.1',
        'pandas>=2.1.0',
        'pkginfo>=1.9.6',
        'Pygments>=2.16.1',
        'pyproject_hooks>=1.0.0',
        'python-dateutil>=2.8.2',
        'pytz>=2023.3',
        'pywin32-ctypes>=0.2.2',
        'readme-renderer>=41.0',
        'requests>=2.31.0',
        'requests-toolbelt>=1.0.0',
        'rfc3986>=2.0.0',
        'rich>=13.5.2',
        'six>=1.16.0',
        'tomli>=2.0.1',
        'tqdm>=4.66.1',
        'twine>=4.0.2',
        'tzdata>=2023.3',
        'urllib3>=2.0.4',
        'webencodings>=0.5.1',
        'zipp>=3.16.2'
    ],
    include_package_data=True
)

#-----------------------------------------------------------------------------#