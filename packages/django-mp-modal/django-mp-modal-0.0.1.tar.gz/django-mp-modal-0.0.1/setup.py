
from setuptools import setup, find_packages


version = '0.0.1'
url = 'https://github.com/pmaigutyak/mp-modal'


setup(
    name='django-mp-modal',
    version=version,
    description='Django run app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
