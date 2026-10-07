from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class MafiaUI(Widget):
    pass

class Player:
    def __init__(self):
        self.id = 0
        print(f"Player {self.id} is created")

class Time:
    def __init__(self):
        self.period = 0
        print(f"Game time {times[self.period]} is initialized")

class MafiaApp(App):
    def build(self):
        return MafiaUI()

times = {0: "day", 1: "night"}

if __name__ == '__main__':
     time = Time()
     player = Player()
     GameApp = MafiaApp
     GameApp().run()


