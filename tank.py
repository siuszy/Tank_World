import sys
import pygame
import random
import time
from settings import * # 加载游戏配置

# 工具函数：加载图片
def load_img(name_img):
    saved =BASE_PATH + name_img + '.gif'
    return pygame.image.load(saved)

# 工具函数：加载音乐
def load_music(name_music):
    saved = BASE_PATH + name_music + '.wav'
    pygame.mixer.music.load(saved)
    pygame.mixer.music.play()

# pygame精灵的基类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

# 子弹类
class Bullet(BaseItem):
    def __init__(self, tank, window):
        super().__init__()
        self.direction = tank.direction
        self.speed = tank.speed * BULLET_RSPEED
        self.img = load_img('bullet')
        self.rect = self.img.get_rect()
        self.window = window
        self.live = True
        # 调整子弹相对于坦克的位置
        if self.direction == U:
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == D:
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == L:
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        else:
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
    
    def display_bullet(self):
        self.window.blit(self.img, self.rect)

    def bullet_move(self):
        if self.direction == U:
            if self.rect.top > 0:
                self.rect.top -= self.speed
                return
        elif self.direction == D:
            if self.rect.top < SCREEN_HEIGHT:
                self.rect.top += self.speed
                return
        elif self.direction == L:
            if self.rect.left > 0:
                self.rect.left -= self.speed
                return
        else:
            if self.rect.left < SCREEN_WIDTH:
                self.rect.left += self.speed
                return
        self.live = False

    def hit_enemy_tank(self):
        for enemy in TankGame.enemy_tank_list:
            hit = pygame.sprite.collide_rect(self, enemy)
            if hit:
                self.live = False
                if enemy.click_count == 1:
                    enemy.live = False
                    return None
                enemy.click_count -= 1
                if enemy.click_count == 2:
                    enemy.load_image = enemy.img32
                if enemy.click_count == 1:
                    enemy.load_image = enemy.img31
                load_music('hit')

    def hit_my_tank(self, tank):
        hit = pygame.sprite.collide_rect(self, tank)
        if hit:
            self.live = False
            tank.live = False

    def bullet_collide_wall(self):
        for wall in TankGame.wall_list:
            result = pygame.sprite.collide_rect(self, wall)
            if result:
                self.live = False
                if wall.count == 1:
                    wall.live = False
                else:
                    load_music('hit')
        
        for wall in TankGame.basewall_list:
            result = pygame.sprite.collide_rect(self, wall)
            if result:
                self.live = False
                if wall.count == 1:
                    wall.live = False
                else:
                    load_music('hit')
        
        for heart in TankGame.heart_list:
            result = pygame.sprite.collide_rect(self, heart)
            if result:
                self.live = False
                heart.count -= 1
                if heart.count == 0: 
                    heart.live = False
                else:
                    load_music('hit')
        
    def bullet_collide_bullet(self):
        for bullet in TankGame.enemy_bullet_list:
            if pygame.sprite.collide_rect(bullet, self):
                bullet.live = False
                self.live = False

# 坦克类
class Tank(BaseItem):
    def __init__(self, left, top, window, image, direction, speed):
        super().__init__()
        self.window = window
        self.load_image = image
        self.direction = direction
        self.img = self.load_image[self.direction]
        self.rect = self.img.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.tank_width = self.rect.width
        self.tank_height = self.rect.height
        self.cross_wall = CROSS_WALL # 是否允许左右穿墙
        self.move_stop = True
        self.live = True
        self.old_left = 0
        self.old_top = 0

    def fire(self):
        return Bullet(self, self.window)

    def display(self):
        self.img = self.load_image[self.direction]
        self.window.blit(self.img, self.rect)

    def meet_boundary(self, direction):
        if direction == U:
            return self.rect.top <= 0
        elif direction == D:
            return self.rect.top >= SCREEN_HEIGHT - self.tank_height
        elif direction == L:
            return self.rect.left <= 0
        else:
            return self.rect.left >= SCREEN_WIDTH - self.tank_width

    def move(self, direction):
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        
        if self.cross_wall: 
            if direction == L:
                if self.rect.left < 0:
                    self.rect.left = SCREEN_WIDTH
            elif direction == R:
                self.rect.left %= SCREEN_WIDTH
            else:
                if self.meet_boundary(direction):
                    return None
        elif self.meet_boundary(direction):
            return None

        if direction == U:
            self.rect.top -= self.speed
        elif direction == D:
            self.rect.top += self.speed
        elif direction == L:
            self.rect.left -= self.speed
        else:
            self.rect.left += self.speed

    def stay(self):
        self.rect.left = self.old_left
        self.rect.top = self.old_top

    def tank_collide_wall(self):
        for wall in TankGame.wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
        
        for wall in TankGame.basewall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()
        
        for heart in TankGame.heart_list:
            if pygame.sprite.collide_rect(self, heart):
                self.stay()
                
    def tank_collide_tank(self):
        for tank in TankGame.my_tank_list:
            if self is tank:
                pass
            else:
                if pygame.sprite.collide_rect(self, tank):
                    self.stay() 

        for tank in TankGame.enemy_tank_list:
            if self is tank:
                pass
            else:
                if pygame.sprite.collide_rect(self, tank):
                    self.stay()

