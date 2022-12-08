import pygame
import random
import os

pygame.init()
pygame.mixer.init()

# Creating Game Windows
screen_width = 900
screen_height = 500
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
wlcolor = (255, 152, 112)
game_window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()
# Background Image 
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game=False
    while not exit_game:
        game_window.fill(wlcolor)
        text_screen("Welcome to Snake",black, 330, 180)
        text_screen("Press Space Bar to Play",black, 295, 210)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
                    
                    
        pygame.display.update()
        clock.tick(50)

# Game Loop
def gameloop():
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play()
    # Game Spacific Variables
    game_over = False
    exit_game = False
    snake_x = 70
    snake_y = 70
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(10, screen_width/2)
    food_y = random.randint(10, screen_height/2)
    snake_size = 20
    snake_list = []
    snake_length = 1
    init_veleocity = 5
    fps = 50
    score = 0

    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            game_window.fill(white)
            text_screen("Game Over! Press Enter To Continue",red, 200, 200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = init_veleocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = -init_veleocity
                        velocity_y = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_y = -init_veleocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_y = init_veleocity
                        velocity_x = 0
                    if event.key == pygame.K_p:
                        score+=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(10, screen_width/2)
                food_y = random.randint(10, screen_height/2)
                snake_length += 5
                if  score>int(highscore):
                    highscore = score

            game_window.fill(white)
            game_window.blit(bgimg, (0,0))
            text_screen("Score: " + str(score + 10) + "  Highscore: " + str(highscore), red, 300, 5)
            pygame.draw.rect(game_window, black, [snake_x, snake_y, snake_size, snake_size])
    
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]
            
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            pygame.draw.rect(game_window, red, [food_x, food_y, snake_size, snake_size])
            plot_snake(game_window, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    # Exit Game
    pygame.quit()
    quit()

welcome()
