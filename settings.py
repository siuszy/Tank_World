# 初始游戏界面长、宽
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
# 己方坦克初始化位置（基地左上方） 
MY_BIRTH_LEFT, MY_BIRTH_TOP = SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT - 120
# 方向列表
DIRECTION = [U, D, L, R] = ['U', 'D', 'L', 'R']
# img文件路径
BASE_PATH = r'D:/Python/siu/tank/img/'
# 是否允许左右穿墙
CROSS_WALL = True
# 游戏帧数 
# 根据电脑性能可以做相应调整使得游戏更流畅
INTERVAL = 0.02

# 子弹相对于坦克车速的值（Relative Speed）
# 坦克速度可在己方坦克/敌方坦克类的初始化函数中修改
BULLET_RSPEED = 3

# 己方坦克生命值
MY_TANK_LIFT = 3
# 己方坦克最大连续开火数
MAX_MY_TANK_BULLET = 2
# 进入下一关后己方坦克生命值增加值
ADD_LIFT = 1

# 初始敌方坦克数量
INITIAL_ENEMY_NUMBER = 5
# 敌方坦克最大数量 一般推荐设定不超过 int(SCREEN_WIDTH/60)-1 
# 坦克元素的长宽60*60 数量过多会导致敌方坦克初始化出现重叠，及后续无法移动情况
# 此为可以继续改进的地方：更优的初始化方法和判断互相碰撞的规则
MAX_ENEMY_NUMBER = 15
# 敌方坦克随机移动中最小和最大连续步长
MIN_SEQUENCE_STEP = 30
MAX_SEQUENCE_STEP = 100
# 敌方坦克collide后反应速度 
# 设定与MAX_SEQUENCE_STEP有关 最大值为1（此时collide后会立马随机生成下一个运动方向） 
REFLEX_SPEED = 0.2
# 敌方开火间隔
# 数值越小，开火越密集，最小值为1（不推荐设定过小）
ENEMY_BULLET_INTERVAL = 50
# 游戏界面敌方坦克存续子弹最大数量
# 该值越大，被击中可能性自然越大
MAX_ENEMY_BULLET = 30
# 每进入下一关后敌方坦克数量增加值
ADD_ENEMY = 1

# 墙类生成过程中的间隔参数
# 设定小于60会导致出现两墙虽不相邻但之间无法通过情况
WALL_INTERVAL = 61

# 基地steel/wall两类墙变化的频率
# 该值越大 变化速度越慢
BASE_WALL_INTERVAL = 300
# 基地两墙随机变化依据从该列表随机选出的值 0对应steel 1对应(普通)wall 
# 游戏中每增加通过一个关卡 该初始列表中会被添加一个1 也可以自行设定
RANDOMLIST = [0,1]
# 基地墙类初始化基础
# 改为False 被击中后在本关卡消失 若成功进入下一关不会像普通墙类被重新初始化（重新出现） 
RECEREAT_BASE_WALL = True
# 基地Heart生命值
# 设定为1 即击中就Game Over
MY_HEART_LIFT = 1

# 游戏主类TankGame下creat_wall/creat_enenmy两个函数可以自行设定，对整体元素布局进行改变
# 需要注意的是避免敌方坦克/墙类/己方坦克初始化出现重叠情况
# eg:如果墙类top参数随机生成过程中最大值较大，可能会出现基地正前方出现墙导致左右移动困难（难度提升的一种方法）