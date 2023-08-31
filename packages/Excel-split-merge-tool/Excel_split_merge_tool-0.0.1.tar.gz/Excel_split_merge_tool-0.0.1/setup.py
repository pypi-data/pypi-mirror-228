from setuptools import setup, find_packages

__version__ = '0.0.1'
__authur__ = "Pongpol Prommacharoen"
__email__ = "pongpol095@gmail.com"
__github__ = "https://github.com/Armynous"

#----------------------------------------------------------------------------#

# with open("requirements.txt", "r") as file_obj:

#     file_data = file_obj.read()

#     dependencies = file_data.splitlines()

#-------#
# Setup #
#-----------------------------------------------------------------------------#

setup(
    name='Excel_split_merge_tool',
    version=__version__,
    author=__authur__,
    author_email=__email__,
    packages=['main'],
    url='https://github.com/Armynous/split_n_merge_excelfile.git',
    include_package_data=True
)

#-----------------------------------------------------------------------------#