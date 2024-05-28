from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Constants
WIDTH = 800
HEIGHT = 600
BALL_SPEED = 5
PADDLE_SPEED = 10
PADDLE_WIDTH = 100

class PongGame(Widget):
    
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        
        self.ball = Ellipse(pos=(WIDTH/2, HEIGHT/2), size=(20, 20))
        self.player_paddle = Rectangle(pos=(WIDTH/2, 20), size=(PADDLE_WIDTH, 20))
        self.opponent_paddle = Rectangle(pos=(WIDTH/2, HEIGHT-40), size=(PADDLE_WIDTH, 20))
        
        self.ball_speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
        self.ball_speed_y = BALL_SPEED
        
        self.player_score = 0
        self.opponent_score = 0
        
        self.goal_scored = False
        self.goal_time = 0

        self.start_counter = 60

        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        if not self.goal_scored:
            self.ball.pos = (self.ball.pos[0] + self.ball_speed_x, self.ball.pos[1] + self.ball_speed_y)

            if self.ball.pos[0] <= 0 or self.ball.pos[0] + 20 >= WIDTH:
                self.ball_speed_x = -self.ball_speed_x
            if self.ball.collide_widget(self.player_paddle) or self.ball.collide_widget(self.opponent_paddle):
                self.ball_speed_y = -self.ball_speed_y
                
            if self.ball.pos[1] <= 0:
                self.player_score += 1
                self.goal_scored = True
                self.goal_time = Clock.get_time()

                self.ball_speed_y = BALL_SPEED
                self.ball.pos = (WIDTH/2, HEIGHT/2)
            elif self.ball.pos[1] + 20 >= HEIGHT:
                self.opponent_score += 1
                self.goal_scored = True
                self.goal_time = Clock.get_time()
                
                self.ball_speed_y = -BALL_SPEED
                self.ball.pos = (WIDTH/2, HEIGHT/2)

        else:
            if Clock.get_time() - self.goal_time >= 1:
                self.ball.pos = (WIDTH/2, HEIGHT/2)
                self.ball_speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
                self.ball_speed_y = BALL_SPEED
                self.goal_scored = False

    def on_touch_move(self, touch):
        if touch.y < HEIGHT/2:
            self.player_paddle.pos = (touch.x - PADDLE_WIDTH/2, 20)

    def draw(self):
        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=self.player_paddle.pos, size=self.player_paddle.size)
            Rectangle(pos=self.opponent_paddle.pos, size=self.opponent_paddle.size)
            Ellipse(pos=self.ball.pos, size=self.ball.size)
            
    def on_size(self, *args):
        pass
    
class PongApp(App):
    
    def build(self):
        game = PongGame()
        Window.size = (WIDTH, HEIGHT)
        return game

if __name__ == '__main__':
    PongApp().run()