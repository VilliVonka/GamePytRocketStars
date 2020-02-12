import random
import turtle
import math

#настраиваем всё окно
window = turtle.Screen()

window.screensize(900,660)
window.bgpic("tumblr.png")
#подбираем размер оптимального рабочего окна
window.setup(width=1100, height=700, startx=None, starty=None)

#изза медлительности летания ракет, увеличиваем отрисовку кадров
window.tracer(n=2)

ENEMY_CONST = 5



#множественное присвоение координат базы
BASE_X, BASE_Y = 0, -300
#координаты полета ракеты
#def calc_heading(x1, y1, x2, y2):
 #   dx = x2 - x1
 #   dy = y2 - y1
 #   lenght = (dx ** 2 + dy ** 2 ) ** 0.5
 #   cos_alpha = dx / lenght
 #   alpha = math.acos(cos_alpha)
#    alpha = math.degrees(alpha)
 #   if dy <0:
 #       alpha = -alpha
 #   return alpha


def create_missile(color, x, y, x2, y2):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color(color)
    missile.penup()
    missile.setpos(x=x, y=y)
    missile.pendown()
    #ракета летит из базы в координаты x,y в которые обознач мышкой
    heading = missile.towards(x2, y2)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x2, y2], 'state': 'launched', 'radius': 0 }
    return info



#наша ракета
def fire_missile(x, y):

    info = create_missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)

def fire_enemy_missile():

    x = random.randint(-600, 600)
    y = 400
    info = create_missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)



def move_missiles(missiles):
    for info in missiles:
        state = info['state']
        missile = info['missile']
        #если летит то двигаем на 4 пикселя вычисляем таргет
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            #если долетела до цели, попала в таргет, то бабах
            if missile.distance(x=target[0], y=target[1]) < 20:
                info['state'] = 'explode'
                missile.shape('circle')
        #если бабах то радиус увличиваем
        elif state == 'explode':
            info['radius'] += 1
            if info['radius'] > 5:
                missile.clear()
                missile.hideturtle()
                info['state'] = 'dead'
            else:
                missile.shapesize(info['radius'])
        elif state == 'dead':
            missile.clear()
            missile.hideturtle()


    #чиистим мертвые ракеты списковая сборка
    dead_missiles = [info for info in missiles if info['state']=='dead']
    #удаляем из списка
    for dead in dead_missiles:
        missiles.remove(dead)

def check_enemy_count():
    if len(enemy_missiles) < ENEMY_CONST:
        fire_enemy_missile()


#проверка перехватов ракет
def check_interceptions():
    #проверяем свою ракету
    for our_info in our_missiles:
        if our_info['state'] != 'explode':
            continue
        our_missile = our_info['missile']
        #проверяем вражеские ракеты
        for enemy_info in enemy_missiles:
            enemy_missile = enemy_info['missile']
            #если вражеская ракета находится рядом с нашей во время взрыва
            if enemy_missile.distance(our_missile.xcor(), our_missile.ycor()) < our_info['radius'] * 7:
                enemy_info['state'] = 'dead'
#определяем  событие пользователя
window.onclick(fire_missile)


#создаем список ракет
our_missiles = []
enemy_missiles = []

base = turtle.Turtle(visible=True)
base.speed(0)
base.penup()
base.setpos(x=BASE_X, y=BASE_Y)
#pic_path = os.path.join(BASE_PATH, "base.png")
#window.register_shape(pic_path)
#bace.shape(pic_path)

base_health = 2000

#организуем бесконечный цикл
def game_over():
    return base_health < 0


def check_impact():
    global base_health
    for enemy_info in enemy_missiles:
        if enemy_info['state'] != 'explode':
            continue
        enemy_missile = enemy_info['missile']
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_info['radius'] * 10:
            base_health -= 100


while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()

    check_interceptions()

    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)






