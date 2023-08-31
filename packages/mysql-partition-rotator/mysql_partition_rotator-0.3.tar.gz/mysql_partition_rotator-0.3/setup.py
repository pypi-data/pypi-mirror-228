from setuptools import setup
import pathlib
here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
here = pathlib.Path(__file__).parent.resolve()


setup(
    name='mysql_partition_rotator',
    packages=['mysql_partition_rotator'],
    version='0.3',
    license='MIT',
    description='Rotates mysql tables by using partition method',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Jimmy Atauje',
    author_email='jimmy.atauje@gmail.com',
    url='https://github.com/jinraynor1/mysql_partition_rotator',
    download_url='https://github.com/jinraynor1/mysql_partition_rotator/releases/tag/v0.3-alpha',
    keywords=['mysql', 'partition', 'rotate', 'python'],
    install_requires=[
        'pymysql',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
