from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools import find_packages, setup
from setuptools.command.egg_info import egg_info


setup(
    name='my-dummy-package-11002530',
    packages=find_packages(),
    version="1.0.0",
    include_package_data=True,
    description='soem some',
    author='dsa',
    author_email='test@test.com',
    license='Apache 2.0',
    url='https://github.com/example',
    download_url='https://github.com/example',
    long_description="some package long",
    long_description_content_type='text/markdown',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Unix Shell',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Multimedia :: Video',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Source': 'https://github.com/example',
        'Tracker': 'https://github.com/example',
    },
)