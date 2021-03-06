# Kenzo_Rom_Update_Checker

一个使用Python语言编写的简单的检查Kenzo的Rom更新的工具<br>
(A simple tool to check Kenzo's Rom update in Python)

此程序需要Python 3.5+版本<br>
(This program requires the Python 3.5+ version)

正常运行所必须的第三方库<br>
(Third-party libraries necessary for normal operation)

```
BeautifulSoup4 lxml (or html5lib)
```

由于本人技术笨拙，代码中如果有不完美和可完善的地方，请多为我提供宝贵的意见而不是嘲笑我。<br>
(Due to my technical clumsy, if the code is not perfect enough, please give me more advice, rather than laugh at me.)

此程序不支持在Win和Linux以外的操作系统下运行，并且只支持英文，以后会考虑做出GUI。<br>
(This program does not support OS other than Win and Linux, and only supports English, will consider making a GUI.)

如果需要启动本程序，请执行：<br>
(To execute:)

```sh
python main.py
```

或者：<br>
(or:)

```sh
python3 main.py
```

你还可以使用参数来进行一些快捷的操作。<br>
(You can also use the parameters for some quick operation.)

比如：<br>
(Such as:)
```sh
main.py -a        # 自动检查所有Rom的更新(Automatically check all Rom updates)
main.py -s <argv> # 检查单个项目的更新(Check a single item)
main.py -l        # 显示已保存的最新版本信息(Show saved info)
main.py -x        # 预览Kenzo的XDA Development页面(Preview Kenzo's XDA development page)
```

请享受！<br>
(Enjoy!)
