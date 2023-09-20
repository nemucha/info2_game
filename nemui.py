import pyxel
import math

pyxel.init(800, 800)

pyxel.image(0).load(0, 0, "p.png")

pyxel.mouse(True)

class Back: #　複数個のクラス定義を使用している
    def __init__(self):
        self.x = pyxel.rndi(0,799)
        self.y = pyxel.rndi(0,799)
        
    def draw(self):
        pyxel.rect(self.x, self.y, 1, 1, 7)
        
class Earth: #　複数個のクラス定義を使用している
    def draw(self):
        pyxel.blt(320, 320, 0, 0, 0, 160, 160, 7)
        
class Moon:
    def __init__(self):
        self.r = 0
        self.x = 0
        self.y = 0
        
    def update(self, item): #　異なる規則によって動く図形が3種類以上ある
        if pyxel.btn(pyxel.KEY_LEFT): #　キー入力を使用している
            self.r -= 10
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.r += 10
        self.x = 350+pyxel.cos(self.r)*150
        self.y = 350+pyxel.sin(self.r)*150
        for i in range(len(item)):
            if (self.x <= item[i].x <= self.x + 95 and self.y <= item[i].y <= self.y + 95):
                del item[i]
                Item.points += 1
                break
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 165, 0, 95, 95, 7)

class Item:
    points = 0
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        while(0 <= self.x <= 800 and 0 <= self.y <= 800):
            self.x = pyxel.rndi(-200, 1000) #　乱数を使用している
            self.y = pyxel.rndi(-200, 1000)
        self.speed = 2
            
    def update(self): #　異なる規則によって動く図形が3種類以上ある
        self.vx = 400 - self.x
        self.vy = 400 - self.y
        self.x += (self.vx / (pyxel.sqrt(self.vx**2 + self.vy**2))) * self.speed * ( 4 - math.log10(pyxel.sqrt((400 - self.x)**2))) # pyxel.sqrtという平方根を求める授業に出てこなかった機能を使用している
        self.y += (self.vy / (pyxel.sqrt(self.vx**2 + self.vy**2))) * self.speed * ( 4 - math.log10(pyxel.sqrt((400 - self.y)**2)))
        
    def draw(self):
        pyxel.rectb(self.x,self.y, 5, 5, 6)
        
class Artificial_Satellite:
    def __init__(self):
            self.r = -10
            self.x = 0
            self.y = 0
            self.height = 0
            self.stop_r = 0
        
    def update(self,missile): # self以外の引数を持つメソッドを使用している
        if self.stop_r == self.r:
            self.height = 20 + (pyxel.rndi(0,6) * 5)
            self.stop_r = (pyxel.rndi(0,35))*10
            missile.append(Missile(self.x + 47, self.y + 47, 398+pyxel.cos(self.r)*(200 + self.height), 398+pyxel.sin(self.r)*(200 + self.height)))
        else:
            self.r = (self.r + 10) % 360
        self.x = 350+pyxel.cos(self.r)*150
        self.y = 350+pyxel.sin(self.r)*150
        return missile
        
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 165, 100, 95, 95, 7)
        
class Aim:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 20
        self.stop_time = 0
        self.color = 3
        
    def update(self, moon, missile): #　異なる規則によって動く図形が3種類以上ある
        if self.stop_time <= 8:
            self.color = 3
        if 40 <= self.height and pyxel.btn(pyxel.KEY_DOWN):
            self.height -= 20
        if self.height <= 200 and pyxel.btn(pyxel.KEY_UP):
            self.height += 20
        self.x = 398+pyxel.cos(moon.r)*(200 + self.height)
        self.y = 398+pyxel.sin(moon.r)*(200 + self.height)
        self.shot(moon, missile)
        return missile
            
    def shot(self, moon, missile):
        if self.stop_time == 0 and pyxel.btn(pyxel.KEY_SPACE):
            self.stop_time = 10
            self.color = 8
            missile.append(Missile(moon.x + 47, moon.y + 47, self.x, self.y))
            
        if not (self.stop_time == 0):
            self.stop_time -= 1
        
            
    def draw(self):
        pyxel.line(self.x - 10, self.y, self.x - 15, self.y, self.color)
        pyxel.line(self.x + 10, self.y, self.x + 15, self.y, self.color)
        pyxel.line(self.x, self.y - 10, self.x, self.y - 15, self.color)
        pyxel.line(self.x, self.y + 10, self.x, self.y + 15, self.color)
        pyxel.circ(self.x, self.y, 2, self.color)

