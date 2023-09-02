# Diviner
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvdiviner)
![PyPI - License](https://img.shields.io/pypi/l/uvdiviner)
![PyPI](https://img.shields.io/pypi/v/uvdiviner)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uvdiviner)
![PyPI - Downloads](https://img.shields.io/pypi/dw/uvdiviner)

基于周易蓍草占卜原理实现的中国古占卜.

感谢熊逸先生的《周易江湖》对本项目提供的基本原理支持.

## 安装
使用`pip`安装:
```sh
pip install uvdiviner
```

## 使用
### 完整占卜
```python
from uvdiviner.main import main

if __name__ == "__main__":
    main()
```

### 快速占卜
```python
from uvdiviner.divine import divine

def main():
    diagram = divine()
    print("本卦: ", diagram.name)
    diagram.variate()
    print("变卦: ", diagram.name)

if __name__ == "__main__":
    main()
```

### 快速检定
执行以下代码进行快速吉凶检定:
```python
from uvdiviner.divine import quick_check

print(quick_check()) # 返回 True 或 False
```