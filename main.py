import pygame
import random
import spritesheet
pygame.init()

pygame.display.set_caption("Typing Game")
screen = pygame.display.set_mode((900, 500))

bg = pygame.image.load("assets/wallpaper.png")
bg_alt = pygame.image.load("assets/wallpaper_alt.png")
heart = pygame.transform.scale(pygame.image.load("assets/heart.png"), (40, 40))
small_heart = pygame.transform.scale(heart, (20, 20))

spritesheet_img = pygame.image.load("assets/necromancer.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(spritesheet_img)
ghost_img = pygame.image.load("assets/ghost-idle.png").convert_alpha()
ghost_sheet = spritesheet.SpriteSheet(ghost_img)

font = pygame.font.Font("assets/MatchupPro.otf", 50)
big_font = pygame.font.Font("assets/MatchupPro.otf", 80)
small_font = pygame.font.Font("assets/MatchupPro.otf", 40)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (21, 21, 47)

life = 5
meter = 0
lines = open("words.txt").read().splitlines()
short_list = [word for word in lines if len(word) < 6]
long_list = [word for word in lines if len(word) > 4]
monster_cd = 0
monster_life = 100
loading_bar = pygame.image.load("assets/loading-bar.png")
loading_bar_rect = loading_bar.get_rect(midleft=(280, 360))

def options():
    global life, difficulty, next_word
    screen.blit(bg, (0, 0))

    easy_text = big_font.render("EASY", True, white)
    easy_rect = easy_text.get_rect()
    easy_rect.center = (screen.get_width() // 2, screen.get_height() // 3)
    screen.blit(easy_text, easy_rect)

    normal_text = big_font.render("NORMAL", True, white)
    normal_rect = normal_text.get_rect()
    normal_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(normal_text, normal_rect)

    hard_text = big_font.render("HARD", True, white)
    hard_rect = hard_text.get_rect()
    hard_rect.center = (screen.get_width() // 2, screen.get_height() // 1.5)
    screen.blit(hard_text, hard_rect)

    pygame.display.update()

    options = True
    while options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):
                    life = 5
                    difficulty = 12
                    next_word = random.choice(short_list)
                    print(short_list)
                    options = False
                if normal_rect.collidepoint(mouse_pos):
                    life = 4
                    difficulty = 10
                    next_word = random.choice(lines)
                    options = False
                if hard_rect.collidepoint(mouse_pos):
                    life = 3
                    difficulty = 8
                    next_word = random.choice(long_list)
                    options = False
    new_word()
    monster()

# def score():


def monster():
    global monster_life, monster_cd, monster_maxpv, loading_bar_width
    monster_life = random.randint(3, 5)
    monster_maxpv = monster_life
    print("vie : ", monster_maxpv)
    monster_cd = 0
    loading_bar_width = 900


def new_word():
    global next_word, pressed_word, lines, text, text_rect, count, count_rect, active_word
    pressed_word = ""
    active_word = next_word
    if difficulty == 12:
        next_word = random.choice(short_list)
    elif difficulty == 8:
        next_word = random.choice(long_list)
    else:
        next_word = random.choice(lines)
    text = font.render(next_word, True, white)
    text_rect = text.get_rect()
    count = font.render(str(meter), True, white)
    count_rect = count.get_rect()


def main_menu():
    global life
    screen.blit(bg, (0, 0))

    play_text = big_font.render("PLAY", True, white)
    play_rect = play_text.get_rect()
    play_rect.center = (screen.get_width() // 3, screen.get_height() // 1.5)
    screen.blit(play_text, play_rect)

    quit_text = big_font.render("QUIT", True, white)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (screen.get_width() // 1.5, screen.get_height() // 1.5)
    screen.blit(quit_text, quit_rect)

    pygame.display.update()

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    menu = False
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
    options()


main_menu()

# animations
necro_idle_list = []
ghost_idle_list = []
update = pygame.time.get_ticks()
animation_cd = 250
frames = 0

for frame in range(0, 8):
    necro_idle_list.append(sprite_sheet.get_image(frame, 160, 128, 3, black))
for frame in range(0, 7):
    ghost_idle_list.append(ghost_sheet.get_image(frame, 64, 80, 3, black))

clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            typed_key = pygame.key.name(event.key)
            if typed_key == active_word[len(pressed_word)]:
                pressed_word += typed_key
                if active_word == pressed_word:
                    meter += len(active_word)
                    new_word()
                    monster_life -= 1
            else:
                pressed_word = ""

    screen.blit(bg_alt, (0, 0))

    current_time = pygame.time.get_ticks()

    if current_time - update >= animation_cd:
        frames += 1
        loading_bar_width -= 900 / (monster_maxpv * difficulty)
        monster_cd += 1
        update = current_time
        print(monster_cd, monster_life)
        if frames >= 7:
            frames = 0
        if monster_cd == monster_maxpv * difficulty:
            life -= 1
            monster()
        if monster_life == 0:
            meter += monster_maxpv * (20 - difficulty)
            print("KILL")
            monster()

    screen.blit(necro_idle_list[frames], (-150, 100))
    screen.blit(ghost_idle_list[frames], (650, 230))

    loading_bar = pygame.transform.scale(
        loading_bar, (int(loading_bar_width), 150))
    loading_bar_rect = loading_bar.get_rect(midleft=(0, 550))
    screen.blit(loading_bar, loading_bar_rect)

    for hearts in range(life):
        screen.blit(heart, (20 + hearts * 50, 20))

    for hearts in range(monster_life):
        screen.blit(small_heart, (screen.get_width() // 1.19 -
                    monster_maxpv * 15 + hearts * 25, 260))

    next_surface = small_font.render(next_word, True, white)
    next_rect = next_surface.get_rect()
    next_rect.center = (screen.get_width() // 2, 200)
    screen.blit(next_surface, next_rect)
    for i, letter in enumerate(active_word):
        if i < len(pressed_word):
            color = blue
        else:
            color = white
        letter_surface = big_font.render(letter, True, color)
        letter_rect = letter_surface.get_rect()
        letter_rect.center = (screen.get_width(
        ) // 2 - len(active_word) * 14 + i * 34, screen.get_height() // 2)
        screen.blit(letter_surface, letter_rect)
    if life == 0:
        main_menu()
        life = 10
    count_rect.center = (screen.get_width() // 1.05, 25)
    screen.blit(count, count_rect)

    pygame.display.update()

    clock.tick(60)
