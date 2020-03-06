# Tank_World

基于**pygame**的坦克大战

依托于https://github.com/ml365/some-code/blob/master/tanke.py 提供的框架

仅做了细节的优化，不甚感激！

编写过程共做了8个demo，对源码做的相应改动记录于**logger.md**

## 如何运行

下载或克隆整个文件夹。

**settings.py**包含了整个游戏所需的全局参数，初次运行可以仅修改*BASE_PATH*，指向*img*文件夹所在的路径。

Python3（编写环境是Python3.7.0）命令行模式打开**tank.py**（保证与**settings.py**在同一路径下）。

## 游戏规则与操作简述

**规则**

继承了经典的坦克大战的游戏规则，当己方坦克生命值耗尽或基地被攻下均*Game Over*

细节可参考**settings.py**

**操作**

Key_UP/DOWN/LEFT/RIGHT：控制坦克方向

SPACE: Fire

LCtrl: Pause

鼠标任意点击：Game Over后重新开始

