#Создай собственный Шутер!

from pygame import *
from random import randint
#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()
font1 = font.SysFont("Arial",80)
win = font1.render('YOU WIN!', True,( 255,255,255))
lose = font1.render('YOU LOSE!', True,(180,0,0))

font2 = font.SysFont('Arial', 36)

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, width,height,player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение

        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.width=width
        self.height=height
        # каждый спрайт должен хранить свойство rect - прямоугол
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet=Bullet("bullet.png",self.rect.centerx-7,self.rect.top,15,20,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y+=self.speed
        if self.rect.y>500:
            self.rect.x=randint(60,650)
            self.rect.y=00
            lost+=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<0:
            self.kill()


ship = Player("rocket.png",350,400,80,100,10)
monsters = sprite.Group()
for i in range(5):
    monster=Enemy("ufo.png", randint(60,650),0, 80,50,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
score = 0
lost  = 0
while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                ship.fire()
    if finish != True:
        window.blit(background,(0,0))
        text=font2.render("Счет: "+ str(score),True,(255,255,255))
        window.blit(text, (20,20))
        text1=font2.render("Пропущено: "+ str(lost),True,(255,255,255))
        window.blit(text1, (20,50))
        ship.reset()
        ship.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for monster in collides:
            monster=Enemy("ufo.png",randint(60,650),0,80,50,randint(1,5))
            monsters.add(monster)
            score = score + 1
            print(score)
        sprite_list=sprite.spritecollide(ship, monsters, False)
        if sprite_list:
            finish=True
            window.blit(lose, (200,200))
        if score==10:
            finish=True
            window.blit(win, (200,200))

    display.update()
    time.delay(60)