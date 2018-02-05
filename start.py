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
		self.mask = pygame.mask.from_surface(self.image)

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
		self.imagen = load_image(imagen, True)
		self.imagen_transp=load_image('images/soldado_spritesheet_nada.png', True)
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.velx = velx
		self.speed = [velx, vely]
		self.vida = 5
		self.saltando = False
		self.cayendo = True
		self.disparando = False
		self.cargando = False
		self.invulnerable = False
		self.contadorInvulnerable = 0
		self.contadorFrame = 2
		self.cargador = 250
		self.indiceVelocidad = 0
		self.stagePosX = 0
		self.xVelocidad = 0
		self.mask = pygame.mask.from_surface(self.image)

	def Mover(self,time,keys,stagewidth):
		if self.vida > 0:
			if keys[K_LEFT]:
				if self.rect.left >= 0:
					self.xVelocidad = -self.speed[1]
					
					if not self.disparando:
						self.rect.centerx -= self.speed[1] * time
						self.row=0						
					else:
						self.rect.centerx -= (self.speed[1]/20) * time
						
					for objeto in escenario:
						objeto.rect.centerx += self.speed[1] * time
						objeto.mask = pygame.mask.from_surface(objeto.image)				
				if not self.saltando and not self.cayendo and self.contadorFrame == 0:
					if self.row==3:
						if self.col >1:
							self.col-=1
						else:
							self.col=9
					else:
						if self.col <=1:
							self.col +=1
						elif self.col <9 and self.col>1:
							self.col +=1
						else:
							self.col = 2

			elif keys[K_RIGHT]:
				if self.rect.right <= stagewidth:
					self.xVelocidad = self.speed[1]
					
					if not self.disparando:
						self.rect.centerx += self.speed[1] * time
						self.row=1
					else:
						self.rect.centerx += (self.speed[1]/20) * time
						
					for objeto in escenario:
						objeto.rect.centerx -= self.speed[1] * time
						objeto.mask = pygame.mask.from_surface(objeto.image)			
				if not self.saltando and not self.cayendo and self.contadorFrame == 0:
					if self.row==2:
						if self.col >1:
							self.col-=1
						else:
							self.col=9
					else:
						if self.col <=1:
							self.col +=1
						elif self.col <9 and self.col>1:
							self.col +=1
						else:
							self.col = 2
			else:
				self.xVelocidad = 0
				if self.disparando:
					self.col=0
				if not self.saltando and not self.cayendo and not self.disparando:
					if self.row==4 and self.col<2 or self.row==2:
						self.row=0
					elif self.row==4 and self.col>1 or self.row==3:
						self.row=1
					if self.col==1:
						self.col=1
					else:
						self.col = 0

			if not self.saltando and not self.cayendo:
				if keys [K_UP]:
					self.saltando = True

				if keys [K_SPACE]:
					self.disparando = True

				else:
					self.disparando = False

			if self.disparando:
				if self.row==0 or self.row==2:
					self.row=2

				elif self.row==1 or self.row==3:
					self.row=3

	def update(self):
		self.contadorFrame += 1

		if self.invulnerable:
			self.contadorInvulnerable -= 1
		if self.contadorInvulnerable == 0:
			self.invulnerable = False

		if self.contadorFrame > 2:
			self.contadorFrame = 0
		if self.vida > 0:
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
					
			elif self.disparando or self.cargando:
				if not self.cargando:
					if self.row==2 or self.row==0:
						newBala = bala('images/bala.png',True,self.jugadorPosX+90,self.rect.top+112,"derecha",(7,4),0,0)
					elif self.row==3 or self.row==1:
						newBala = bala('images/bala.png',True,self.jugadorPosX+150,self.rect.top+112,"izquierda",(7,4),1,0)
					balas.add(newBala)
					self.cargador -=10
				else:
					self.cargador +=5

				if self.cargador == 0:
					self.cargando = True
				if self.cargador == 250:
					self.cargando = False
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
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
		self.disparando = False
		self.saltando = False
		self.cayendo = True
		self.indiceVelocidad = 0
		self.contadorFrame = 2
		self.cooldown = 0
		self.mask = pygame.mask.from_surface(self.image)
		self.vida = 100

	def update(self, time, jug):
		if self.vida <= 0:
			self.kill()

		self.contadorFrame += 1
		if self.contadorFrame > 2:
			self.contadorFrame = 0
		self.speed = 0.5
		if self.cooldown > 0:
			self.cooldown-=1

		if self.rect.centerx > jug.jugadorPosX + 700:
			self.row = 0
			if self.contadorFrame == 0:
				if self.col < 5:
					self.col+=1
				else:
					self.col=1
			self.rect.centerx -= self.speed * time
			self.disparando = False

		elif self.rect.centerx < jug.jugadorPosX - 700:
			self.row = 1
			if self.contadorFrame == 0:
				if self.col < 5:
					self.col+=1
				else:
					self.col=1
			self.rect.centerx += self.speed * time
			self.disparando = False
		else:
			self.col = 0
			if not self.cayendo:
				self.disparando = True

		if self.cayendo == True:
			if self.indiceVelocidad < len(VELOCIDAD_G)/2:
				self.indiceVelocidad = len(VELOCIDAD_G)/2
			self.rect.centery += VELOCIDAD_G[self.indiceVelocidad]
			self.indiceVelocidad += 1
			if self.indiceVelocidad >= len(VELOCIDAD_G)-1:
				self.indiceVelocidad = len(VELOCIDAD_G)-1
			if (self.col == 0 and self.row == 2) or self.row == 0:
				self.col = 1
			elif (self.col == 2 and self.row == 2) or self.row == 1:
				self.col = 3
			self.row = 2

		if self.disparando == True and self.cooldown == 0:
			self.cooldown=120
			if self.row == 0:
				newFuego = fuego('images/boladefuego.png', self.rect.left - 20, self.rect.centery + 5,(64,57),self.row)
			else:
				newFuego = fuego('images/boladefuego.png', self.rect.right + 20, self.rect.centery + 5,(64,57),self.row)
			balas.add(newFuego)
			escenario.add(newFuego)

		if self.rect.top > HEIGHT:
			self.kill()

		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.mask = pygame.mask.from_surface(self.image)

