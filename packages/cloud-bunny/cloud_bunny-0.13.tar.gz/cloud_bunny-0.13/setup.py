from setuptools import setup, find_packages

setup(
    name='cloud_bunny',
    version='0.13',
    package_dir={'': 'cloud_bunny'},
    packages=find_packages(where='cloud_bunny'),
    author='Akeel Ather Medina',
    author_email='akeelmedina22@gmail.com',
    description='A Warp-Accelerated Python library for point cloud processing.',
    readme='README.md',
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
