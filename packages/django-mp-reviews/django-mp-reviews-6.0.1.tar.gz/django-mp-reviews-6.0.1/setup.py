
from setuptools import setup, find_packages

version = '6.0.1'


url = 'https://github.com/pmaigutyak/mp-reviews'


setup(
    name='django-mp-reviews',
    version=version,
    description='Django reviews apps',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
)
