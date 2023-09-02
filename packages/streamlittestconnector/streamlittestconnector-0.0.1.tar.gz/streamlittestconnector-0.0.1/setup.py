from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Define Streamlit connection'


# Setting up
setup(
    name="streamlittestconnector",
    version=VERSION,
    author="JeongHan Shin (Noah)",
    author_email="junghwanshin@mz.co.kr",
    description=DESCRIPTION,
    packages=find_packages(),
    url="https://github.com/NoahMZC/streamlit-sample-connector.git",
    install_requires=['pymysql', 'cryptography', 'streamlit'],
    keywords=['streamlit','mysql']
    )