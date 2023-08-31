## 简介

- 在控制台中用于彩色打印的包
- 采用的是亮色
- 支持多值打印

## 安装

```
pip install --index-url https://pypi.org/simple colorPrintConsole -U
```

## 使用

```python
from colorPrintConsole import ColorPrint

cp = ColorPrint()
cp.red('红色文本')
cp.green('绿色文本')
cp.yellow('黄色文本')
cp.blue('蓝色文本')
cp.magenta('品红色文本')
cp.cyan('青色文本')
cp.red('123', '456', '789') # 多值打印

```

## 展示

![效果展示](https://img-1256814817.cos.ap-beijing.myqcloud.com/images/color.png)
