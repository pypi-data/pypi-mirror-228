from setuptools import setup
    
    
def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name='gadgetpie', # project name
    version='0.0.1', # version
    author='Baoming Yu', # author's name
    author_email='dingxuanliang@icloud.com', # author's email
    url='https://github.com/Baoming520/gadgetpie', # url on github
    description='A set of common tools.', # abstract
    long_description=readme(), # contents in README.MD file
    long_description_content_type="text/markdown", # type of long description
    packages=['gadgetpie'], # pakages waiting for packing
    package_data={}, # data files in package
    install_requires=[], # required packages
)