class Missile:
    def __init__(self, moon_x, moon_y, aim_x, aim_y):
        self.moon_x = moon_x
        self.moon_y = moon_y
        self.aim_x = aim_x
        self.aim_y = aim_y
        self.long = 0
        
    def update(self):
        self.long += 1
        return int(self.long / 11)
    
    def draw(self):
        pyxel.line(self.moon_x, self.moon_y, self.moon_x + (self.aim_x - self.moon_x)*self.long/10, self.moon_y + (self.aim_y - self.moon_y)*self.long/10, 7)

class Attack:
    def __init__(self, missle):
        self.x = missle.aim_x
        self.y = missle.aim_y
        self.r = 0
        self.scene = 0
        self.end = 0
        self.color = 0
        self.del_list = []
        
    def update(self, meteorite, item, r):
        self.del_list = []
        self.color = (self.color + 1) % 15
        if self.scene == 0:
            self.r += 1
            if self.r >= 20 + r * 5:
                self.scene = 1
        elif self.scene == 1:
            self.r -= 1
            if self.r <= 0:
                self.scene = 2
        else:
            self.end = 1
        for i in range(len(meteorite)):
            if ((meteorite[i].x - self.x) ** 2 + (meteorite[i].y - self.y) ** 2) < (20 + self.r) ** 2: #　アルゴリズムが複雑な部分
                del meteorite[i]
                item.append(Item())
                break
        return self.end, meteorite, item
    
    def draw(self):
        pyxel.circ(self.x, self.y, self.r, self.color + 1)
        
class Meteorite:
    def __init__(self, color):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.black_ball_size = 1
        self.black_ball_in = 0
        while(0 <= self.x <= 800 and 0 <= self.y <= 800):
            self.x = pyxel.rndi(-200, 1000)
            self.y = pyxel.rndi(-200, 1000)
        self.color = color
        self.speed = 0.5
        if self.color == 11:
            self.speed = 1
        if self.color == 14:
            self.black_ball_size = 2
            
    def update(self, blackball, scene):
        self.vx = 400 - self.x
        self.vy = 400 - self.y
        self.black_ball_in = 0
        self.x += (self.vx / (pyxel.sqrt(self.vx**2 + self.vy**2))) * self.speed * ( 4 - math.log10(pyxel.sqrt((400 - self.x)**2)))
        self.y += (self.vy / (pyxel.sqrt(self.vx**2 + self.vy**2))) * self.speed * ( 4 - math.log10(pyxel.sqrt((400 - self.y)**2)))
        for i in range(len(blackball)):
            if (self.x - blackball[i].x) ** 2 + (self.y - blackball[i].y) ** 2 <= (blackball[i].r*20) ** 2:
                self.black_ball_in = 1
        if ((self.vx) ** 2 + (self.vy) ** 2 <= 80 ** 2) and self.black_ball_in == 0:
            blackball.append(Black_Ball(self.x, self.y, self.black_ball_size))
        if (self.vx) ** 2 + (self.vy) ** 2 <= (self.black_ball_size * 20) ** 2:
            scene = 4
        return blackball, scene
        
    def draw(self):
        pyxel.circ(self.x, self.y, 20, self.color)
        
class Black_Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        
    def draw(self):
        pyxel.circ(self.x, self.y, 20 * self.r, 0)
        
