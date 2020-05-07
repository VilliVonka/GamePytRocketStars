#игра написана на скорость: 1.5 - 2 часа

import turtle
from random import randint

'''частоту кадров необходимо увеличить до 2х потому что будет слишком медленно
по другому не фиксится, в window.setup делаем полноэкранный режим'''
window = turtle.Screen()
window.title('Ping-Pong')
window.setup(width=1.0,height=1.0)
window.bgcolor('red')
window.tracer(2)


'''рисуем поле'''
border = turtle.Turtle()
border.speed(0)
border.color('green')
border.begin_fill()
border.goto(-500,300)
border.goto(500,300)
border.goto(500,-300)
border.goto(-500,-300)
border.goto(-500,300)
border.end_fill()

'''сплошную пингпонговкую сетку, не строчную ибо увеличиться количество отрисовки
кадров и в без того страдающей зацикливанием игры'''
border.goto(0, 300)
border.color('white')
border.goto(0, -300)
border.hideturtle()

'''Добавляем белую ракетку'''
rosket_a = turtle.Turtle()
rosket_a.color('white')
rosket_a.shape('square')
rosket_a.shapesize(5, 1)
rosket_a.up()
rosket_a.goto(-470, 0)

'''выводим счет очков'''
FONT = ("Arial", 44)
score_a = 0
s1 = turtle.Turtle(visible=False)
s1.color('white')
s1.up()
s1.setposition(-190, 300)
s1.write(score_a, font=FONT)
score_b = 0
s2 = turtle.Turtle(visible = False)
s2.color('white')
s2.up()
s2.setposition(190, 300)
s2.write(score_a, font=FONT)

'''т.к двигаемся только по y, пишем функцию движения белой рокетки'''
def move_up():
    y = rosket_a.ycor()
    if y > 230:
        y = 230
    rosket_a.sety(y+22)


def move_down():
    y = rosket_a.ycor()
    if y < -230:
        y = -230
    rosket_a.sety(y-22)

'''создаем синюю рокетку'''
rosket_b = turtle.Turtle()
rosket_b.color('blue')
rosket_b.shape('square')
rosket_b.shapesize(5, 1)
rosket_b.up()
rosket_b.goto(470, 0)

'''т.к двигаемся только по y, пишем функцию движения синей рокетки'''
def move_up_b():
    y = rosket_b.ycor()
    if y > 230:
        y = 230
    rosket_b.sety(y+22)


def move_down_b():
    y = rosket_b.ycor()
    if y < -230:
        y = -230
    rosket_b.sety(y-22)

'''создаем мячик, ball.dx,ball.dy изменяем его траекторию движения'''
ball = turtle.Turtle()
ball.speed(1)
ball.shape('circle')
ball.color('black')
ball.dx = 1
ball.dy = 1
ball.up()

'''собираем ключевые события которые передаются игре'''
window.listen()
window.onkeypress(move_up, "w")
window.onkeypress(move_down, "s")
window.onkeypress(move_up_b, "o")
window.onkeypress(move_down_b, "l")

'''по сути бесконечный цикл'''
while True:
    '''постоянная отрисовка кадров конфликтует с методом clear(), если применять
    их одновременно будут отваливаться клавиши, выбираем из двух зол меньшее'''
    #window.update()
    '''скорость по x и по y'''
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    '''границы поля'''
    if ball.ycor() >= 290:
        ball.dy = -ball.dy
    if ball.ycor() <= -290:
        ball.dy = -ball.dy
    '''передвигаем мяч после пересечения x, и чекаем счет '''
    if ball.xcor() >= 490:
        ball.goto(0, randint(-250, 250))
        score_b += 1
        s2.clear()
        s2.write(score_b, font=FONT)
    if ball.xcor() <= -490:
        ball.goto(0, randint(-250, 250))
        score_a += 1
        s1.clear()
        s1.write(score_a, font=FONT)

    '''пересечение мячика с ракеткой'''
    if ball.ycor() >= rosket_b.ycor() - 50 and ball.ycor() <= rosket_b.ycor() + 50 \
        and ball.xcor() >= rosket_b.xcor() - 5 and ball.xcor() <= rosket_b.xcor() + 5:
        ball.dx = -ball.dx
    if ball.ycor() >= rosket_a.ycor() - 50 and ball.ycor() <= rosket_a.ycor() + 50 \
        and ball.xcor() >= rosket_a.xcor() - 5 and ball.xcor() <= rosket_a.xcor() + 5:
        ball.dx = -ball.dx


turtle.done()