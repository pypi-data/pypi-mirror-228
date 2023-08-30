from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='process-logging',
    version='0.1.0',
    description='Simple logging module run on process with python logging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='kyon333',
    author_email='originky2@gmail.com',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['logging', 'multiprocess'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