class fuego(pygame.sprite.Sprite):
	def __init__(self,imagen,posx,posy,size,row):
		pygame.sprite.Sprite.__init__(self)
		self.col = 0
		self.row = row
		self.size = size
		self.x, self.y = size
		self.imagen = load_image(imagen, True)
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.speed = 0
		self.mask = pygame.mask.from_surface(self.image)

	def update(self,time):
		self.speed=0.5
		if self.col < 6:
			self.col += 1
		else:
			self.col = 0
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.mask = pygame.mask.from_surface(self.image)

		if self.row == 0:
			self.rect.centerx -= self.speed * time
		else:
			self.rect.centerx += self.speed * time

		if self.rect.centerx >= WIDTH or self.rect.centerx<=0:
			self.kill()

class plataforma(pygame.sprite.Sprite):
	def __init__(self,imagen,bottom,left,width,height):
		pygame.sprite.Sprite.__init__(self)
		self.imagen = load_image(imagen, True)
		self.image = pygame.transform.scale(self.imagen, (width,height))
		self.rect = self.image.get_rect()
		self.rect.bottom = bottom
		self.rect.left = left
		self.mask = pygame.mask.from_surface(self.image)

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
		if not jugador.disparando:
			jugador.stagePosX += -jugador.xVelocidad
		else:
			jugador.stagePosX += -jugador.xVelocidad/20

	rel_x = jugador.stagePosX % fondo.get_rect().width
	pantalla.blit(fondo,(rel_x - fondo.get_rect().width, 0 ))
	if rel_x < WIDTH:
		pantalla.blit(fondo, (rel_x,0))

# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------
def colisiones(objetos1, objetos2):
	for objeto1 in objetos1:
		for objeto2 in objetos2:
			colision = sprite.mask.overlap(plataforma.mask,(plataforma.rect.left-sprite.rect.left, plataforma.rect.centery-sprite.rect.centery))
			
def colisionesJugador(plataformas, jug):
	for bala in balas:
		colision = jug.mask.overlap(bala.mask,(bala.rect.centerx - jug.jugadorPosX,  jug.rect.bottom - 20 - bala.rect.centery))
		if colision and not jug.invulnerable:
			jug.vida -= 1
			jug.invulnerable = True
			jug.contadorInvulnerable = 240

		for oso in osos:
			if pygame.sprite.collide_mask(bala, oso):
				bala.kill()
				oso.vida -= 4

			if jug.mask.overlap(oso.mask, (oso.rect.left-jug.jugadorPosX, oso.rect.centery - jug.rect.centery)):
				if not jug.invulnerable:
					jug.vida -= 1
					jug.invulnerable = True
					jug.contadorInvulnerable = 240
					
	for plataforma in plataformas:
		colision = jug.mask.overlap(plataforma.mask,(plataforma.rect.left-jug.jugadorPosX, plataforma.rect.centery - (jug.rect.bottom - 200)))
		if colision:
			jug.cayendo = False
			jug.indiceVelocidad = 0
			if jug.rect.bottom-36 > plataforma.rect.top:
				jug.rect.bottom = plataforma.rect.top
			break
			
		else:
			if not jug.saltando:
				jug.cayendo = True

		for sprite in allsprites:
			colision = sprite.mask.overlap(plataforma.mask,(plataforma.rect.left-sprite.rect.left, plataforma.rect.centery-sprite.rect.centery))
			if colision:
				sprite.cayendo = False
				sprite.indiceVelocidad = 0
				if sprite.rect.bottom > plataforma.rect.top:
					sprite.rect.bottom = plataforma.rect.top+36
			else:
				if not sprite.saltando:
					sprite.cayendo = True

