from setuptools import setup, find_packages

setup(
    name='cloud_bunny',
    version='0.11',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'numpy',
        'open3d',
        'pye57',
        'pytest',
        'warp-lang',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
