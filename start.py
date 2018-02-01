#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos
import sys, pygame
import random
from pygame.locals import *

# Constantes
WIDTH = 1280
HEIGHT = 720
SUELO = HEIGHT - 300
VELOCIDAD_G = list([-12.0, -11.5, -11.0, -10.5, -10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0, -6.5, -6.0, -5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0])
# ---------------------------------------------------------------------
# Clases
# ---------------------------------------------------------------------
class elemento(pygame.sprite.Sprite):
	def __init__(self,imagen,transp,posx,posy,velx,vely,size,col,row):
		pygame.sprite.Sprite.__init__(self)
		self.col = col
		self.row = row
		self.size = size
		self.x, self.y = size
		self.imagen = pygame.image.load(imagen).convert_alpha()
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.speed = [velx, vely]

class bala(pygame.sprite.Sprite):
	def __init__(self,imagen,transp,posx,posy,orientacion,size,col,row):
		pygame.sprite.Sprite.__init__(self)
		self.col = col
		self.row = row
		self.size = size
		self.x, self.y = size
		self.imagen = pygame.image.load(imagen).convert_alpha()
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.speed = 0
		self.orientacion = orientacion

	def update(self,time):
		self.speed=3.0
		if self.orientacion == "derecha":
			self.rect.centerx -= self.speed * time
		else:
			self.rect.centerx += self.speed * time

		if self.rect.centerx >= WIDTH or self.rect.centerx<=0:
			self.kill()

class jugador(pygame.sprite.Sprite):
	def __init__(self, imagen, transp, posx, posy, velx, vely, size, col, row):
		pygame.sprite.Sprite.__init__(self)
		self.col = col
		self.row = row
		self.size = size
		self.x, self.y = size
		self.imagen = load_image(imagen, transp)
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.velx = velx
		self.speed = [velx, vely]
		self.saltando = False
		self.cayendo = True
		self.disparando = False
		self.indiceVelocidad = 0
		self.stagePosX = 0
		self.xVelocidad = 0
		self.mask = pygame.mask.from_surface(self.image)
		
	def Mover(self,time,keys,stagewidth):
		if keys[K_LEFT]:
			if self.rect.left >= 0:
				self.xVelocidad=-self.velx
				self.rect.centerx -= self.speed[1] * time
			if not self.disparando:
				self.row=0
			if not self.saltando and not self.cayendo:
				if self.row==3:
					if self.col >1:
						self.col-=1
					else:
						self.col=9
					self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
				else:
					if self.col <=1:
						self.col +=1
						self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
					elif self.col <9 and self.col>1:
						self.col +=1
						self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
					else:
						self.col = 2
						self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
						
		elif keys[K_RIGHT]:
			if self.rect.right <= stagewidth:
				self.xVelocidad = self.velx
				self.rect.centerx += self.speed[1] * time
			if not self.disparando:
				self.row=1
			if not self.saltando and not self.cayendo:
				if self.row==2:
					if self.col >1:
						self.col-=1
					else:
						self.col=9
					self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
				else:
					if self.col <=1:
						self.col +=1
						self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
					elif self.col <9 and self.col>1:
						self.col +=1
						self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
					else:
						self.col = 2
						self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		else:
			self.xVelocidad = 0
			if self.disparando:
				self.col=0
				self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
			if not self.saltando and not self.cayendo and not self.disparando:
				if self.row==4 and self.col<2 or self.row==2:
					self.row=0
				elif self.row==4 and self.col>1 or self.row==3:
					self.row=1
				if self.col==1:
					self.col=1
				else:
					self.col = 0
				self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))

		if not self.saltando and not self.cayendo:
			if keys [K_UP]:
				self.saltando = True

			if keys [K_SPACE]:
				#Mirando a la izquierda
				self.disparando = True
				if self.row==2 or self.row==0:
					newBala = bala('images/bala.png',True,self.jugadorPosX+90,self.rect.top+112,"derecha",(7,4),0,0)
				elif self.row==3 or self.row==1:
					newBala = bala('images/bala.png',True,self.jugadorPosX+150,self.rect.top+112,"izquierda",(7,4),1,0)
				balas.add(newBala)
			else:
				self.disparando = False

		if self.disparando:
			if self.row==0 or self.row==2:
				self.row=2

			elif self.row==1 or self.row==3:
				self.row=3

		if self.saltando:
			self.disparando=False
			self.rect.centery += VELOCIDAD_G[self.indiceVelocidad]
			self.indiceVelocidad +=1
			if self.indiceVelocidad >= len(VELOCIDAD_G)/2:
				self.saltando = False
				self.cayendo = True
			else:
				if self.row==0:
					self.col = 0
				elif self.row==1:
					self.col = 2
				self.row = 4
				self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))

		if self.cayendo:
			if self.indiceVelocidad < len(VELOCIDAD_G)/2:
				self.indiceVelocidad = len(VELOCIDAD_G)/2
			self.rect.centery += VELOCIDAD_G[self.indiceVelocidad]
			self.indiceVelocidad += 1
			if self.indiceVelocidad >= len(VELOCIDAD_G)-1:
				self.indiceVelocidad = len(VELOCIDAD_G)-1
			if self.col == 0 or self.row == 0:
				self.col = 1
			elif self.col == 2 or self.row == 1:
				self.col = 3
			self.row = 4
			self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
	
	def update(self):
		self.mask = pygame.mask.from_surface(self.image)
		
