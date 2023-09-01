from setuptools import setup, find_packages

setup(
    name='vatvie',
    version='0.8',
    description='A Python library for checking VAT numbers using the VIES SOAP API',
    long_description='The objective of this library is to allow companies involved in the intra-Community supply of goods or of services to obtain confirmation of the validity of the VAT identification number of any specified person, in accordance to article 31 of Council Regulation (EC) No. 904/2010 of 7 October 2010.',
    author='Nikolay Oleynikov',
    author_email='nikolay.oleynikov96@gmail.com',
    url='https://github.com/OleynikovNikolay/vatvie',
    download_url='https://github.com/OleynikovNikolay/vatvie/archive/refs/tags/v_01.tar.gz',
    keywords=['VAT', 'SOAP', 'API'],
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    install_requires=[
       'requests',
       're',
    ],
)
