import math
import turtle

#настраиваем всё окно
window = turtle.Screen()

window.screensize(900,660)
window.bgpic("tumblr.png")
#подбираем размер оптимального рабочего окна
window.setup(width=1100, height=700, startx=None, starty=None)

#изза медлительности летания ракет, увеличиваем отрисовку кадров
#window.tracer(n=2)

#множественное присвоение координат базы
BASE_X, BASE_Y = 0, -300
#координаты полета ракеты
def calc_heading(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    lenght = (dx ** 2 + dy ** 2 ) ** 0.5
    cos_alpha = dx / lenght
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy <0:
        alpha = -alpha
    return alpha


#наша ракета
def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('white')
    missile.penup()
    missile.setpos( x = BASE_X, y = BASE_Y)
    missile.pendown()
    #ракета летит из базы в координаты x,y в которые обознач мышкой
    heading = calc_heading(x1 = BASE_X, y1 = BASE_Y, x2 = x, y2 = y)
    missile.setheading(heading)
    missile.showturtle()
    our_missiles.append(missile)
    our_missiles_target.append([x, y])
 #   missile.forward(500)
 #   missile.shape('circle')
  #  missile.shapesize(0.5)
  #  missile.shapesize(1)
  #  missile.shapesize(1.5)
  #  missile.shapesize(2)
  #  missile.clear()
  #  missile.hideturtle()

#fire_missile()

#определяем  событие пользователя
window.onclick(fire_missile)


pen = turtle.Turtle()
pen.shape('turtle')

#создаем список ракет
our_missiles = []
#сохраняем таргет куда летит ракета
our_missiles_target = []

#организуем бесконечный цикл
while True:
    window.update()

    for num, missile in enumerate(our_missiles):
        missile.forward(4)
        target = our_missiles_target[num]
        #в тот момент когда она пролетает мимо своей цели
        if missile.distance(x=target[0], y=target[1]) < 20:
            missile.shape('circle')
            missile.shapesize(0.5)
            missile.shapesize(1)
            missile.shapesize(1.5)
            missile.shapesize(2)
            missile.clear()
