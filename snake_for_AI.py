import turtle
import time
import random
import os.path
import math

class snake:

    def __init__(self, delay):

        self.delay = delay
        self.wn = turtle.Screen()
        self.head = turtle.Turtle()
        self.food = turtle.Turtle()
        self.new_segment = turtle.Turtle()
        self.notification = turtle.Turtle()
        self.stats = turtle.Turtle()
        self.stats.hideturtle()
        self.score = 0
        self.segments = []
        self.body = False
        self.notification.hideturtle()
        self.head_to_body_mean = []
        self.head_to_food = []
        self.head_to_borders = []

    def window_box(self):

        self.wn.title("Snake ML")
        self.wn.bgcolor("midnight blue")
        self.wn.setup(width = 600, height = 600)
        self.wn.tracer(0)

    def make_head(self):

        self.head.speed(0)
        self.head.shape("square")
        self.head.color("firebrick")
        self.head.penup()
        self.head.goto(0,0)
        self.head.direction = "stop"

    def make_food(self):

        self.food.speed(0)
        self.food.shape("turtle")
        self.food.color("sea green")
        self.food.penup()
        self.food.goto((random.randint(-280,280)//20) * 20, (random.randint(-280,280)//20) * 20)

    def up(self):

        if self.head.direction != "down":
            self.head.direction = "up"

    def left(self):

        if self.head.direction != "right":
            self.head.direction = "left"

    def right(self):

        if self.head.direction != "left":
            self.head.direction = "right"

    def down(self):

        if self.head.direction != "up":
            self.head.direction = "down"

    def end_game(self):
        self.wn.bye()

    def keyboard_bindings(self):

        self.wn.listen()
        self.wn.onkeypress(self.up, "Up")
        self.wn.onkeypress(self.left, "Left")
        self.wn.onkeypress(self.down, "Down")
        self.wn.onkeypress(self.right, "Right")
        self.wn.onkeypress(self.end_game, "q")

    def move(self):

        y = self.head.ycor()
        x = self.head.xcor()

        if self.head.direction ==  "up":
            self.head.sety(y + 20)

        if self.head.direction ==  "left":
            self.head.setx(x - 20)

        if self.head.direction ==  "right":
            self.head.setx(x + 20)

        if self.head.direction ==  "down":
            self.head.sety(y - 20)

    def eat(self):

        if (self.head.ycor() == self.food.ycor()) and (self.head.xcor() == self.food.xcor()):
            self.body = True
            self.make_food()
            self.new_body()
            self.score += 1
            self.score_print()

    def new_body(self):

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape('square')
        new_segment.color("maroon")
        new_segment.penup()
        self.segments.append(new_segment)

    def update_body(self, head_position):

        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        if len(self.segments) > 0:
            x = head_position[0]
            y = head_position[1]
            self.segments[0].goto(x, y)

    def game_over(self):

        self.notification.hideturtle()
        self.notification.color("red")
        arg = "GAME OVER"
        self.notification.write(arg, move=False, align="center", font=("Impact", 45, "bold"))
        time.sleep(1)
        self.notification.clear()
        for each in self.segments:
            each.hideturtle()
        self.head.goto(0,0)
        self.segments.clear()
        self.food.clear()
        self.head.direction = "stop"
        self.score = 0
        self.score_print()
        self.body = False

    def border_collision(self):

        if (self.head.xcor() >= 300) or (self.head.xcor() <= -300) or (self.head.ycor() >= 300) or (self.head.ycor() <= -300):
            self.game_over()

    def score_print(self):

        self.stats.color("white")
        self.stats.hideturtle()
        self.stats.clear()
        self.stats.setpos(250,250)
        self.stats.hideturtle()
        self.stats.clear()
        arg = "Score: " + str(self.score)
        self.stats.write(arg, move=False, align="right", font=("Arial", 14, "normal"))

    def distance_calculations(self):

        def head_to_borders():

            self.head_to_borders.clear()
            d_head_borders = []
            d_head_borders.clear()
            d_head_borders_all = [-(self.head.xcor() - 300), -(self.head.xcor() + 300), -(self.head.ycor() - 300), -(self.head.ycor() + 300)]

            if self.head.ycor() < 0:
                d_y_border = d_head_borders_all[3]
            if self.head.ycor() >= 0:
                d_y_border = d_head_borders_all[2]

            if self.head.xcor() < 0:
                d_x_border = d_head_borders_all[1]
            if self.head.xcor() >= 0:
                d_x_border = d_head_borders_all[0]
            
            self.head_to_borders = [d_x_border, d_y_border]

        def head_to_body():

            d_x_vec = []
            d_y_vec = []
            d_x_vec.clear()
            d_y_vec.clear()

            for each in self.segments:
                d_x = each.xcor() - self.head.xcor()
                d_y = each.ycor() - self.head.ycor()
                d_x_vec.append(d_x)
                d_y_vec.append(d_y)
            self.head_to_body_mean = [sum(d_x_vec) / len(d_x_vec), sum(d_y_vec) / len(d_y_vec)]

        def head_to_food():

            self.head_to_food.clear()
            d_x = self.food.xcor() - self.head.xcor()
            d_y = self.food.ycor() - self.head.ycor()
            self.head_to_food = [d_x, d_y]

        head_to_borders()
        if self.body == True:
            head_to_body()
        head_to_food()

    def body_collision(self):

        for each in self.segments:
            distance = each.distance(self.head)
            if distance == 0:
                self.game_over()

    def mainloop(self):

        self.window_box()
        self.make_head()
        self.make_food()
        self.score_print()

        while True:
            
            self.keyboard_bindings()
            self.move()
            self.border_collision()
            self.body_collision()
            self.eat()

            if self.body == True:
                self.update_body(head_position)
            
            self.distance_calculations()
            self.wn.update()
            head_position = [self.head.xcor(), self.head.ycor()]
            time.sleep(self.delay)

# To run manually
delay = 0.1     # Adjusts the screen update frequency
foo = snake(delay)
foo.mainloop()