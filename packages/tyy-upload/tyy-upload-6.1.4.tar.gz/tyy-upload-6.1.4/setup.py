# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="tyy-upload",
    version="6.1.4",
    description="upload file",
    author="hxl",
    maintainer="hxl",
    packages=find_packages(),
    license='MIT License',
    install_requires=['tqdm==4.62.3', 'setuptools==58.1.0', 'requests==2.26.0'],
    entry_points={
        'console_scripts': [
            'tupload=file_upload.upload:start'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)


