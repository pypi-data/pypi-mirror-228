import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utils-c",
    version="0.0.7",  # 包版本号，便于维护版本
    author="CodexploRe",  # 作者，可以写自己的姓名
    author_email="1259864733@qq.com",  # 作者联系方式，可写自己的邮箱地址
    url="https://gitee.com/CodexploRe",  # 自己项目地址，比如github的项目地址
    description="A package used to store various modules written by individuals while learning the Python language.",
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'fake_useragent>=1.2.1',
        'lxml>=4.9.3',
        'Requests>=2.31.0',
        'setuptools>=68.1.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT License',
    python_requires='>=3.6',  # 对python的最低版本要求
)
