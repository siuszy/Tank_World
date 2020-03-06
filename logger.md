#### demo1

复现了代码

去除了从网络请求元素图片的操作（**感谢**https://gitee.com/tyoui/logo/tree/master/img提供的素材）

#### demo2

添加pause和restart操作

#### demo3

合并了游戏边界判断，限制了只能左右穿墙

#### demo4

修复了两坦克相遇时的判断bug

更改了部分基础参数 

#### demo5

增加了基地这一元素（加入了base_wall）

#### demo6

增加了Heart类，引入两种触发Game Over模式

修复了部分精灵list缓存未清理导致精灵重叠的bug

#### demo7

将初始参数设定移动至settings.py

改写敌方坦克类下多个collide相关函数，加快敌方坦克碰撞后转向速度

#### demo8（tank）

加入控制敌方坦克反应速度参数使其碰撞后移动更顺畅

更改了敌方坦克开火规则（自身方向上遇到己方坦克、基地组件必开火）

更改了敌方坦克初始化方法


