import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.label import Label
import traceback as tb
from math import sqrt, atan2
import random

def dist(a,b):
    dx = b[0]-a[0]
    dy = b[1]-a[1]
    return sqrt(dx*dx+dy*dy)

class ErrorApp(App):
    def __init__(self, **args):
        super(ErrorApp, self).__init__(**args)
        self.msg=args["msg"]    
        
    def build(self):
        return Label(text=self.msg)

def errorm(r):
    ErrorApp(msg=r).run()


class LaserTurret(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    
    def __init__(self, **args):
        super(LaserTurret, self).__init__(**args)
    
    def update(self, dt):
        self.pos[0]=5
        
class GunTurret(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    cooldown = NumericProperty()
    maxRange = NumericProperty()
    coolcycle = 0.1
    target = None
    
    def __init__(self, **args):
        super(GunTurret, self).__init__(**args)
        self.cooldown = self.coolcycle
        
    def update(self, dt):
        self.chooseTarget(self.parent.enemies)
        
        self.cooldown -= dt
        if(self.cooldown<0):
            if self.target!=None:
                self.cooldown = self.coolcycle
                self.shoot()
    
        for c in self.children:
            c.update(dt)
            
        for c in self.children:
            if c.destroyMe:
                self.remove_widget(c)
                del c
            
    def shoot(self):
        self.add_widget(Bullet(pos=self.pos, target=self.target))
        pass

    def chooseTarget(self, enemies):
        self.target = None
        tdist = self.maxRange
        for e in enemies:
            d = dist(e.pos, self.pos)
            if (d<tdist):
                self.target = e
                tdist = d
        if self.target:
            a = atan2(self.target.pos[1]-self.pos[1], self.target.pos[0]-self.pos[0])
            self.orient = a*180/3.14159
            
        
class Bullet(Widget):
    speed=150.0
    destroyMe=False
    
    def __init__(self, **args):
        super(Bullet, self).__init__(**args)
        self.target = args["target"]
        self.lasttpos = self.target.pos
    
    def update(self, dt):
        try:
            tpos = self.target.pos
            self.lasttpos = tpos
        except:
            tpos = self.lasttpos
        dv = [tpos[0] - self.pos[0], tpos[1] - self.pos[1]]
        norm = sqrt(float(dv[0]*dv[0]+dv[1]*dv[1]))
        dv[0] /= norm
        dv[1] /= norm
        self.pos = Vector(dv[0]*self.speed*dt, dv[1]*self.speed*dt) + self.pos
        if dist(self.pos, tpos)<self.speed*dt*2:
            self.target.hit(self)
            self.destroyMe=True
        

class Base(Widget):
    d = NumericProperty()
    
    def __init__(self, **args):
        super(Base, self).__init__(**args)

class SquareEnemy(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    life = NumericProperty()
    speed = NumericProperty()
    destroyMe = False
    
    def __init__(self, **args):
        super(SquareEnemy, self).__init__(**args)
        
    def update(self, dt):
        self.pos = Vector(-1, 0)*dt*self.speed + self.pos
        if self.life<=0:
            self.life=0
            self.destroyMe=True
        
    def hit(self, bullet):
        self.life -= 0.1
        if self.life<=0:
            self.life=0
        

class TurretGame(Widget):
    main_base = ObjectProperty(None)
    deblog = ObjectProperty(None)
    life = NumericProperty()
    firstresize=True
    enemies=list()

    def spawn_enemy(self, pos):
        e=SquareEnemy(pos=pos)
        self.enemies.append(e)
        self.add_widget(e)
    
    def update(self, dt):
        if self.size==[100,100]:
            return
        if self.firstresize:
            #self.deblog.text=str(self.size)
            self.firstresize = False
            self.spawn()
            
        for c in self.children:
            #c.update(dt)
            try:
                c.update(dt)
            except AttributeError:
                pass

        for c in self.enemies:
            if c.destroyMe:
                self.remove_widget(c)
                self.enemies.remove(c)
                
        if random.random()<0.04:
            self.spawn_enemy((random.randint(350,550), self.size[1]/2 + random.randint(-50,50)))
        return
        
    def spawn(self):
        self.spawn_enemy((400, self.size[1]/2))
        self.main_base=Base(pos=(50,self.size[1]/2))
        self.add_widget(self.main_base)
        self.add_widget(GunTurret(pos=(150, self.size[1]/2-50), target=self.enemies[0]))
        self.add_widget(GunTurret(pos=(250, self.size[1]/2+80), target=self.enemies[0]))

class TurretApp(App):
    def build(self):
        game = TurretGame()
        game.update(1.0/60.0)
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    try:
        TurretApp().run()
    except:
        errorm(tb.format_exc())































