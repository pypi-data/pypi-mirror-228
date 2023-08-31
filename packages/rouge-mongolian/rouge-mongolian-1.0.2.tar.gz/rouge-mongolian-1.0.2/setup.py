import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="rouge-mongolian",
    version="1.0.2",
    author="Han yongshun",
    author_email="hys971030@163.com",
    description="蒙古文ROUGE评价工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords=['python', 'rouge', 'mongolian','windows','mac','linux'],
    install_requires=[
        "six>=1.16.0",
    ]
)

