import pygame
from random import *

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0: idle #1: run #2: jump #3: attack1 #4: attack2 #5: hit #6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True


    def load_images(self, sprite_sheet, animation_steps):
        #Extrair Imagens do Spritsheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list


    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #Ler as Teclas
        key = pygame.key.get_pressed()

        #Apenas Faça Outra Ação se Não Estiver Atacando
        if self.attacking == False and self.alive == True and round_over == False:
            #Checa os Controles do Player 1
            if self.player == 1:
                #Movimento
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                #Pulo
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                #Ataque
                if key[pygame.K_e] or key[pygame.K_r]:
                    self.attack(surface, target)
                    #Determine Qual o Tipo de Ataque Foi Usado
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2
            #Checa os Controles do Player 2
            if self.player == 2:
                #Movimento
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                #Pulo
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                #Ataque
                if key[pygame.K_o] or key[pygame.K_p]:
                    self.attack(surface, target)
                    #Determine Qual o Tipo de Ataque Foi Usado
                    if key[pygame.K_o]:
                        self.attack_type = 1
                    if key[pygame.K_p]:
                        self.attack_type = 2

        #Aplicar a Gravidade
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Verificação de Player Dentro da Tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        #Deixar um Player Olhando Para o Outro
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Aplica o Cooldown de Ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #Update Player Position
        self.rect.x += dx
        self.rect.y += dy


    #Manipular Atualização das Animações
    def update(self):
        #Checa o que o Player esta Fazendo
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #6: Death
        elif self.hit == True:
            self.update_action(5) #5: Hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) #3: Attack1
            elif self.attack_type == 2:
                self.update_action(4) #4: Attack2
        elif self.jump == True:
            self.update_action(2) #2: Jump
        elif self.running == True:
            self.update_action(1) #1: Run
        else:
            self.update_action(0) #0: Idle

        animation_cooldown = 50
        #Atualização da Imagem/Frame
        self.image = self.animation_list[self.action][self.frame_index]
        #Checa o Tempo que Passou da Ultima Atualização
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #Checa se a Animação Chegou ao Fim
        if self.frame_index >= len(self.animation_list[self.action]):
            #Se o Jogador Morreu, Finaliza a Animação
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #Checa se um Ataque foi Executado
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #Checa se um Hit foi Executado
                if self.action == 5:
                    self.hit = False
                    #Se o Jogador esta no meio de um Ataque, o Ataque é Pausado
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def update_action(self, new_action):
        #Checa se a Nova Ação é Diferente da Anterior
        if new_action != self.action:
            self.action = new_action
            #Atualiza as Configurações da Animação
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))