# 己方坦克
class MyTank(Tank):
    def __init__(self, left, top, window):
        self.img = dict(U=load_img('p2tankU'), D=load_img('p2tankD'), L=load_img('p2tankL'), R=load_img('p2tankR'))
        self.my_tank_speed = 4
        super().__init__(left, top, window, self.img, U, self.my_tank_speed)

# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, window):
        self.img1 = dict(U=load_img('enemy1U'), D=load_img('enemy1D'), L=load_img('enemy1L'), R=load_img('enemy1R'))
        self.img2 = dict(U=load_img('enemy2U'), D=load_img('enemy2D'), L=load_img('enemy2L'), R=load_img('enemy2R'))
        self.img3 = dict(U=load_img('enemy3U'), D=load_img('enemy3D'), L=load_img('enemy3L'), R=load_img('enemy3R'))
        self.img31 = dict(U=load_img('enemy3U_1'), D=load_img('enemy3D_1'), L=load_img('enemy3L_1'),
                          R=load_img('enemy3R_1'))
        self.img32 = dict(U=load_img('enemy3U_2'), D=load_img('enemy3D_2'), L=load_img('enemy3L_2'),
                          R=load_img('enemy3R_2'))
        # 不同的坦克击中的次数不一样
        image, self.click_count, speed = random.choice([(self.img1, 1, 4), (self.img3, 3, 3), (self.img2, 1, 5)])
        super().__init__(left, top, window, image, self.random_direction(), speed)
        self.step = MAX_SEQUENCE_STEP

    @staticmethod
    def random_direction():
        n = random.randint(0, 3)
        return DIRECTION[n]

    def random_move(self):
        if self.step <= 0:
            self.direction = self.random_direction()
            self.step = random.randint(MIN_SEQUENCE_STEP, MAX_SEQUENCE_STEP)
        else:
            self.move(self.direction)
            self.step -=1

    def random_fire(self):
        if random.randint(0, ENEMY_BULLET_INTERVAL) == 1 and len(TankGame.enemy_bullet_list) < MAX_ENEMY_BULLET:
            enemy_bullet = self.fire()
            TankGame.enemy_bullet_list.append(enemy_bullet)
    
    def move(self, direction): 
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        
        if self.cross_wall: 
            if direction == L:
                if self.rect.left < 0:
                    self.rect.left = SCREEN_WIDTH
            elif direction == R:
                self.rect.left %= SCREEN_WIDTH
            else:
                if self.meet_boundary(direction):
                    self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
                    return None
        elif self.meet_boundary(direction):
            self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
            return None

        if direction == U:
            self.rect.top -= self.speed
        elif direction == D:
            self.rect.top += self.speed
        elif direction == L:
            self.rect.left -= self.speed
        else:
            self.rect.left += self.speed
    
    def tank_collide_wall(self): 
        for wall in TankGame.wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.random_fire()
                self.stay()
                self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
                
        
        for wall in TankGame.basewall_list:
            if pygame.sprite.collide_rect(self, wall):
                if self not in TankGame.my_tank_list:
                    enemy_bullet = self.fire()
                    TankGame.enemy_bullet_list.append(enemy_bullet)
                self.stay()
                self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
        
        for heart in TankGame.heart_list:
            if pygame.sprite.collide_rect(self, heart):
                if self not in TankGame.my_tank_list:
                    enemy_bullet = self.fire()
                    TankGame.enemy_bullet_list.append(enemy_bullet)
                self.stay()
                self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
                
    def tank_collide_tank(self): 
        for tank in TankGame.my_tank_list:
            if self is tank:
                pass
            else:
                if pygame.sprite.collide_rect(self, tank):
                    enemy_bullet = self.fire()
                    TankGame.enemy_bullet_list.append(enemy_bullet)
                    self.stay()
                    self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
                    

        for tank in TankGame.enemy_tank_list:
            if self is tank:
                pass
            else:
                if pygame.sprite.collide_rect(self, tank):
                    self.stay()
                    self.step -= REFLEX_SPEED * MAX_SEQUENCE_STEP
    
