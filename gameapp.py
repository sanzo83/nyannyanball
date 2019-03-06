import pyxel
import random

WINDOW_H = 120
WINDOW_W = 160
CAT_H = 16
CAT_W = 16
ENEMY_H = 16
ENEMY_W = 16

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class cat:
    def __init__(self, img_id):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.img_cat = img_id
    
    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class Ball:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.size = 2
        self.speed = 3
        self.color = random.randrange(15) # 0~15
    
    def update(self, x, y, dx, size, color):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
        self.size = size
        self.color = color

class Enemy:
    def __init__(self, img_id):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.speed = 0.02
        self.img_enemy = img_id
    
    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class App:
    def __init__(self):
        self.IMG_ID0_X = 60
        self.IMG_ID0_Y = 65
        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        self.IMG_ID2 = 2
        self.EnemyAppearFlameCount = 0
        self.score = 0

        pyxel.init(WINDOW_W, WINDOW_H, caption="Cat Game")
        pyxel.image(self.IMG_ID0).load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.image(self.IMG_ID1).load(0, 0, "assets/cat_16x16.png")
        pyxel.image(self.IMG_ID2).load(0, 0, "assets/mouse_2.gif")

        # pyxel.mouse(True)

        # make instance
        self.mcat = cat(self.IMG_ID1)
        self.Balls = []
        self.Enemies = []

        # flag
        self.GameOver_flag = 0
        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # ctrl cat
        dx = pyxel.mouse_x - self.mcat.pos.x
        dy = pyxel.mouse_y - self.mcat.pos.y
        if dx != 0:
            self.mcat.update(pyxel.mouse_x, pyxel.mouse_y, dx)
        elif dy != 0:
            self.mcat.update(self.mcat.pos.x, self.mcat.pos.y, self.mcat.vec)
        
        # ctrl enemy
        if pyxel.frame_count - self.EnemyAppearFlameCount == 20 and self.GameOver_flag == 0: # 敵キャラを実体化
            new_enemy = Enemy(self.IMG_ID2)
            new_enemy.update(random.choice((0, WINDOW_W)), random.randrange(WINDOW_H), self.mcat.vec)
            self.Enemies.append(new_enemy)
            
            self.EnemyAppearFlameCount = pyxel.frame_count
        
        enemy_count = len(self.Enemies)
        for i in range(enemy_count):
            # p制御
            ex = (self.mcat.pos.x - self.Enemies[i].pos.x)
            ey = (self.mcat.pos.y - self.Enemies[i].pos.y)
            Kp = self.Enemies[i].speed
            if ex != 0 or ey != 0:
                self.Enemies[i].update(self.Enemies[i].pos.x + ex * Kp,
                self.Enemies[i].pos.y+ ey * Kp,
                self.mcat.vec)
            
            # 当たり判定（敵キャラと猫）
            if ((self.mcat.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                and (self.Enemies[i].pos.x + ENEMY_W < self.mcat.pos.x + CAT_W)
                and (self.mcat.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                and (self.Enemies[i].pos.y + ENEMY_H < self.mcat.pos.y + CAT_H)
            or (self.mcat.pos.x < self.Enemies[i].pos.x)
                and (self.Enemies[i].pos.x < self.mcat.pos.x + CAT_W)
                and (self.mcat.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                and (self.Enemies[i].pos.y + ENEMY_H < self.mcat.pos.y + CAT_H)
            or (self.mcat.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                and (self.Enemies[i].pos.x + ENEMY_W < self.mcat.pos.x + CAT_W)
                and (self.mcat.pos.y < self.Enemies[i].pos.y)
                and (self.Enemies[i].pos.y < self.mcat.pos.y + CAT_H)
            or (self.mcat.pos.x < self.Enemies[i].pos.x)
                and (self.Enemies[i].pos.x < self.mcat.pos.x + CAT_W)
                and (self.mcat.pos.y < self.Enemies[i].pos.y)
                and (self.Enemies[i].pos.y < self.mcat.pos.y + CAT_H)):
                # GameOverフラグを立てる
                self.GameOver_flag = 1

        # ctrl ball
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.GameOver_flag == 0:
            new_ball = Ball()
            if self.mcat.vec > 0:
                new_ball.update(self.mcat.pos.x + CAT_W/2 + 6,
                self.mcat.pos.y + CAT_H/2,
                self.mcat.vec, new_ball.size, new_ball.color)
            else:
                new_ball.update(self.mcat.pos.x + CAT_W/2 - 6,
                self.mcat.pos.y + CAT_H/2,
                self.mcat.vec, new_ball.size, new_ball.color)
            self.Balls.append(new_ball)
        
        ball_count = len(self.Balls)
        for i in range(ball_count):
            if 0 < self.Balls[i].pos.x and self.Balls[i].pos.x < WINDOW_W:
                # Ball update
                if self.Balls[i].vec > 0:
                    self.Balls[i].update(self.Balls[i].pos.x + self.Balls[i].speed,
                    self.Balls[i].pos.y,
                    self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                else:
                    self.Balls[i].update(self.Balls[i].pos.x - self.Balls[i].speed,
                    self.Balls[i].pos.y,
                    self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)

                # 当たり判定（敵キャラとボール）
                attack_enemy_flag = 0
                enemy_count = len(self.Enemies)
                for j in range(enemy_count):
                    if ((self.Enemies[j].pos.x < self.Balls[i].pos.x)
                        and (self.Balls[i].pos.x < self.Enemies[j].pos.x + ENEMY_W)
                        and (self.Enemies[j].pos.y < self.Balls[i].pos.y)
                        and (self.Balls[i].pos.y < self.Enemies[j].pos.y + ENEMY_H)):
                        # 消滅（敵インスタンス破棄）
                        del self.Enemies[j]
                        attack_enemy_flag =1
                        self.score += 100
                        break
                
                if attack_enemy_flag == 1:
                    del self.Balls[i]
                    break
            else:
                del self.Balls[i]
                ball_count -= 1
                break
        
    def draw(self):
        pyxel.cls(0)

        # 背景
        pyxel.blt(self.IMG_ID0_X, self.IMG_ID0_Y, self.IMG_ID0, 0, 0, 38, 16)
        # draw cat
        if self.mcat.vec > 0:
            pyxel.blt(self.mcat.pos.x, self.mcat.pos.y, self.mcat.img_cat, 0, 0, -CAT_W, CAT_H, 5)
        else:
            pyxel.blt(self.mcat.pos.x, self.mcat.pos.y, self.mcat.img_cat, 0, 0, CAT_W, CAT_H, 5)
        
        # draw Balls
        for ball in self.Balls:
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

        # draw Enemy
        for enemy in self.Enemies:
            if enemy.vec > 0:
                pyxel.blt(enemy.pos.x, enemy.pos.y, enemy.img_enemy, 0, 0, -ENEMY_W, ENEMY_H, 11)
            else:
                pyxel.blt(enemy.pos.x, enemy.pos.y, enemy.img_enemy, 0, 0, ENEMY_W, ENEMY_H, 11)
        
        if self.GameOver_flag == 1:
            pyxel.text(self.mcat.pos.x -10, self.mcat.pos.y -5, "GAME OVER", 8)
        
        # スコア
        pyxel.text(0 + 5 , WINDOW_H - 10, "SCORE:" + str(self.score), 7)
        

App()
