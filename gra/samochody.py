import pygame
import time
import threading
from datetime import datetime, timedelta
from samochod import Audi,Mercedes,Bmw, wybierz_nastepny

pygame.init()

player_auto = Audi()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
index_glowny = 0

tlo = 'mapa.png'
dotyka = False
time_wlaczony = False
czas_przegrania = None

paliwo = 0
nitro = player_auto.nitro


def timer():
    global czas, dotyka, time_wlaczony
    while True:
        if time_wlaczony:
            time.sleep(1)
            czas += 1


def timer_trigger():
    global czas, dotyka, time_wlaczony
    if screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (255, 174, 201):
        dotyka = True
        time_wlaczony = True
    if screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (163, 73, 164):
        dotyka = False
        time_wlaczony = False


def fuel_consumption():
    global paliwo, index_glowny
    paliwo = player_auto.bak
    while not paliwo == 0:
        paliwo = paliwo - 1
        time.sleep(0.3)
    index_glowny = 6


screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('need for speed wiocha edition')

clock = pygame.time.Clock()
czas = 0

watek = threading.Thread(target=timer)
uzycie_paliwa = threading.Thread(target=fuel_consumption)


def load_image(position, player_auto):
    image = pygame.image.load(player_auto.lista_obrazow[index_glowny])

    surface = image.convert()

    transparent_color = (255, 255, 255)
    surface.set_colorkey(transparent_color)

    rect = surface.get_rect(center=position)

    return [image, surface, rect]


def show_bind():
    global paliwo
    czcionka = pygame.font.SysFont("Arial", 90)
    paliwo = 50

    bindW = czcionka.render("góra: W", True, (255, 255, 255))
    bindS = czcionka.render("dół: S", True, (255, 255, 255))
    bindA = czcionka.render("lewo: A", True, (255, 255, 255))
    bindD = czcionka.render("prawo: D", True, (255, 255, 255))
    bindCTRL = czcionka.render("drift: CTRL", True, (255, 255, 255))
    bindSHIFT = czcionka.render("nitro: SHIFT", True, (255, 255, 255))

    screen_surface.blit(bindW, (SCREEN_WIDTH / 2, 50))
    screen_surface.blit(bindS, (SCREEN_WIDTH / 2, 150))
    screen_surface.blit(bindD, (SCREEN_WIDTH / 2, 250))
    screen_surface.blit(bindA, (SCREEN_WIDTH / 2, 350))
    screen_surface.blit(bindCTRL, (SCREEN_WIDTH / 2, 450))
    screen_surface.blit(bindSHIFT, (SCREEN_WIDTH / 2, 550))


def print_image(img_list) -> None:
    image, surface, rect = img_list
    screen_surface.blit(surface, rect)
    pass


def set_position_image(img_list, position):
    image, surface, rect = img_list
    rect = surface.get_rect(center=position)
    return [image, surface, rect]


def calculate_player_movement(keys):
    global delta_y, delta_x, speed, player_auto, index_glowny, nitro,paliwo
    speed = 0.5
    delta_x = 0
    delta_y = 0


    if keys[pygame.K_SPACE]:
        time.sleep(1)
        player_auto = wybierz_nastepny(player_auto)
        load_image(player_pos, player_auto)

    if not index_glowny == 6:
        if not any(pygame.key.get_pressed()):
            speed = 0
        if keys[pygame.K_a]:
            if keys[pygame.K_LSHIFT] and keys[pygame.K_a]:
                if nitro == 0 or nitro < 0:
                    pass
                else:
                    speed *= player_auto.przyspieszenie
                    nitro = nitro - 0.4
                    index_glowny = 4
                delta_x -= speed * player_auto.przyspieszenie
                index_glowny = 5
            elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:
                speed /= 2
                if nitro == player_auto.nitro:
                    pass
                else:
                    nitro = nitro + 0.2

                delta_x -= speed * player_auto.przyspieszenie
                index_glowny = 3
            else:
                delta_x -= speed * player_auto.przyspieszenie
                index_glowny = 1
        else:
            if index_glowny == 6:
                pass
            if index_glowny == 1:
                index_glowny = 0

        if keys[pygame.K_LSHIFT] and not keys[pygame.K_a]:
            if nitro == 0 or nitro < 0:
                pass
            else:
                speed *= player_auto.przyspieszenie
                nitro = nitro - 0.4
                index_glowny = 4
        if keys[pygame.K_LCTRL] and not keys[pygame.K_a]:
            speed /= 2
            if nitro == player_auto.nitro:
                pass
            else:
                nitro = nitro + 0.2
            index_glowny = 2

        if keys[pygame.K_w]:
            delta_y -= speed * player_auto.przyspieszenie
            index_glowny = 0
        if keys[pygame.K_s]:
            delta_y += speed * player_auto.przyspieszenie
        if keys[pygame.K_d]:
            delta_x += speed * player_auto.przyspieszenie
        if keys[pygame.K_ESCAPE]:
            show_bind()


    else:
        print("samochod ulegl zniszczenmiu przez dziury")
        print("napraw auto r")
        if keys[pygame.K_r]:
            index_glowny = 0
            delta_x += 10
            paliwo += 10
    return [delta_x, delta_y]


