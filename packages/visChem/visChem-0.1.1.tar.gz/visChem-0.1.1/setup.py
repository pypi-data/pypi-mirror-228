from setuptools import setup, find_packages

setup(
    name='visChem',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        line.strip() for line in open('requirements.txt').readlines()
    ],
    author='Steve Niu',
    author_email='stevexniu@gmail.com',
    description='A tool for chemical space visualization and clustering.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)

