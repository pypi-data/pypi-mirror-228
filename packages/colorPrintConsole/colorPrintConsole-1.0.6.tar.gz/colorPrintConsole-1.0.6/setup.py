from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='colorPrintConsole',
    version='1.0.6',
    author='苏寅',
    author_email='suyin_long@163.com',
    packages=['colorPrintConsole'],
    description='A package for color printing in the console',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/suyin-long/color-print",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
