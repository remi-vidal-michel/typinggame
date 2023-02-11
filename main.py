import pygame, random

pygame.init()

pygame.display.set_caption("Typing Game")
screen = pygame.display.set_mode((480, 720))

bg = pygame.image.load("assets/wallpaper.png")
resized_bg = pygame.transform.scale(bg, (480, 720))
bg_alt = pygame.image.load("assets/wallpaper_alt.png")
resized_bg_alt = pygame.transform.scale(bg_alt, (480, 720))

font = pygame.font.Font("assets/MatchupPro.otf", 70)
white = (255, 255, 255)

word_speed = 0.5

def new_word():
    global active_word, pressed_word, lines, text, text_rect, word_Y, word_speed 
    word_Y = 0
    word_speed += 0.1
    pressed_word = ""
    lines = open("words.txt").read().splitlines()
    active_word = random.choice(lines)
    text = font.render(active_word, True, white)
    text_rect = text.get_rect()

def main_menu():
    screen.blit(resized_bg, (0, 0))
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
                    new_word()
            else:
                pressed_word = ""
    
    screen.blit(resized_bg_alt, (0, 0))
    word_Y += word_speed
    if word_Y > 720:
        main_menu()
        word_speed = 0.5
    text_rect.center = (screen.get_width() // 2, word_Y)
    screen.blit(text, text_rect)
    pygame.display.update()

    clock.tick(60)