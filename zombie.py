import pygame, sys

pygame.init()

screen_height = 500
screen_width = 1000
screen_size = (screen_width, screen_height)
zombieCount = 10

win = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Zombie Mania")
scoreFont = pygame.font.SysFont('Comic Sans MS',30,False, True)

# setting up the sounds
bulletSound = pygame.mixer.Sound('NFF-laser-02.wav')
hitSound = pygame.mixer.Sound('NFF-kid-hurt.wav')
music = pygame.mixer.Sound('Lonewolf.wav')
music.play(-1)  # -1 plays music continuously

clock = pygame.time.Clock()
FPS = 60


bg = pygame.transform.scale(pygame.image.load("flatboy/background(1).png"), (1000, 600))

class Player:
	# setting up the sprites & background
	walkRight = [pygame.image.load('flatboy/walk (1).png'),pygame.image.load('flatboy/walk (2).png'),pygame.image.load('flatboy/walk (3).png'),pygame.image.load('flatboy/walk (4).png'),pygame.image.load('flatboy/walk (5).png'),pygame.image.load('flatboy/walk (6).png'),pygame.image.load('flatboy/walk (7).png'),pygame.image.load('flatboy/walk (8).png')]

	walkLeft = [pygame.image.load('flatboy/walk (8).png'),pygame.image.load('flatboy/walk (7).png'),pygame.image.load('flatboy/walk (6).png'),pygame.image.load('flatboy/walk (5).png'),pygame.image.load('flatboy/walk (4).png'),pygame.image.load('flatboy/walk (3).png'),pygame.image.load('flatboy/walk (2).png'),pygame.image.load('flatboy/walk (1).png')]
	# flip the image horizontally   pygame.transform.flip(image, horizontal = True, vertical = False)
	walkLeft = [pygame.transform.flip(sprite, True, False) for sprite in walkLeft]

	died = []
	
	jump = [pygame.image.load('flatboy/Jump (1).png'),pygame.image.load('flatboy/Jump (2).png'),pygame.image.load('flatboy/Jump (3).png'),pygame.image.load('flatboy/Jump (4).png'),pygame.image.load('flatboy/Jump (5).png'),pygame.image.load('flatboy/Jump (6).png'),pygame.image.load('flatboy/Jump (7).png'),pygame.image.load('flatboy/Jump (8).png'),pygame.image.load('flatboy/Jump (9).png'),pygame.image.load('flatboy/Jump (10).png'),pygame.image.load('flatboy/Jump (11).png'),pygame.image.load('flatboy/Jump (12).png'),pygame.image.load('flatboy/Jump (13).png'),pygame.image.load('flatboy/Jump (14).png'),pygame.image.load('flatboy/Jump (15).png')]

	character = pygame.image.load("flatboy/Idle (1).png")
	

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.walkRight = [pygame.transform.scale(sprite, (self.width,self.height)) for sprite in self.walkRight]
		self.walkLeft = [pygame.transform.scale(sprite, (self.width, self.height)) for sprite in self.walkLeft]
		self.jump = [pygame.transform.scale(sprite, (self.width, self.height)) for sprite in self.jump]
		self.character = pygame.transform.scale(self.character,(self.width, self.height))
		self.speed = 8
		self.left = False
		self.right = False
		self.isJump = False
		self.jummpLeft = False
		self.walkCount = 0
		self.jumpCount = 10
		self.deadCount = 0
		self.jumps = 0
		self.score = 0
		self.health = 1
		self.isDead = False
		self.hitbox = (self.x, self.y, 60, 100)
	
		for i in range(1,16):
			self.died.append(pygame.transform.scale(pygame.image.load(f'flatboy/Dead ({i}).png'),(self.width, self.height)))


	def draw(self, win):
		
		# show scores
		score_textsurface = scoreFont.render('Score : ' + str(self.score), False,(0,0,0))
		win.blit(score_textsurface,(830,10))

		if not(self.isDead):
			# Health Bar
			pygame.draw.rect(win, (250,0,0), (self.x, self.y-10, self.width-65, 10))
			pygame.draw.rect(win, (0,250,0), (self.x, self.y-10, self.width-65-((self.width-65)-(self.width-65)/self.health), 10))
			
			if self.walkCount+1 > 8:
				self.walkCount = 0
			if self.jumps+1 > 15:
				self.jumps = 0
			if self.left:
				win.blit(self.walkLeft[self.walkCount//1], (self.x-60,self.y))
				self.hitbox = (self.x+70, self.y, 60, 100)
				self.walkCount += 1
			elif self.right:
				win.blit(self.walkRight[self.walkCount//1], (self.x,self.y))
				self.hitbox = (self.x, self.y, 60, 100)
				self.walkCount += 1
			elif self.isJump:
				if self.jummpLeft:
					win.blit(pygame.transform.flip(self.jump[self.jumps//1],True,False), (self.x-50,self.y))
					self.hitbox = (self.x, self.y, 60, 100)
					self.jumps+=1
				else:
					win.blit(self.jump[self.jumps//1], (self.x,self.y))
					self.hitbox = (self.x, self.y, 60, 100)
					self.jumps+=1
			else:
				if self.left or self.jummpLeft:
					win.blit(pygame.transform.flip(self.character, True, False), (self.x,self.y))
				else:
					win.blit(self.character, (self.x,self.y))
		else:
			pygame.draw.rect(win,(255,0,0),(self.x+40,self.y,self.width-65,10))
			if self.deadCount >= 15:
				win.blit(self.died[14], (self.x, self.y))
			else:
				win.blit(self.died[self.deadCount], (self.x, self.y))
				pygame.time.delay(100) 				
				self.deadCount+= 1

		# pygame.draw.rect(win, (250, 0, 0), self.hitbox,3)

	def hit(self):
		if self.health < 2:
			self.score-= 5
			self.health+= 1
			font = pygame.font.SysFont('Comic Sans MS', 100, True, False)
			text = font.render('-5',False,(0,0,0))
			win.blit(text, (400, 180))

			self.x = 0
			zombie.x = 800 
			# zombie.health+=5
			pygame.display.update()
			pygame.time.delay(100)
		else:
			self.isDead = True




class Projectiles:
	bullets = []
	cooldown = 3
	
	def __init__(self, x, y, radius, color, direction):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.left, self.right = direction
		self.speed = 10
	
	def draw(self, win):
		if self.left:
			pygame.draw.circle(win, self.color, (self.x-50, self.y), self.radius)
		else:
			pygame.draw.circle(win, self.color, (self.x-10, self.y), self.radius)
			
class Enemy:
	died = []
	walk = []

	def __init__(self, x, y, width, height, enemy_constraints):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.speed = -4
		self.walkCount = 0
		self.diedCount = 0
		self.start, self.end = enemy_constraints
		self.hitbox = (self.x, self.y, self.width + 5, self.height + 5)
		self.health = 100
		self.isDead = False

		for i in range(1,11):
			self.walk.append(pygame.transform.scale(pygame.image.load(f'Zombiefiles/Walk ({i}).png'), (width,height)))
			self.died.append(pygame.transform.scale(pygame.image.load(f'Zombiefiles/Dead ({i}).png'), (width,height)))
	
	def draw(self, win):
		self.move()
		if not(self.isDead):
			pygame.draw.rect(win, (250,0,0),(self.x, self.y-8, self.width, 10))
			pygame.draw.rect(win, (0,250,0),(self.x, self.y-8, (self.width - ((self.width//100)*(100-self.health))), 10))
			if self.walkCount >= 10:
				self.walkCount = 0
			else:
				if self.speed > 0:
					win.blit(self.walk[self.walkCount//1], (self.x, self.y))
					self.walkCount+=1
				else:
					win.blit(pygame.transform.flip(self.walk[self.walkCount//1],True, False), (self.x, self.y))
					self.walkCount+=1
			self.hitbox = (self.x+13, self.y, self.width-25, self.height)
		else:
			self.hitbox = (0,0,0,0)
			if self.diedCount < 10:
				win.blit(self.died[self.diedCount//1], (self.x, self.y))
				self.diedCount += 1
			else:
				win.blit(self.died[9], (self.x, self.y))


		# pygame.draw.rect(win, (250,0,0), self.hitbox,3)


	def move(self):
		if not(self.isDead):
			self.x += self.speed
			if self.x >= self.end:
				self.speed *= -1
			if self.x <=self.start:
				self.speed *= -1

	def hit(self):
		hitSound.play()
		if self.health > 0:
			self.health-=10
			hero.score+=10
		else:
			self.isDead = True



def redraw_window():
	win.blit (bg, (0, 0))
	zombie.draw(win)
	hero.draw(win)
	# win.blit(hero.score_textsurface,(850,10))

	for bullet in Projectiles.bullets:
		bullet.draw(win)
	
	pygame.display.update()

run = True
hero = Player(0, 411, 130, 100)
zombie = Enemy(800, 400, 100, 100, (0, 900))


while run:
	clock.tick(FPS)
	Projectiles.cooldown-=1
	
	# listening for events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	# if hero.hitbox[0] > zombie.hitbox[0] and hero.hitbox[1] > zombie.hitbox[1]+zombie.height:
	# 	# if hero.hitbox[1] < zombie.hitbox[1] and hero.hitbox[1]+hero.height > zombie.hitbox[1]+zombie.height:
	# 	hero.hit()
	# if hero.hitbox[0]  > zombie.hitbox[0] and hero.hitbox[0] < zombie.hitbox[0] + zombie.width:
	# 			if hero.hitbox[1] > zombie.hitbox[1] and hero.hitbox[1] < zombie.hitbox[1] + zombie.height:
	# 				hero.hit()

	if hero.hitbox[1] - hero.hitbox[3] > zombie.hitbox[1] - zombie.hitbox[3]:
		if hero.hitbox[0] > zombie.hitbox[0] and hero.hitbox[0]+hero.hitbox[2] < zombie.hitbox[0]+zombie.hitbox[2]:
			hero.hit()
	for bullet in Projectiles.bullets:
		if bullet.x < screen_width and bullet.x > 0:
			if bullet.left:
				bullet.x-=bullet.speed
			else:
				bullet.x+=bullet.speed
			if bullet.x  > zombie.hitbox[0] and bullet.x < zombie.hitbox[0] + zombie.width:
				if bullet.y > zombie.hitbox[1] and bullet.y < zombie.hitbox[1] + zombie.height:
					zombie.hit()
					Projectiles.bullets.pop(Projectiles.bullets.index(bullet))
		else:
			Projectiles.bullets.pop(Projectiles.bullets.index(bullet))

	keys = pygame.key.get_pressed()
	if not(hero.isDead):
		if keys[pygame.K_SPACE]:
			if len(Projectiles.bullets) < 5 and Projectiles.cooldown == 2:
				bulletSound.play()
				Projectiles.bullets.append(Projectiles(round(hero.x+hero.width//2),round(hero.y+hero.height//2), 5, (250, 0, 0), (hero.left, hero.right)))
			else:
				Projectiles.cooldown = 3	
		if keys[pygame.K_LEFT] and hero.x >= 0 :
			hero.x-= hero.speed
			hero.left = True
			hero.right = False
			hero.jummpLeft = True
		elif keys[pygame.K_RIGHT] and hero.x < screen_width-50 :
			hero.x+= hero.speed
			hero.right = True
			hero.left = False
			hero.jummpLeft = False
		else:
			# hero.left = False
			# hero.right = False
			hero.walkCount = 0

		if not(hero.isJump):
			if keys[pygame.K_UP]:
				hero.isJump = True
				# hero.left = False
				# hero.right = False
				# hero.walkCount = 0

		else:
			if hero.left:
				hero.jummpLeft = True
			hero.left = False
			hero.right = False
			hero.walkCount = 0

			# jump logic code
			if hero.jumpCount >=-10:
				negative = 1
				if hero.jumpCount < 0:
					negative = -1
				hero.y -= hero.jumpCount ** 2 * 0.5 * negative
				hero.jumpCount -= 1
			
			else:
				if hero.jummpLeft:
					hero.left = True
				hero.isJump = False
				hero.right = False
				hero.jummpLeft = False
				hero.jumpCount = 10


	# continue on boundaries
	# if hero.x >= screen_width:
	# 	hero.x = screen_width
	# if hero.x < 0:
	# 	hero.x = 0
	# if hero.y >= screen_height:
	# 	hero.y = 0
	# if hero.y < 0:
	# 	hero.y = screen_height

	redraw_window()

sys.exit()