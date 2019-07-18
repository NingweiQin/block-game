import pygame
import sys
import random

pygame.init()

width = 800	
height = 600

red = (255,0,0)
blue = (0,0,255)
score_color = (178,34,34)
background_color = (0,238,238)


player_size = 50
player_pos = [width/2, height-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0,width-enemy_size),0]
enemy_numbers = 10

screen = pygame.display.set_mode((width,height))

pygame.display.set_caption("Sins")

clock = pygame.time.Clock()

speed = 10

score = 0

my_font = pygame.font.SysFont("monospace", 35)

enemy_list = [enemy_pos]

def set_level_speed(score, speed):
	if score < 20:
		speed = 5
	elif score < 50:
		speed = 7
	elif score < 90:
		speed = 10
	else:
		speed = 12
	return speed

def set_level_numbers(score, enemy_numbers):
	if score < 20:
		enemy_numbers = 6
	elif score < 50:
		enemy_numbers = 8
	elif score < 90:
		enemy_numbers = 10
	else:
		enemy_numbers = 12
	return enemy_numbers

def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < enemy_numbers and delay < 0.1:
		x_pos = random.randint(0,width-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos,y_pos])

def draw_enemy(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
	for index, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < height:
			enemy_pos[1] += speed
		else:
			enemy_list.pop(index)
			score += 1
	return score

def collision_check(player_pos, enemy_list):
	for enemy_pos in enemy_list:
		if detect_collision(player_pos, enemy_pos):
			return True
	return False

def detect_collision(player_pos, enemy_pos):

	p_x = player_pos[0]
	p_y = player_pos[1]
	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True
	return False

game_over = False
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:
				x -= player_size
			if event.key == pygame.K_RIGHT:
				x += player_size
			if event.key == pygame.K_UP:
				y -= player_size
			if event.key == pygame.K_DOWN:
				y += player_size
			player_pos=[x,y]

	screen.fill(background_color)

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	speed = set_level_speed(score, speed)
	enemy_numbers = set_level_numbers(score, enemy_numbers)

	text = "Score:" + str(score)
	label = my_font.render(text, 1, score_color)
	screen.blit(label, (width-200, height-40))

	if collision_check(player_pos, enemy_list):
		game_over = True

	draw_enemy(enemy_list)

	pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))
		
	clock.tick(30)

	pygame.display.update()