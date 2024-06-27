"""
	NOTE:		
		1. Reduced the spawning time of clouds
		2. Added different speed to each of the cloud 
		3. Spawning at random x axis and y axis
"""

import pygame
from random import randint, choice, uniform

pygame.init()


# screen
WIDTH = 800
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Intro to pygame")


# global variables
running = True

CLOCK = pygame.time.Clock()

FONT = pygame.font.Font("Fonts/font1.ttf",35)

game_state = "OUTRO"

FLOOR = 430

enemy_speed = 7


# BG Music
pygame.mixer.music.load("Audio/music.wav")
pygame.mixer.music.set_volume(0.5)


# Timers
obstacle_adder = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_adder, 1400)

cloud_adder = pygame.USEREVENT + 2
pygame.time.set_timer(cloud_adder, randint(3*1000, 5*1000))


class Player(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()

		PLAYER_WALK_1 = pygame.image.load("Graphics/Player/player_walk_1.png").convert_alpha()
		PLAYER_WALK_2 = pygame.image.load("Graphics/Player/player_walk_2.png").convert_alpha()
		self.PLAYER_JUMP = pygame.image.load("Graphics/Player/jump.png").convert_alpha()
		self.PLAYER_WALK = [PLAYER_WALK_1, PLAYER_WALK_2]
		
		self.player_index = 0
		self.gravity = 0

		self.image = self.PLAYER_WALK[self.player_index]
		self.rect = self.image.get_rect(midbottom = (90,FLOOR))

		self.JUMP_SOUND = pygame.mixer.Sound("Audio/jump.mp3")
		self.JUMP_SOUND.set_volume(0.3)

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		
		if self.rect.bottom > FLOOR:
			self.rect.bottom = FLOOR
			self.gravity = 0

	def jump(self):
		if self.rect.bottom == FLOOR and game_state == "ACTIVE":
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE]:
				self.gravity = -20
				self.JUMP_SOUND.play()

	def animation(self):
		if self.rect.bottom < FLOOR:
			self.image = self.PLAYER_JUMP
		else:
			self.player_index += 0.1

			if self.player_index >= len(self.PLAYER_WALK):
				self.player_index = 0

			self.image = self.PLAYER_WALK[int(self.player_index)]

	def restart_changes(self):
		self.rect.bottom = FLOOR-2
		self.gravity = 0

	def update(self, screen_state):
		if screen_state == "ACTIVE":
			self.apply_gravity()
			self.jump()
			self.animation()
		
		elif screen_state == "OUTRO":
			self.restart_changes()

class Enemy(pygame.sprite.Sprite):

	def __init__(self, type):
		super().__init__()

		if type == "snail":
			SNAIL_SURF_1 = pygame.image.load("Graphics/Snail/snail1.png").convert_alpha()
			SNAIL_SURF_2 = pygame.image.load("Graphics/Snail/snail2.png").convert_alpha()
			self.SURFS = [SNAIL_SURF_1, SNAIL_SURF_2]
			
			Y_POS = FLOOR

		else:
			FLY_SURF_1 = pygame.image.load("Graphics/Fly/Fly1.png").convert_alpha()
			FLY_SURF_2 = pygame.image.load("Graphics/Fly/Fly2.png").convert_alpha()
			self.SURFS = [FLY_SURF_1, FLY_SURF_2]
			
			Y_POS = FLOOR - 90

		self.obstacle_index = 0

		self.image = self.SURFS[self.obstacle_index]
		self.rect = self.image.get_rect(midbottom = (randint(800, 1000), Y_POS))

	def animation(self):
		self.obstacle_index += 0.1

		if self.obstacle_index >= len(self.SURFS):
			self.obstacle_index = 0

		self.image = self.SURFS[int(self.obstacle_index)]

	def movement(self):
		global enemy_speed

		if self.rect.right <= 0:
			self.kill()
			enemy_speed += 1

		else:
			self.rect.x -= enemy_speed

	def update(self):
		self.animation()
		self.movement() 

