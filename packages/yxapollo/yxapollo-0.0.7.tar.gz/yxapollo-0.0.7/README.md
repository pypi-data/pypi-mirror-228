# Example

## apollo.py

```python
from Apollo import Apollo

apollo1 = Apollo("your_appid_1", "your_config_server_url_1")
apollo2 = Apollo("your_appid_2", "your_config_server_url_2")
```

## main.py
```python
from apollo import apollo1,apollo2

value1 = apollo1.get_value("your_key", namespace="your_namespace")
value2 = apollo1.get_value("your_key", namespace="your_namespace")
```

## 打包发版流程
1. setup.py修改版本号push
2. 项目打包
```shell
python3 setup.py sdist bdist_wheel
```
3. 项目发布
```
python3 -m twine upload dist/*
```