class oso(pygame.sprite.Sprite):
	def __init__(self,imagen,transp,posx,posy,size,col,row):
		pygame.sprite.Sprite.__init__(self)
		self.col = col
		self.row = row
		self.size = size
		self.x, self.y = size
		self.imagen = pygame.image.load(imagen).convert_alpha()
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.speed = 0
	
	def update(self, time, jug):
		self.speed = 0.5
		if self.rect.centerx > jug.jugadorPosX:
			self.row = 0
			if self.col < 5:
				self.col+=1
			else:
				self.col=1			
			self.rect.centerx -= self.speed * time
			
		elif self.rect.centerx < jug.jugadorPosX:
			self.row = 1
			if self.col < 5:
				self.col+=1
			else:
				self.col=1
			self.rect.centerx += self.speed * time
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))		

class plataforma(pygame.sprite.Sprite):
	def __init__(self,imagen):
		pygame.sprite.Sprite.__init__(self)		
		self.image = load_image(imagen)
		self.image = pygame.transform.scale(self.image, (WIDTH-300, 30))
		self.rect = self.image.get_rect()
		self.rect.bottom = HEIGHT-20
		self.rect.left = 300
		self.mask = pygame.mask.from_surface(self.image)
					
	#def update(self, jug):
	#	self.posx = self.posx - jug.jugadorPosX
		
# ---------------------------------------------------------------------
# Funciones generales
# ---------------------------------------------------------------------

def load_image(filename, transparent=False):
	try: image = pygame.image.load(filename)
	except pygame.error, message:
			raise SystemExit, message
	image = image.convert()
	if transparent:
			color = image.get_at((0,0))
			image.set_colorkey(color, RLEACCEL)

	return image

def texto(texto, fuente, posx, posy, color):
	salida = pygame.font.Font.render(fuente, texto, 1, color)
	salida_rect = salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

def sidescroll(fondo,stagewidth,pantalla,jugador):
	if jugador.rect.centerx > stagewidth-25:
		jugador.rect.centerx = stagewidth-25
	if jugador.rect.centerx < 25:
		jugador.rect.centerx = 25
	if jugador.rect.centerx < WIDTH/2:
		jugador.jugadorPosX = jugador.rect.centerx-100
	elif jugador.rect.centerx > stagewidth - WIDTH/2:
		jugador.jugadorPosX = jugador.rect.centerx - stagewidth + WIDTH - 100
	else:
		jugador.jugadorPosX = WIDTH/2 - 100
		jugador.stagePosX += -jugador.xVelocidad

	rel_x = jugador.stagePosX % fondo.get_rect().width
	pantalla.blit(fondo,(rel_x - fondo.get_rect().width, 0 ))
	if rel_x < WIDTH:
		pantalla.blit(fondo, (rel_x,0))
	
# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------

def colisiones(balas, osos , plataformas, allsprites):
	for bala in balas:
		for oso in osos:
			if pygame.sprite.collide_mask(bala, oso):
				bala.kill()
				oso.kill()
	for plataforma in plataformas:
		for sprite in allsprites:			
			colision = plataforma.mask.overlap(sprite.mask, (WIDTH/2-sprite.jugadorPosX, SUELO+100-sprite.rect.top+20))
			if colision:
				sprite.cayendo = False
				sprite.indiceVelocidad = 0
			else:
				sprite.cayendo = True
				
def invocarOsos():
	print
	#if len(osos) < 1:
	#	newOso = oso('images/oso_spritesheet.png',True,WIDTH,SUELO+150,(267,267),0,0)
	#	osos.add(newOso)

# ---------------------------------------------------------------------
# Programa Principal
# ---------------------------------------------------------------------
allsprites = pygame.sprite.Group()
balas = pygame.sprite.Group()
osos = pygame.sprite.Group()
plataformas = pygame.sprite.Group()

def main():
# Inicializaciones pygame
	pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Juego Epumer")
	background_image = load_image('images/fondo.png')
	fondoancho, fondoaltura = background_image.get_rect().size
	stagewidth = fondoancho * 4

# Inicializaciones elementos de juego
	jug = jugador('images/soldado_spritesheet.png',True,WIDTH/2,SUELO+100,1.0,0.5,(267,267),0,1)
	#cuadradoprueba = elemento('images/cuadrado1.png',True,1000,600,2.0,0.5,(40,40),0,0)
	allsprites.add(jug)
	clock = pygame.time.Clock()
	plataforma1 = plataforma('images/cuadrado2.png')
	plataformas.add(plataforma1)
	while True:
		time = clock.tick(30)
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
# Procesamos jugador
		sidescroll(background_image,stagewidth,pantalla,jug)
		keys = pygame.key.get_pressed()
		jug.Mover(time,keys,stagewidth)

# Procesamos ia

# Actualizamos estado de la partida
		invocarOsos()
		balas.update(time)
		osos.update(time, jug)
		allsprites.update()
		colisiones(balas,osos,plataformas,allsprites)
# Renderizamos
		plataformas.draw(pantalla)
		pantalla.blit(jug.image, (jug.jugadorPosX,jug.rect.top+20,267,267))
		balas.draw(pantalla)
		osos.draw(pantalla)
		"""pygame.draw.circle(pantalla, (255,255,0,0), (jug.jugadorPosX,jug.rect.centery),25)
		pantalla.blit(jug.bala.image, (jug.bala.rect)) """


		pygame.display.flip()
	return 0

if __name__ == '__main__':
	pygame.init()
	main()
