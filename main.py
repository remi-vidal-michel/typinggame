import pygame, random

pygame.init()

pygame.display.set_caption("Typing Game")
screen = pygame.display.set_mode((480, 720))

bg = pygame.image.load("assets/wallpaper.png")
resized_bg = pygame.transform.scale(bg, (480, 720))

font = pygame.font.Font("assets/MatchupPro.otf", 48)

word_speed = 0.5

def new_word():
    global active_word, pressed_word, lines, text, word_X, word_Y, word_speed 
    word_X = 200
    word_Y = 0
    word_speed += 0.1
    pressed_word = ""
    lines = open("words.txt").read().splitlines()
    active_word = random.choice(lines)
    text = font.render(active_word, True, (255, 255, 255))

new_word()

# boucle programme
clock = pygame.time.Clock()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            pressed_word += pygame.key.name(event.key)
            if active_word.startswith(pressed_word):
                if active_word == pressed_word:
                    new_word()
            else:
                pressed_word = ""
    
    screen.blit(resized_bg, (0, 0))
    word_Y += word_speed
    screen.blit(text, (word_X, word_Y))
    pygame.display.update()

    clock.tick(60)