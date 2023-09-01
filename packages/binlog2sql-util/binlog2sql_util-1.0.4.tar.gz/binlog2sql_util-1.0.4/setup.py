from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='binlog2sql_util',
      version='1.0.4',   # 版本号
      description='helloworld',  # 包的介绍
      author='binlog2sql_util',  # 作者 
      author_email='1138514746@qq.com',  # 你的邮箱
      url='https://github.com/blackmonkey121/verify',  # 项目地址，一般的填git地址,也可以是任意url
      packages=find_packages(),  # Python导入包的列表
      long_description=long_description,  # 项目的描述 
      long_description_content_type="text/markdown",   # 描述文档REDME的格式，默认markdown
      license="GPLv3",   # 开源协议,默认即可
      classifiers=[
          "Programming Language :: Python :: 3", 
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"],

      python_requires='>=3.3',   # Python 的版本约束
      install_requires=[] # 其他依赖的约束
      )
