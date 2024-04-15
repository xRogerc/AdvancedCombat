import pygame
from fighter import Fighter

pygame.init()

#Cria a Janela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#Define o FPS
clock = pygame.time.Clock()
FPS = 60

#Definir Cores
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
AQUA_GREN = (0, 255, 130)
GRAY = (70, 70, 70)

#Definir As Variaveis de Jogo
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #Player Scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#Definir Tamanho dos Lutadores
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Carrega o Background
bg_image = pygame.image.load("assets/images/backgrounds/castles_in_the_mountain.jpg").convert_alpha()

#Carrega a Imagem de Vitória
victory_img = pygame.image.load("assets/images/icons/Victory.png").convert_alpha()

#Carrega os Spritesheets dos Players
warrior_spritesheet = pygame.image.load("assets/images/champions/warrior/Sprites/Warrior_Spritesheets.png").convert_alpha()
wizard_spritesheet = pygame.image.load("assets/images/champions/wizard/Sprites/Wizard_Spritesheets.png").convert_alpha()

#Define o Numero de Frames na Animação
WARRIOR_ANIMATION_FRAMES = [10, 8, 3, 7, 7, 3, 7]
WIZARD_ANIMATION_FRAMES = [8, 8, 2, 8, 8, 3, 7]

#Define Fontes
count_font = pygame.font.Font("assets/fonts/hexenkotel/Hexenkotel.otf", 100)
score_font = pygame.font.Font("assets/fonts/hexenkotel/Hexenkotel.otf", 30)

#Função de Desenhar Textos na Tela
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Função de Desenhar o Background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#Função de Desenhar a Barra de Vida dos Lutadores
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, GRAY, (x - 2, y - 2, 504, 34))
    pygame.draw.rect(screen, RED, (x, y, 500, 30))
    pygame.draw.rect(screen, AQUA_GREN, (x, y, 500 * ratio, 30))


#Cria duas Instancias dos Lutadores
fighter_1 = Fighter(1, 300, 420, False, WARRIOR_DATA, warrior_spritesheet, WARRIOR_ANIMATION_FRAMES)
fighter_2 = Fighter(2, 930, 420, True, WIZARD_DATA, wizard_spritesheet, WIZARD_ANIMATION_FRAMES)

#Game Loop
running = True
while running:

    clock.tick(FPS)

    #Draw Background
    draw_bg()

    #Exibir o Status do Lutador
    draw_health_bar(fighter_1.health, 30, 20)
    draw_health_bar(fighter_2.health, 752, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 30, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 750, 60)

    #Update Countdown
    if intro_count <= 0:
        #Movimenta os Lutadores
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #Display Count Timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2.08, SCREEN_HEIGHT / 3)
        #Update Count Timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            

    #Atualiza os Frames
    fighter_1.update()
    fighter_2.update()

    #Draw Lutadores
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #Checa se o Player Perdeu
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #Display Imagem da Vitória
        scaled_victory = pygame.transform.scale(victory_img, (825/2, 237/2))
        screen.blit(scaled_victory, (435, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 300, 420, False, WARRIOR_DATA, warrior_spritesheet, WARRIOR_ANIMATION_FRAMES)
            fighter_2 = Fighter(2, 930, 420, True, WIZARD_DATA, wizard_spritesheet, WIZARD_ANIMATION_FRAMES)

    #pygame.Quit se o usuario clicar no X fecha a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update Display
    pygame.display.update()

#Exit Pygame, Fecha o Jogo
pygame.quit()