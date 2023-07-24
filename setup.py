from setuptools import setup, find_packages

setup(
    name='corpus_reader',
    version='0.0.2',
    description='A fast and memory-efficient indexing tool for reading large-scale corpora.',
    author='waylight3',
    author_email='waylight3@snu.ac.kr',
    url='https://github.com/waylight3/corpus_reader',
    install_requires=['unidecode',],
    packages=find_packages(exclude=[]),
    keywords=['corpus', 'reader', 'index', 'large data', 'memory-efficient'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)