# 爆炸动作类
class Explode(BaseItem):
    def __init__(self, tank, window):
        super().__init__()
        self.img = [load_img('blast0'), load_img('blast1'), load_img('blast2'), load_img('blast3'),
                    load_img('blast4'), load_img('blast5'), load_img('blast6')]
        self.rect = tank.rect
        self.stop = 0
        self.window = window
        self.rect.left = tank.rect.left - tank.rect.width / 2

    def display_explode(self):
        load_music('blast')
        while self.stop < len(self.img):
            self.window.blit(self.img[self.stop], self.rect)
            self.stop += 1

# 墙类
class Wall(BaseItem):
    def __init__(self, left, top, window):
        super().__init__()
        self.count = random.randint(0, 1)
        self.img = [load_img('steels'), load_img('walls')][self.count]
        self.rect = self.img.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.window = window
        self.live = True

    def display_wall(self):
        self.window.blit(self.img, self.rect)
    
    def random_change(self):
        if random.randint(0, BASE_WALL_INTERVAL) == 1:
            self.count = random.choice(RANDOMLIST) 
            self.img = [load_img('steels'), load_img('walls')][self.count]

# 基地类
class Heart(BaseItem):
    def __init__(self, left, top, window):
        super().__init__()
        self.count = MY_HEART_LIFT
        self.img = load_img('ecnu')
        self.rect = self.img.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.window = window
        self.live = True
    
    def display_heart(self):
        self.window.blit(self.img, self.rect)