class App:
    def __init__(self):
        self.scene = 0
        self.phase = 0
        self.earth = Earth()
        self.moon = Moon()
        self.aim = Aim()
        self.item = []
        self.item_1_rate_list = [3, 5, 7, 99] #　リストを使用している
        self.item_2_rate_list = [2, 4, 6, 99]
        self.artificial_satellite = []
        self.back = [Back() for o in range(20)]
        self.meteorite = []
        self.missile = []
        self.attack = []
        self.black_ball = []
        self.ball_del_list = []
        self.missile_del = 0
        self.attack_del = 0
        self.big_r = 0
        self.black_ball_len = 0
        self.scene_change_time = 180
        # 11(緑の早い隕石),13(灰の一般的な隕石), 14(赤の爆発範囲の大きい隕石)
        self.meteorite_color = [[11, 13, 14],[13, 13, 13, 13],[14, 14, 14, 14, 14],[11, 11, 11, 11],[11, 14, 11, 14, 11, 14],[11, 11, 11, 13, 13, 13, 14, 13, 14, 11, 14, 11, 14, 11, 14]]
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.scene == 0:
            if ((350 <= pyxel.mouse_x <= 450) and (350 <= pyxel.mouse_y <= 450)) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): #　マウス座標を使用している
                self.scene = 1
                pyxel.mouse(False)
                
        if self.scene == 1:
            self.moon.update(self.item)
            self.aim.update(self.moon, self.missile)
            for t in range(len(self.item)):
                self.item[t].update()
            for q in range(len(self.artificial_satellite)):
                self.artificial_satellite[q].update(self.missile)
            for i in range(len(self.missile)):
                self.missile_del = 0
                self.missile_del = self.missile[i].update()
                if self.missile_del == 1:
                    self.attack.append(Attack(self.missile[i]))
                    del self.missile[i]
                    break
            if pyxel.rndi(0, 59) == 0 and len(self.meteorite_color[self.phase]) > 0:
                self.meteorite.append(Meteorite(self.meteorite_color[self.phase][0]))
                del self.meteorite_color[self.phase][0]
            for o in range(len(self.meteorite)):
                self.black_ball_len = len(self.black_ball)
                self.black_ball, self.scene = self.meteorite[o].update(self.black_ball, self.scene)
                if len(self.black_ball) - self.black_ball_len == 1:
                    del self.meteorite[o]
                    break
            for l in range(len(self.attack)):
                self.attack_del = 0
                self.attack_del, self.meteorite, self.item = self.attack[l].update(self.meteorite, self.item, self.big_r)
                if self.attack_del == 1:
                    del self.attack[l]
                    break
            if (len(self.meteorite)+len(self.meteorite_color[self.phase]) == 0):
                self.scene_change_time -= 1
                if self.scene_change_time == 0:
                    self.scene = 2
                    if self.phase == len(self.meteorite_color) - 1:
                        self.scene = 3
                    self.scene_change_time = 180
                    pyxel.mouse(True)
                    
        if self.scene == 2:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if (300 <= pyxel.mouse_x <= 350) and (120 <= pyxel.mouse_y <= 170) and (Item.points >= self.item_1_rate_list[0]):
                    self.big_r += 1
                    Item.points -= self.item_1_rate_list[0]
                    del self.item_1_rate_list[0]
                elif (375 <= pyxel.mouse_x <= 425) and (120 <= pyxel.mouse_y <= 170) and (Item.points >= self.item_2_rate_list[0]):
                    self.artificial_satellite.append(Artificial_Satellite())
                    Item.points -= self.item_2_rate_list[0]
                    del self.item_2_rate_list[0]
                elif (300 <= pyxel.mouse_x <= 430) and (250 <= pyxel.mouse_y <= 280):
                    self.scene = 1
                    self.phase += 1
                    pyxel.mouse(False)
            
    def draw(self):
        pyxel.cls(7)
        if self.scene == 0:
            pyxel.rect(350,350,100,100,8)
            pyxel.text(390,397,'start',0)
            
        if self.scene == 1:
            pyxel.cls(0)
            pyxel.text(10, 10, 'Remaining meteorites:'+ str(len(self.meteorite)+len(self.meteorite_color[self.phase])), 7)
            pyxel.text(10, 30, 'Points I have:'+ str(Item.points), 7)
            for n in self.back:
                n.draw()
            for u in range(len(self.item)):
                self.item[u].draw()
            self.earth.draw()
            self.aim.draw()
            for r in range(len(self.artificial_satellite)):
                self.artificial_satellite[r].draw()
            for j in range(len(self.missile)):
                self.missile[j].draw()
            for m in range(len(self.attack)):
                self.attack[m].draw()
            for w in range(len(self.black_ball)):
                self.black_ball[w].draw()
            self.moon.draw()
            for p in range(len(self.meteorite)):
                self.meteorite[p].draw()
                
        if self.scene == 2:
            pyxel.text(300, 30, 'Points I have', 0)
            pyxel.text(367, 30, 'P', 0)
            pyxel.text(382, 30, str(Item.points), 0)
            pyxel.rectb(360, 25, 15, 15, 0)
            pyxel.text(305, 103, 'P', 0)
            if (len(self.item_1_rate_list)):
                pyxel.text(315, 103, str(self.item_1_rate_list[0]), 0)
            pyxel.rectb(300, 100, 10, 10, 0)
            pyxel.circ(325,140,10,int((pyxel.frame_count/2) % 15) + 1)
            pyxel.text(320,160,'big',0)
            pyxel.text(300, 180, 'Expansion of', 0)
            pyxel.text(300, 190, 'explosion range', 0)
            pyxel.rectb(300, 120, 50, 50, 0)
            pyxel.text(380, 103, 'P', 0)
            if (len(self.item_2_rate_list)):
                pyxel.text(390, 103, str(self.item_2_rate_list[0]), 0)
            pyxel.rectb(375, 100, 10, 10, 0)
            pyxel.text(388,160,'create',0)
            pyxel.text(375, 180, 'Building Satellites', 0)
            pyxel.rect(385, 125, 30, 30, 1)
            pyxel.rectb(375, 120, 50, 50, 0)
            pyxel.rect(300, 250, 130, 30, 14)
            pyxel.text(360, 263, 'END', 0)
            
        if self.scene == 3:
            pyxel.text(360, 397, 'Game Clear!', 0)
            
        if self.scene == 4:
            pyxel.text(360, 397, 'Game Over', 0)
App()