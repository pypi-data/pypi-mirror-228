# Yantu-Tools For Python
Yantu-Tools-Python是言图科技提供的以Python语言编写的应用程序库，以实现对Yantu API便捷访问。它包括一个用于初始化的API资源的预定义类集，可以方便地访问Yantu API，以高效地使用言图私域知识库、言图文档问答等功能。

## 安装

```
pip install --upgrade yantu-tools-python
```
使用以下命令从源代码安装：
```
python setup.py install
```
## 用法
该库需要使用您帐户的密钥进行配置，该密钥可在[言图科技官方网站](http://www.yantu-tech.com/)上找到。
```python
yt_object = YantuObject('您的密钥')
```
或直接设置yantu_key
```python
import yantu-tools-python
yantu-tools-python.yantu_key = "您的密钥"
```