# 游戏主类
class TankGame:
    my_bullet_list = list()
    enemy_bullet_list = list()
    enemy_tank_list = list()
    my_tank_list = list()
    wall_list = list()
    basewall_list = list()
    heart_list = list()

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display = pygame.display
        self.window = self.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE, 32)
        self.display.set_caption('Tank_World')
        self.my_tank = MyTank(MY_BIRTH_LEFT, MY_BIRTH_TOP, self.window)
        TankGame.my_tank_list.append(self.my_tank)
        self.heart = Heart(0.5*SCREEN_WIDTH-30, SCREEN_HEIGHT-60, self.window)
        TankGame.heart_list.append(self.heart)
        self.creat_enemy_number = INITIAL_ENEMY_NUMBER
        self.my_tank_lift = MY_TANK_LIFT
        self.creat_enemy(self.creat_enemy_number)
        self.creat_walls()
        self.creat_basewalls()
        self.font = pygame.font.SysFont('kai_ti', 18)
        self.number = 1
        self.gameover = False
        self.paused = False
        
    def creat_enemy(self, number):
        interval = int(SCREEN_WIDTH/number)
        for index in range(number):
            left = random.randint(index*interval, (index+1)*interval-self.my_tank.tank_width)
            top = random.randint(10,50)
            enemy_tank = EnemyTank(left, top, self.window)
            TankGame.enemy_tank_list.append(enemy_tank)

    def creat_walls(self):
        for i in range(SCREEN_WIDTH // WALL_INTERVAL):
            wall_h = random.randint(120, SCREEN_HEIGHT-240)
            w = Wall(WALL_INTERVAL * i, wall_h, self.window)
            TankGame.wall_list.append(w)
    
    def creat_basewalls(self):
        for base_left,base_top in zip([0.5*SCREEN_WIDTH-90,0.5*SCREEN_WIDTH-30,0.5*SCREEN_WIDTH+30],
                    [SCREEN_HEIGHT-60,SCREEN_HEIGHT-120,SCREEN_HEIGHT-60]
        ):
            w = Wall(base_left, base_top, self.window)
            TankGame.basewall_list.append(w)

    @staticmethod
    def show_walls():
        for w in TankGame.wall_list:
            if w.live:
                w.display_wall()
            else:
                TankGame.wall_list.remove(w)

    @staticmethod
    def show_basewalls():
        for w in TankGame.basewall_list:
            if w.live:
                w.display_wall()
            else:
                TankGame.basewall_list.remove(w)
        for w in TankGame.basewall_list:
            w.random_change()

    def start_game(self):
        global RANDOMLIST
        load_music('start') 
        # 游戏主循环
        while True:
            self.get_event()
            if not self.gameover:
                if not self.paused:
                    self.window.fill([0, 0, 0])
                    len_enemy = len(TankGame.enemy_tank_list)
                    self.window.blit(
                        self.draw_text('敌方坦克*{0},我方生命值*{1},当前{2}关'.format(len_enemy, self.my_tank_lift, 
                                        self.number)), (10, 10))
                    if len_enemy == 0:
                        if self.creat_enemy_number < MAX_ENEMY_NUMBER:
                            self.creat_enemy_number += ADD_ENEMY
                        self.number += 1
                        RANDOMLIST.append(1)
                        self.my_tank_lift += ADD_LIFT
                        # 下一关开始前将己方坦克移动至至初始位置
                        self.my_tank.rect = pygame.Rect(MY_BIRTH_LEFT, MY_BIRTH_TOP, 60, 60) 
                        self.creat_enemy(self.creat_enemy_number)
                        self.wall_list.clear()
                        self.creat_walls()
                        if RECEREAT_BASE_WALL:
                            TankGame.basewall_list = list()
                            self.creat_basewalls()
                    self.show_my_tank()
                    self.show_enemy_tank()
                    self.show_bullet(TankGame.enemy_bullet_list)
                    self.show_bullet(TankGame.my_bullet_list)
                    self.show_walls()
                    self.show_basewalls()
                    self.show_heart()
                    self.display.update()
                    time.sleep(INTERVAL)
            else:
                # 清除游戏中各精灵缓存数据
                TankGame.my_bullet_list = list()
                TankGame.enemy_bullet_list = list()
                TankGame.enemy_tank_list = list()
                TankGame.my_tank_list = list()
                TankGame.wall_list = list()
                TankGame.basewall_list = list()
                TankGame.heart_list = list()
                # 提示
                self.game_over()
                self.display.update()
                time.sleep(INTERVAL)

    def show_heart(self):
        for heart in TankGame.heart_list:
            if heart.live:
                heart.display_heart()
            else:
                TankGame.heart_list.remove(heart)
                self.gameover = True
                
    def show_my_tank(self):
        if self.my_tank.live:
            self.my_tank.display()
            self.my_tank.tank_collide_tank()
            self.my_tank.tank_collide_wall()
        else:
            Explode(self.my_tank, self.window).display_explode()
            del self.my_tank
            if self.my_tank_lift == 0:
                self.gameover = True
            self.my_tank_lift -= 1
            load_music('add')
            TankGame.my_tank_list = list()
            self.my_tank = MyTank(MY_BIRTH_LEFT, MY_BIRTH_TOP, self.window)
            TankGame.my_tank_list.append(self.my_tank)
        if not self.my_tank.move_stop:
            self.my_tank.move(self.my_tank.direction)

    def show_enemy_tank(self):
        for e in TankGame.enemy_tank_list:
            e.random_move()
            e.tank_collide_tank()
            e.tank_collide_wall()
            if e.live:
                e.display()
            else:
                TankGame.enemy_tank_list.remove(e)
                Explode(e, self.window).display_explode()
            e.random_fire()

    def show_bullet(self, ls):
        for b in ls:
            b.bullet_move()
            b.bullet_collide_wall()
            if ls is TankGame.my_bullet_list:
                b.hit_enemy_tank()
                b.bullet_collide_bullet()
            else:
                b.hit_my_tank(self.my_tank)
            if b.live:
                b.display_bullet()
            else:
                ls.remove(b)

    def get_event(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                self.window = self.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE, 32)

            if event.type == pygame.QUIT:
                self.end_game()

            if self.gameover and event.type == pygame.MOUSEBUTTONUP: #重置游戏
                self.gameover = False
                self.__init__()
                self.start_game()

            if event.type == pygame.KEYDOWN:
                # move
                if event.key == pygame.K_UP:
                    self.my_tank.direction = U
                elif event.key == pygame.K_DOWN:
                    self.my_tank.direction = D
                elif event.key == pygame.K_LEFT:
                    self.my_tank.direction = L
                elif event.key == pygame.K_RIGHT:
                    self.my_tank.direction = R
                # fire
                elif event.key == pygame.K_SPACE:
                    if len(TankGame.my_bullet_list) < MAX_MY_TANK_BULLET:
                        bullet = self.my_tank.fire()
                        load_music('fire')
                        TankGame.my_bullet_list.append(bullet)
                # pause
                elif event.key == pygame.K_LCTRL:
                    if self.paused == True:
                        self.paused = False
                    else:
                        self.paused = True
                else:
                    return None

                self.my_tank.move_stop = False 

            elif event.type == pygame.KEYUP:
                self.my_tank.move_stop = True

    def game_over(self):
        font1 = pygame.font.Font(None, 64)
        text = font1.render("Game Over", 1, (255, 0, 0))
        self.window.blit(text, (0.5*SCREEN_WIDTH-100, 0.5*SCREEN_HEIGHT))
        
    def end_game(self):
        self.display.quit()
        sys.exit()

    def draw_text(self, content):
        text_sf = self.font.render(content, True, [255, 0, 0])
        return text_sf

if __name__ == '__main__':
    g = TankGame()
    g.start_game()