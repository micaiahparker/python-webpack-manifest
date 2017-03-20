from setuptools import setup
from webpack_manifest import WEBPACK_MANIFEST_VERSION

setup(
    name='webpack-manifest',
    version=WEBPACK_MANIFEST_VERSION,
    packages=['webpack_manifest'],
    description='Manifest loader that allows you to include references to files built by webpack',
    long_description='Documentation at https://github.com/markfinger/python-webpack-manifest',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/python-webpack-manifest',
)
