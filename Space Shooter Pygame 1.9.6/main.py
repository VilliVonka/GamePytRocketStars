import pygame , os, time, random, sys
pygame.font.init()

#work display
WIDTH = 750
HEIGHT = 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Pygame")

#load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))

#player lasers
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

#parent of all laser
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # draw on coordinat
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    # return laser off work space (count)
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    #time in second then collide (determine the value(int))
    def collision(self, obj):
        return collide(self, obj)

#parent of all ships
class Ship:
    COOLDOWN = 30 #30ml.second (FPS 60sec)

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    #draw on coordinat
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        # use method draw for each laser
        for laser in self.lasers:
            laser.draw(window)

    #check then move obj lasers when collision whith all objs
    def move_lasers(self, vel, obj):
        #shooting lasers at cooldown
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    #check recharch shoot
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            #recharge counter
            self.cool_down_counter = 1

    #get width and height for impossible outside border play area
    def get_width(self):
        return self.ship_img.get_width()

    #starting from the coordinates
    def get_heigh(self):
        return self.ship_img.get_height()

#player
class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        #shooting lasers at cooldown
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                #collision with each obj
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

#draw healthbar 
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):

        pygame.draw.rect(window, (255,0,0), (self.x, self.y +
        self.ship_img.get_height() + 10, self.ship_img.get_width(), 10 ))

        pygame.draw.rect(window, (0,255,0), (self.x, self.y +
        self.ship_img.get_height() + 10, self.ship_img.get_width() * 
        (self.health/self.max_health), 10 ))

#enemy ship
class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            #recharge counter
            self.cool_down_counter = 1

#collade 2 obj, mask method (return intersection of two masks)
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 70)

    enemies = []
    wave_length = 5 #count of enemies at the same time

    enemy_vel = 1 #speed enemy (pixels)
    player_vel = 5 #speed player (pixels)
    laser_vel = 6 #speed laser (pixels)

    player = Player(350, 600)

    clock = pygame.time.Clock()

    lost = False    #dead time Player
    lost_count = 0  #time message show lost before reset game

    def redraw_window():
        WIN.blit(BG, (0,0))
        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        #coordinate text
        WIN.blit(lives_label, (0,10))
        WIN.blit(level_label, (150,10))

        player.draw(WIN)

        #use method draw for each enemies
        for enemy in enemies:
            enemy.draw(WIN)

        #draw lost
        if lost:
            lost_label = lost_font.render("You Lost!!!",1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    #start game process
    while run:
        clock.tick(FPS)
        redraw_window()

        #define the properties of a variable lost and lost_count
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        # show 3 second message LOST
        if lost:
            if lost_count > FPS * 5:
                #game over
                run = False
            else:
                continue

        #optimize enemies part1
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            #determine enemies and he's position in non work space (spawn enemies)
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1000,-100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        #exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        #player flight control
        keys = pygame.key.get_pressed()
        if  keys[pygame.K_a] and player.x - player_vel > -15: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: #right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > -15:  #up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_heigh() + 15 < HEIGHT:  #down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # optimize enemies part2
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            #random shooting every 2 second
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            #shooting damage
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            #Departure of the ship beyond the working area
            elif enemy.y + enemy.get_heigh() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

#main menu
def main_menu():
    #declare the text in the menu
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        #designated text properties
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()

