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
from math import sqrt

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
    coolcycle = 1.0
    target = ObjectProperty()
    
    def __init__(self, **args):
        super(GunTurret, self).__init__(**args)
        self.cooldown = self.coolcycle
        
    def update(self, dt):
        self.cooldown -= dt
        if(self.cooldown<0):
            self.cooldown = self.coolcycle
            self.shoot()
    
        for c in self.children:
            c.update(dt)
            
    def shoot(self):
        self.add_widget(Bullet(pos=self.center, target=self.target))
        pass
            
class Bullet(Widget):
    speed=150.0
    
    def __init__(self, **args):
        super(Bullet, self).__init__(**args)
        self.target = args["target"]
        print self.target.center
    
    def update(self, dt):
        tpos = self.target.pos
        dv = [tpos[0] - self.pos[0], tpos[1] - self.pos[1]]
        norm = sqrt(float(dv[0]*dv[0]+dv[1]*dv[1]))
        dv[0] /= norm
        dv[1] /= norm
        self.pos = Vector(dv[0]*self.speed*dt, dv[1]*self.speed*dt) + self.pos
        

class Base(Widget):
    d = NumericProperty()
    
    def __init__(self, **args):
        super(Base, self).__init__(**args)

class SquareEnemy(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    life = NumericProperty()
    speed = 20
    
    def __init__(self, **args):
        super(SquareEnemy, self).__init__(**args)
        
    def update(self, dt):
        self.pos = Vector(-1, 0)*dt*self.speed + self.pos
        

class TurretGame(Widget):
    main_base = ObjectProperty(None)
    deblog = ObjectProperty(None)
    life = NumericProperty()
    firstresize=True
    enemies=list()

    def spawn_enemy(self):
        e=SquareEnemy(pos=(400, self.size[1]/2))
        self.enemies.append(e)
        self.add_widget(e)
    
    def update(self, dt):
        if self.size!=[100,100] and self.firstresize:
            self.deblog.text=str(self.size)
            self.firstresize = False
            self.spawn()
            
        for c in self.children:
            try:
                c.update(dt)
            except:
                pass
        return
        
    def spawn(self):
        self.spawn_enemy()
        self.main_base=Base(pos=(50,self.size[1]/2))
        self.add_widget(self.main_base)
        self.add_widget(GunTurret(pos=(150, self.size[1]/2-50), target=self.enemies[0]))

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































