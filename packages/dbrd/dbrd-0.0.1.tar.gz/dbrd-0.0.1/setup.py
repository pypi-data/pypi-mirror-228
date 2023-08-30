import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dbrd',
    version='0.0.1',
    author='AP tech',
    author_email='mk-lee@aptechinc.kr',
    description='DBRD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
)
