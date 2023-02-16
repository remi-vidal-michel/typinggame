import pygame, random

pygame.init()

pygame.display.set_caption("Typing Game")
screen = pygame.display.set_mode((480, 720))

bg = pygame.image.load("assets/wallpaper_alt.png")
bg_alt = pygame.image.load("assets/wallpaper.png")
heart = pygame.transform.scale(pygame.image.load("assets/heart.png"), (50, 50))


font = pygame.font.Font("assets/MatchupPro.otf", 66)
white = (255, 255, 255)
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
    title_text = font.render("TYPING GAME", True, white)
    title_rect = title_text.get_rect()
    title_rect.center = (screen.get_width() // 2, screen.get_height() // 4)
    screen.blit(title_text, title_rect)

    play_text = font.render("PLAY", True, white)
    play_rect = play_text.get_rect()
    play_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(play_text, play_rect)

    quit_text = font.render("QUIT", True, white)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (screen.get_width() // 2, screen.get_height() // 2 + play_rect.height)
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
    for i in range(0, life):
        screen.blit(heart, (20 + i * 60, 20))
    next_surface = font.render(next_word, True, white)
    next_rect = next_surface.get_rect()
    next_rect.center = (screen.get_width() // 2, 200)
    screen.blit(next_surface, next_rect)
    for i, letter in enumerate(active_word):
        if i < len(pressed_word):
            color = green
        else:
            color = white
        letter_surface = font.render(letter, True, color)
        letter_rect = letter_surface.get_rect()
        letter_rect.center = (screen.get_width() // 2 - len(active_word) * 14 + i * 30, 400)
        screen.blit(letter_surface, letter_rect)
    if life == 0:
        main_menu()
    count_rect.center = (420, 40)
    screen.blit(count,count_rect)

    pygame.display.update()

    clock.tick(60)