import pygame, random, spritesheet
pygame.init()

pygame.display.set_caption("Typing Game")
screen = pygame.display.set_mode((900, 500))

bg = pygame.image.load("assets/wallpaper.png")
bg_alt = pygame.image.load("assets/wallpaper_alt.png")
heart = pygame.transform.scale(pygame.image.load("assets/heart.png"), (40, 40))

spritesheet_img = pygame.image.load("assets/necromancer.png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(spritesheet_img)

font = pygame.font.Font("assets/MatchupPro.otf", 50)
big_font = pygame.font.Font("assets/MatchupPro.otf", 80)
small_font = pygame.font.Font("assets/MatchupPro.otf", 40)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 128, 0)

life = 3
meter = 0
lines = open("words.txt").read().splitlines()
next_word = random.choice(lines)

# def options():
    
# def score():

def new_word():
    global next_word, pressed_word, lines, text, text_rect, count, count_rect, active_word
    pressed_word = ""
    active_word = next_word
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

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    waiting = False
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
    new_word()

main_menu()

# animations
necro_idle_list = []
necro_idle_frames = 8
update = pygame.time.get_ticks()
animation_cd = 250
frames = 0

for frame in range (necro_idle_frames):
    necro_idle_list.append(sprite_sheet.get_image(frame, 160, 128, 3, black))

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
            else:
                pressed_word = ""
                life -= 1
    
    screen.blit(bg_alt, (0, 0))

    current_time = pygame.time.get_ticks()

    if current_time - update >= animation_cd:
        frames += 1
        update = current_time
        if frames >= len(necro_idle_list):
            frames = 0

    screen.blit(necro_idle_list[frames], (-150, 100))

    for hearts in range(life):
        screen.blit(heart, (20 + hearts * 50, 20))
    
    next_surface = small_font.render(next_word, True, white)
    next_rect = next_surface.get_rect()
    next_rect.center = (screen.get_width() // 2, 200)
    screen.blit(next_surface, next_rect)
    for i, letter in enumerate(active_word):
        if i < len(pressed_word):
            color = green
        else:
            color = white
        letter_surface = small_font.render(letter, True, color)
        letter_rect = letter_surface.get_rect()
        letter_rect.center = (screen.get_width() // 2 - len(active_word) * 7.5 + i * 17, screen.get_height() // 2)
        screen.blit(letter_surface, letter_rect)
    if life == 0:
        main_menu()
    count_rect.center = (screen.get_width() // 1.05, 25)
    screen.blit(count,count_rect)

    pygame.display.update()

    clock.tick(60)