def invocarOsos(jug):
	newOso1 = oso('images/oso_spritesheet.png',True,1600,SUELO+150,(267,267),0,0)
	osos.add(newOso1)
	allsprites.add(newOso1)
	escenario.add(newOso1)


def dibujarInterfaz(pantalla, jug, vida, osos):
	if jug.vida > 1:
		pantalla.blit(vida,(20,20,47,46))
		if jug.vida > 2:
			pantalla.blit(vida,(67,20,47,46))
			if jug.vida > 3:
				pantalla.blit(vida,(114,20,47,46))
				if jug.vida > 4:
					pantalla.blit(vida,(161,20,47,46))
					
	for oso in osos:
		pygame.draw.circle(pantalla, (255,255,0,0),(oso.rect.centerx,oso.rect.centery),25)
		pygame.draw.circle(pantalla, (255,0,0,0),(oso.rect.right,oso.rect.centery),5)
		pygame.draw.circle(pantalla, (255,0,0,0),(oso.rect.left,oso.rect.centery),5)
		if oso.vida < 100:
			pygame.draw.rect(pantalla, (255,0,0,255), (oso.rect.centerx, oso.rect.top, oso.vida, 5))

def colocarPlataformas(plataformas):
	plataforma1 = plataforma('images/plataforma.png', HEIGHT+2, 0, 1250, 100)
	plataforma2 = plataforma('images/plataforma.png', HEIGHT-50, 1600, 500, 100)
	plataforma3 = plataforma('images/plataforma.png', HEIGHT+2, 2300, 500, 100)
	plataforma4 = plataforma('images/plataforma.png', HEIGHT-400, 2300, 500, 100)
	plataformas.add(plataforma1,plataforma2,plataforma3,plataforma4)
						
# ---------------------------------------------------------------------
# Programa Principal
# ---------------------------------------------------------------------
allsprites = pygame.sprite.Group()
balas = pygame.sprite.Group()
osos = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
escenario = pygame.sprite.Group()

def main():
# Inicializaciones pygame
	pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Juego Epumer")
	background_image = load_image('images/fondo.png')
	fondoancho, fondoaltura = background_image.get_rect().size
	stagewidth = fondoancho * 4

# Inicializaciones elementos de juego
	jug = jugador('images/soldado_spritesheet.png',True,WIDTH/2,SUELO+100,1.0,0.5,(267,267),0,1)
	vida = load_image('images/soldado_vida.png', True)
	#cuadradoprueba = elemento('images/cuadrado1.png',True,1000,600,2.0,0.5,(40,40),0,0)
	clock = pygame.time.Clock()
	colocarPlataformas(plataformas)
	invocarOsos(jug)		
	for platform in plataformas:
		escenario.add(platform)
	contadorInvocacion = 0
	while True:
		time = clock.tick(60)
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
# Procesamos jugador
		sidescroll(background_image,stagewidth,pantalla,jug)
		keys = pygame.key.get_pressed()
		jug.Mover(time,keys,stagewidth)

# Procesamos ia

# Actualizamos estado de la partida
		balas.update(time)
		osos.update(time, jug)
		jug.update()
		colisiones(balas,osos,plataformas,jug)
# Renderizamos
		if not jug.contadorInvulnerable%12==0 or not jug.invulnerable:
			pantalla.blit(jug.image, (jug.jugadorPosX,jug.rect.top+20,267,267))

		if jug.cargando:
			pygame.draw.rect(pantalla, (0,255,0,255), (jug.jugadorPosX+jug.rect.width/4, jug.rect.centery, jug.cargador/2, 5))
		balas.draw(pantalla)
		escenario.draw(pantalla)
		dibujarInterfaz(pantalla, jug, vida, osos)
		"""pygame.draw.circle(pantalla, (255,255,0,0), (jug.jugadorPosX,jug.rect.centery),25)
		pantalla.blit(jug.bala.image, (jug.bala.rect)) """
		pygame.display.flip()
	return 0

if __name__ == '__main__':
	pygame.init()
	main()