class Cloud(pygame.sprite.Sprite):

	def __init__(self, num):
		super().__init__()

		self.speed = uniform(1.0, 3.0)

		CLOUD_1 = pygame.image.load("Graphics/Clouds/cloud1.png").convert_alpha()
		CLOUD_2 = pygame.image.load("Graphics/Clouds/cloud2.png").convert_alpha()
		CLOUD_3 = pygame.image.load("Graphics/Clouds/cloud3.png").convert_alpha()
		self.CLOUDS = [CLOUD_1, CLOUD_2, CLOUD_3]

		self.image = self.CLOUDS[num]
		self.rect = pygame.rect.Rect(randint(800, 850), randint(0, 10), 200, 200)

	def movement(self):      
		self.rect.x -= self.speed
          
		if self.rect.right <= 0:
			self.kill()

	def update(self):
		self.movement()


# Groups
Player = pygame.sprite.GroupSingle(sprite=Player())
Enemies = pygame.sprite.Group()
Clouds = pygame.sprite.Group()


# ACTIVE SCREEN
BG_SURF = pygame.image.load("Graphics/bg.png").convert()

GROUND_SURF = pygame.image.load("Graphics/ground.png").convert()

restart_time = 0
score = 0
def SCORE_DISPLAY():
	score = pygame.time.get_ticks()//1000 - restart_time
	score_surf = FONT.render("Score: "+str(score), True, "Black")
	score_rect = score_surf.get_rect(center = (400,40))

	screen.blit(score_surf, score_rect)

	return score

#checking collision
def IS_COLLIDE():
	if pygame.sprite.spritecollide(Player.sprite, Enemies, False): return True
	else: return False


# OUTRO SCREEN
#player image
PLAYER_STAND_SURF = pygame.image.load("Graphics/Player/player_stand.png").convert_alpha()
PLAYER_STAND_SURF = pygame.transform.rotozoom(PLAYER_STAND_SURF, 0, 2)
PLAYER_STAND_RECT = PLAYER_STAND_SURF.get_rect(center = (400, 200))

#static texts
GAME_INSTRUCTION_SURF = FONT.render("Press 'SPACE'", True, "White")
GAME_INSTRUCTION_RECT = GAME_INSTRUCTION_SURF.get_rect(center = (400, PLAYER_STAND_RECT.bottom + 140))

GAME_TITLE_SURF = FONT.render("Forest Jump", True, "White")
GAME_TITLE_RECT = GAME_TITLE_SURF.get_rect(center = (400, PLAYER_STAND_RECT.top - 60))

#score
out_score_surf = FONT.render("SCORE: "+ str(score),True, "White")
OUT_SCORE_RECT = out_score_surf.get_rect(center = (400, PLAYER_STAND_RECT.bottom + 60))


#game loop
while running:

	#checking the inputs
	for event in pygame.event.get():
 
		if event.type == pygame.QUIT:
			running = False

		if game_state == "ACTIVE":

			# Obstacle adder
			if event.type == obstacle_adder:
				Enemies.add(Enemy(choice(["snail","snail","snail","fly"])))

			# Cloud adder
			if event.type == cloud_adder:
				Clouds.add(Cloud(choice([0,1,2])))

		elif game_state == "OUTRO":

			if event.type == pygame.KEYDOWN:

				# restart

				if event.key == pygame.K_SPACE:
					pygame.time.delay(300)

					pygame.mixer.music.play(loops = -1)

					game_state = "ACTIVE"

					Player.update("OUTRO")

					Enemies.empty()

					Clouds.empty()
					Clouds.add(Cloud(1))

					restart_time = pygame.time.get_ticks()//1000


	if game_state == "ACTIVE":
		#screen
		screen.blit(BG_SURF, (0,0))
		screen.blit(GROUND_SURF, (0,FLOOR))

		#Drawing the Groups
		Player.update("ACTIVE")
		Player.draw(screen)

		Enemies.update()
		Enemies.draw(screen)

		Clouds.update()
		Clouds.draw(screen)

		score = SCORE_DISPLAY()

		if IS_COLLIDE():
			game_state = "OUTRO"
			pygame.mixer.music.stop()


	elif game_state == "OUTRO":
		#back ground
		screen.fill((94, 129, 162))
		#player image
		screen.blit(PLAYER_STAND_SURF, PLAYER_STAND_RECT)
		#texts
		screen.blit(GAME_INSTRUCTION_SURF, GAME_INSTRUCTION_RECT)
		screen.blit(GAME_TITLE_SURF, GAME_TITLE_RECT)
		#score
		out_score = FONT.render("SCORE: "+ str(score), True, "Black")
		screen.blit(out_score,OUT_SCORE_RECT)
 

	pygame.display.update()


	#framerate
	CLOCK.tick(60)


pygame.quit()