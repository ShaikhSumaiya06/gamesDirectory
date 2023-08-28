import pygame
import random
import os
from pygame import mixer

pygame.init()
pygame.mixer.init()

screen_width = 900
screen_height = 600
fpsClock = pygame.time.Clock()
pygame.display.set_caption("SNAKE GAME")
screen = pygame.display.set_mode((screen_width, screen_height))

# font
font_obj = pygame.font.SysFont(None, 45)
def text_scr(text, color, x_pos, y_pos):
    screen_txt = font_obj.render(text, True, color)
    screen.blit(screen_txt, (x_pos, y_pos))


def plot_snake(screen, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(screen, color,[x, y, snake_size, snake_size])
# background image
file = "../assets/snake.png"
bc_img = pygame.image.load(file)
img = pygame.transform.scale(bc_img, (screen_width, screen_height)).convert_alpha()
# game over img
file2 = "../assets/over.jpeg"
go_img = pygame.image.load(file2)
goImg = pygame.transform.scale(go_img, (screen_width, screen_height)).convert_alpha()
def welcome():
    exit_game = False

    while not exit_game:
        screen.blit(img, (0, 0))
        text_scr(" Welcome to snakes !!!", (255, 255, 255), 260, 280)
        text_scr("Press Space bar to play ", (255, 255, 255), 250, 320 )
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit_game = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: # if space bar pressed
                    pygame.mixer.music.load("../sounds/Calimba - E's Jammy Jams.mp3")
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        fpsClock.tick(60)

def game_loop():

    # check if hiscore file exist
    if not os.path.exists("../hiscore.txt"):
        with open("../hiscore.txt", "w") as f:
            f.write("0")

    with open("../hiscore.txt", "r") as f:
        hiscore = f.read()
    # game specific variables
    fps = 30
    exit_game = False
    game_over = False
    snakeX = 15  # starting x position of snake
    snakeY = 30  # starting y position of snake
    s_sizeX = 19
    s_sizeY = 17
    f_sizeX = 10
    f_sizeY = 10
    s_size = 15
    velocity_X = 0
    velocity_Y = 0
    score = 0
    init_velocity = 5
    snake_len = 1
    snake_list = list()
    # colors
    w = (255, 255, 255)
    r = (255, 0, 0)
    g = (0, 255, 0)
    blue = (0, 0, 255)
    b = (0, 0, 0)

    # creating food for snake
    foodX = random.randint(20, screen_width - 20)
    foodY = random.randint(20, screen_height - 20)

    while not exit_game:
        screen.fill((0, 0, 0))
        fpsClock.tick(fps)
        if game_over:
            with open("../hiscore.txt", "w") as f:
                f.write(str(hiscore))

            screen.blit(goImg, (0, 0))
            text_scr(" Press Enter To Continue", r, 230, 550)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit_game = True

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN: # if press 'enter' button of the keyboard
                        game_loop()
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit_game = True

                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        velocity_X = init_velocity
                        velocity_Y = 0

                    if e.key == pygame.K_LEFT:
                        velocity_X = -init_velocity
                        velocity_Y = 0

                    if e.key == pygame.K_UP:
                        velocity_Y = -init_velocity
                        velocity_X = 0

                    if e.key == pygame.K_DOWN:
                        velocity_Y = init_velocity
                        velocity_X = 0
                    # cheetcode
                    if e.key == pygame.K_q:
                        score += 50

            snakeX += velocity_X
            snakeY += velocity_Y

            if abs(snakeX - foodX) < 12 and abs(snakeY - foodY) < 12:
                score += 10
                # food eating music
                pygame.mixer.music.load("../sounds/Beep Short .mp3")
                pygame.mixer.music.play()
                foodX = random.randint(20, screen_width - 20)
                foodY = random.randint(20, screen_height - 20)
                snake_len += 5

                if score>int(hiscore):
                    hiscore = score
                    # placing text on the screen
            text_scr("Score : " + str(score) + "  Hiscore : " + str(hiscore), w, 5, 5)


            # placing snake on the screen
            # pygame.draw.ellipse(screen, g, (snakeX, snakeY, s_sizeX, s_sizeY))

            head = []
            head.append(snakeX)
            head.append(snakeY)
            snake_list.append(head)
            plot_snake(screen, g, snake_list, s_size)

            if len(snake_list) > snake_len:
                del snake_list[0]

            if snakeX<0 or snakeX>screen_width or snakeY<0 or snakeY>screen_height:
                game_over = True
                # game over music
                pygame.mixer.music.load("../sounds/explosion.wav")
                pygame.mixer.music.play()
            # if co-ordinate of head and tail will become same then game over
            if head in snake_list[:-1]:
                game_over = True
                # game over music
                pygame.mixer.music.load("../sounds/explosion.wav")
                pygame.mixer.music.play()
            # placing food on the screen
            pygame.draw.rect(screen, r, (foodX, foodY, f_sizeX, f_sizeY))

        pygame.display.update()
        pygame.display.flip()

    pygame.quit()
    quit()
welcome()

