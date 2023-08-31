from setuptools import setup, find_packages

setup(
    name="EcodeX",
    version="0.0.0.3",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
    ],

    author="欣源科技EcoSpace",
    author_email="ecospace@qq.com",
    description="SpadaOS官方GUI库EcodeX",
    long_description=open("README.md",encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"#,
        #"Programming Language :: Python :: 3.6",
        #"Programming Language :: Python :: 3.7",
        #"Programming Language :: Python :: 3.8",
        #"Programming Language :: Python :: 3.9",
    ],
)