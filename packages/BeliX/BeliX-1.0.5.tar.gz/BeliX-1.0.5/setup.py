from setuptools import setup

setup(
    name = 'BeliX',
    version = '1.0.5',
    author = 'X_CODER',
    author_email = 'x.coder.2721@gmail.com',
    description = 'BeliX is a simple and fast Bale Messenger library built for you',
    license = "MIT",
    keywords = ["BeliX_library","messenger","python2","python","python3","api","self","BeliX","Bale", "belix","BELIX","beli X","bale","bot","robot","library","balelib","balelibrary","bale.ai","BaleBot","Bale Api"],
    long_description = open('README.rst').read(),
    python_requires = "~=3.7",
    long_description_content_type = 'text/x-rst',
    url = 'https://ble.ir/belix_py',
    packages = ['BeliX'],
    install_requires = ["aiohttp"],
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ]
)