def limit(position):
    x, y = position
    x = max(0, min(x, SCREEN_WIDTH))
    y = max(0, min(y, SCREEN_HEIGHT))
    return [x, y]


#_____________________________________________________________________________________#
font = pygame.font.Font(None, 15)
player_pos = [20, 20]
player = load_image(player_pos, player_auto)
game_status = True
watek.start()
uzycie_paliwa.start()

while game_status:

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            game_status = False
        pass

    pressed_keys = pygame.key.get_pressed()
    timer_trigger()
    delta_x, delta_y = calculate_player_movement(pressed_keys)

    player_pos[0] += delta_x
    player_pos[1] += delta_y

    player = load_image(player_pos, player_auto)

    player_pos = limit(player_pos)

    player = set_position_image(player, player_pos)
    time_surface = font.render(f"czas: {czas}", True, (255, 255, 255))
    speed_surface = font.render(f"predkosc: {int(speed * player_auto.przyspieszenie * 10)} km/h", True, (255, 255, 255))
    fuel_surface = font.render(f"paliwo: {int(paliwo)}L", True, (255, 255, 255))
    nitro_surface = font.render(f"nitro : {int(nitro)}", True, (255, 255, 255))

    screen_surface.blit(time_surface, (SCREEN_WIDTH - 50, 200))
    screen_surface.blit(speed_surface, (SCREEN_WIDTH - 100, 50))

    screen_surface.blit(fuel_surface, (SCREEN_WIDTH - 75, 150))
    screen_surface.blit(nitro_surface, (SCREEN_WIDTH -50, 100))

    info_surface = font.render("przypisane przyciski: ESC", True, (255, 255, 255))
    screen_surface.blit(info_surface, (100, 100))

    print_image(player)

    pygame.display.update()

    if czas_przegrania is not None:
        czas_przegrania_tlo = czas_przegrania + timedelta(seconds=2)
        if datetime.now() > czas_przegrania_tlo:
            tlo = 'mapa.png'
            paliwo = player_auto.bak
            nitro = player_auto.nitro
            player_pos = [20, 20]
            czas_przegrania = None

    background = [121, 121, 121]
    background_image = pygame.image.load(tlo)

    if screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (34, 177, 76):
        print("przegrales")
        if czas_przegrania is None:
            tlo = 'przegrana.png'
            czas_przegrania = datetime.now()
            pass


    if screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (163, 73, 164) and tlo == 'mapa2.png':
        print("wygrales")
        tlo = ('wygrana.png')
    elif screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (163, 73, 164):
        player_pos = [20,40]
        paliwo = player_auto.bak
        nitro = player_auto.nitro
        print("wygrales")
        tlo = ('mapa2.png')

    if screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (136, 0, 21):
        paliwo = player_auto.bak

    if screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (54, 35, 25) or screen_surface.get_at((int(player_pos[0]), int(player_pos[1])))[:3] == (255, 127, 39):
        index_glowny = 6


    screen_surface.blit(background_image, (0, 0))

    clock.tick(60)
    pass

print("Zamykanie aplikacji")
pygame.quit()
quit()
