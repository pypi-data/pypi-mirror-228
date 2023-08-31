
from setuptools import setup, find_packages


version = '1.0.6'
url = 'https://github.com/pmaigutyak/mp-orders'


setup(
    name='django-mp-orders',
    version=version,
    description='Django orders apps',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
