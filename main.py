import kivy
kivy.require('1.1.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class LaserTurret(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    
    def __init__(self, **args):
        super(LaserTurret, self).__init__(**args)
        
class GunTurret(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    
    def __init__(self, **args):
        super(GunTurret, self).__init__(**args)

class Base(Widget):
    d = NumericProperty()
    
    def __init__(self, **args):
        super(Base, self).__init__(**args)


class SquareEnemy(Widget):
    d = NumericProperty()
    orient = NumericProperty()
    life = NumericProperty()
    
    def __init__(self, **args):
        super(SquareEnemy, self).__init__(**args)
        

class TurretGame(Widget):
    main_base = ObjectProperty(None)
    life = NumericProperty()

    def spawn_enemy(self):
        self.add_widget(SquareEnemy(pos=(400, self.size[1]/2)))
    
    def update(self, dt):
        return

class TurretApp(App):
    def build(self):
        game = TurretGame()
        game.update(1.0/60.0)
        game.spawn_enemy()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    TurretApp().run()
