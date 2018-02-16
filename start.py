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
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# ---------------------------------------------------------------------
# Clases
# ---------------------------------------------------------------------
class final(pygame.sprite.Sprite):
	def __init__(self,imagen, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen).convert_alpha()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.centerx = posx
		self.rect.bottom = posy
		self.posicioninicial = posy, posx

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
		self.imagen_municion = load_image('images/munición.png', True)
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.jugadorPosX = self.rect.centerx
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
		self.cargador = 100
		self.indiceVelocidad = 0
		self.stagePosX = 0
		self.xVelocidad = 0
		self.puntuacion = 0
		self.mask = pygame.mask.from_surface(self.image)

	def Mover(self,time,keys,stagewidth):
		if self.vida > 0:
			if keys[K_LEFT]:
				if self.rect.left >= 0:
					self.xVelocidad = -self.speed[0]

					self.rect.centerx -= self.speed[0]
					self.row=0

					for objeto in escenario:
						objeto.rect.centerx += self.speed[0]
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
					self.xVelocidad = self.speed[0]

					self.rect.centerx += self.speed[0]
					self.row=1

					for objeto in escenario:
						objeto.rect.centerx -= self.speed[0]
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
					if self.row==0 or self.row==2:
						self.row=2

					elif self.row==1 or self.row==3:
						self.row=3
				else:
					self.disparando = False

	def update(self):
		self.contadorFrame += 1

		if self.invulnerable:
			self.contadorInvulnerable -= 1
		if self.contadorInvulnerable == 0:
			self.invulnerable = False

		if self.contadorFrame > 2:
			self.contadorFrame = 0
		if self.vida > 0:
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

			if self.cayendo:
				self.disparando = False
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

			elif self.disparando or self.cargando:
				if not self.cargando:
					if self.row==2 or self.row==0:
						newBala = bala('images/bala.png',True,self.jugadorPosX+80,self.rect.top+112,"derecha",(26,9),0,0)
					elif self.row==3 or self.row==1:
						newBala = bala('images/bala.png',True,self.jugadorPosX+230,self.rect.top+112,"izquierda",(26,9),1,0)
					balas.add(newBala)
					self.cargador -=4
				else:
					self.cargador +=1

				if self.cargador == 0:
					self.cargando = True
				if self.cargador == 100:
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
		self.muerte = pygame.image.load('images/explosion_spritesheet.png').convert_alpha()
		self.image = self.imagen.subsurface((self.x*self.col, self.y*self.row, self.x, self.y))
		self.rect = self.image.get_rect()
		self.rect.left = posx
		self.rect.bottom = posy
		self.posicioninicial = posy, posx
		self.speed = 0
		self.disparando = False
		self.saltando = False
		self.cayendo = True
		self.indiceVelocidad = 0
		self.contadorFrame = 2
		self.cooldown = 0
		self.mask = pygame.mask.from_surface(self.image)
		self.vida = 100
		self.izquierda = False
		self.derecha = False

	def update(self, time, jug, plataformas):
		self.contadorFrame += 1
		if self.contadorFrame > 2:
			self.contadorFrame = 0

		if self.vida <= 0 and self.vida > -100:
			self.vida = -100
			size = (96, 96)
			self.x, self.y = size
			self.row = 0
			self.col = 0
			self.rect.centerx += 75
			self.rect.centery -= 50

		if self.vida <= -100:
			if self.contadorFrame == 0:
				if self.col < 4:
					self.col += 1

				elif self.row < 2:
					self.col = 0
					self.row += 1
				else:
					jug.puntuacion += 1
					self.kill()

				self.imagen = pygame.transform.scale(self.muerte.subsurface((self.x*self.col, self.y*self.row, self.x, self.y)),(267,267))
				self.image = self.imagen

		if self.vida > 0:
			self.speed = 0.5
			if self.cooldown > 0:
				self.cooldown-=1
				
			if not self.izquierda:
				self.derecha = comprobarSiCae(self, plataformas, 'derecha')
				if self.derecha:
					if jug.jugadorPosX < self.rect.centerx + 600 and jug.jugadorPosX > self.rect.centerx:
						if not self.cayendo:
							self.row = 1
							self.col=0
							self.disparando = True
					else:
						self.rect.centerx += self.speed * time
						self.disparando = False
					self.row = 1
									
			if not self.derecha:
			 	self.izquierda = comprobarSiCae(self, plataformas, 'izquierda')
				if self.izquierda:
					if jug.jugadorPosX > self.rect.centerx - 600 and jug.jugadorPosX < self.rect.centerx:
						if not self.cayendo:
							self.col=0
							self.disparando = True
					else:
						self.rect.centerx -= self.speed * time
						self.disparando = False
					self.row = 0

			if (self.izquierda or self.derecha) and not self.disparando:
				if self.contadorFrame == 0:
					if self.col < 5:
						self.col+=1
					else:
						self.col=1

			if self.cayendo:
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

			if self.disparando and self.cooldown == 0:
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
		self.posicioninicial = bottom, left
		self.mask = pygame.mask.from_surface(self.image)
		self.ultima = False

	def update (self):
		self.rect.left
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
	entrada = pygame.font.Font(fuente, 25)
	salida = pygame.font.Font.render(entrada, texto, 1, color)
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
def comprobarSiCae(oso, plataformas, orientacion):
	for suelo in plataformas:
		if oso.mask.overlap(suelo.mask,((suelo.rect.left-oso.rect.left),suelo.rect.top-oso.rect.top)):
			if orientacion == 'izquierda':
				if oso.mask.overlap(suelo.mask,((suelo.rect.left-oso.rect.left) + 150,suelo.rect.top-oso.rect.top)):
					return True
				else:
					return False
			else:
				if oso.mask.overlap(suelo.mask,((suelo.rect.left-oso.rect.left) - 150,suelo.rect.top-oso.rect.top)):
					return True
				else:
					return False
		else:
			continue
	return False

def colisiones(balas, osos, plataformas, jug):
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

			if jug.mask.overlap(oso.mask, (oso.rect.centerx-jug.jugadorPosX, jug.rect.bottom - oso.rect.centery)):
				if not jug.invulnerable:
					jug.vida -= 1
					jug.invulnerable = True
					jug.contadorInvulnerable = 240

	for plataforma in plataformas:
		colision = jug.mask.overlap(plataforma.mask,(plataforma.rect.left-jug.jugadorPosX, plataforma.rect.centery - (jug.rect.bottom - 200)))
		if colision:
			jug.cayendo = False
			jug.indiceVelocidad = 0
			if jug.rect.bottom + 100 > plataforma.rect.top:
				jug.rect.bottom = plataforma.rect.top + 15
			colision = False
			break

		else:
			if not jug.saltando:
				jug.cayendo = True
				if jug.rect.top > HEIGHT:
					for bala in balas:
						bala.kill()
					for objeto in escenario:
						objeto.rect.bottom, objeto.rect.left = objeto.posicioninicial
					jug.rect.centerx = plataforma.rect.centerx
					jug.stagePosX = 0
					jug.rect.bottom = plataforma.rect.top
					jug.vida -= 1
					jug.invulnerable = True
					jug.contadorInvulnerable = 240

	for oso in osos:
		for plataforma in plataformas:
			colision = pygame.sprite.collide_mask(plataforma,oso)
			if colision != None:
				oso.cayendo = False
				oso.indiceVelocidad = 0
				if oso.rect.bottom + 130 > plataforma.rect.top:
					oso.rect.bottom = plataforma.rect.top+70
				colision = None
				break

			elif not colision and not oso.saltando:
				oso.cayendo = True

		if colision != None:
			break

def invocarOsos(plataformas):
	for plataforma in plataformas:
		if plataforma.rect.left == 0 or plataforma.rect.left == 7000:
			continue
		else:
			newOso = oso('images/oso_spritesheet.png',True,plataforma.rect.centerx,plataforma.rect.top,(267,267),0,0)
			osos.add(newOso)
			allsprites.add(newOso)
			escenario.add(newOso)


def dibujarInterfaz(pantalla, jug, vida, osos):
	for i in range(jug.vida):
		pantalla.blit(vida,(20+(47*i),20,47,46))
	
	for i in range(jug.cargador):
		pantalla.blit(jug.imagen_municion,(WIDTH-20-9*(25-int(i/4)),15,9,26))
		
	for oso in osos:
		if oso.vida < 100 and oso.vida > 0 and  oso.row==0:
			pygame.draw.rect(pantalla, (255,0,0,255), (oso.rect.centerx, oso.rect.top, oso.vida, 5))
		elif oso.vida < 100 and oso.vida > 0 and oso.row==1:
			pygame.draw.rect(pantalla, (255,0,0,255), (oso.rect.centerx - 100, oso.rect.top, oso.vida, 5))

def colocarPlataformas(plataformas):
	plataforma1 = plataforma('images/plataforma.png', HEIGHT+50, 0, 1250, 100)
	plataforma2 = plataforma('images/plataforma.png', HEIGHT-50, 1600, 750, 100)
	plataforma3 = plataforma('images/plataforma.png', HEIGHT+50, 3000, 1100, 100)
	plataforma4 = plataforma('images/plataforma.png', HEIGHT-400, 2500, 750, 100)
	plataforma5 = plataforma('images/plataforma.png', HEIGHT+50, 4000, 1200 ,100)
	plataforma6 = plataforma('images/plataforma.png', HEIGHT-300, 5500, 1000 ,100)
	plataforma7 = plataforma('images/plataforma.png', HEIGHT-100, 7000, 1000 ,100)	
	plataformas.add(plataforma1,plataforma2,plataforma3,plataforma4, plataforma5, plataforma6, plataforma7)
	allsprites.add(plataformas)
# ---------------------------------------------------------------------
# Programa Principal
# ---------------------------------------------------------------------
allsprites = pygame.sprite.Group()
balas = pygame.sprite.Group()
osos = pygame.sprite.Group()
plataformas = pygame.sprite.Group()
escenario = pygame.sprite.Group()
puntuacion_final = 0

def main():
# Inicializaciones pygame
	fin = False
	pygame.display.set_caption("Juego Epumer")
	background_image = load_image('images/fondo.png')
	fondoancho, fondoaltura = background_image.get_rect().size
	stagewidth = fondoancho * 4

# Inicializaciones elementos de juego
	jug = jugador('images/soldado_spritesheet.png',True,WIDTH/2,SUELO+100,7.0,0.5,(267,267),0,1)
	final_nivel = final('images/final.png', 7500, HEIGHT-250)
	allsprites.add(jug, final_nivel)
	vida = load_image('images/soldado_vida.png', True)
	#cuadradoprueba = elemento('images/cuadrado1.png',True,1000,600,2.0,0.5,(40,40),0,0)
	colocarPlataformas(plataformas)
	invocarOsos(plataformas)
	escenario.add(final_nivel)
	for platform in plataformas:
		escenario.add(platform)
	contadorInvocacion = 0
	while jug.vida > 0 and not fin:
		time = clock.tick(60)
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
# Procesamos jugador
		colisiones(balas,osos,plataformas,jug)
		sidescroll(background_image,stagewidth,pantalla,jug)
		keys = pygame.key.get_pressed()
		jug.Mover(time,keys,stagewidth)
		if jug.mask.overlap(final_nivel.mask,(final_nivel.rect.centerx - jug.jugadorPosX,  jug.rect.bottom - final_nivel.rect.centery)):
			fin = True

# Actualizamos estado de la partida
		plataformas.update()
		balas.update(time)
		osos.update(time, jug, plataformas)
		jug.update()
		p_jug, p_jug_rect = texto(str(jug.puntuacion),'fonts/SaucerBB.ttf',WIDTH/2, 40,(255,255,255))
		
# Renderizamos
		plataformas.draw(pantalla)
		if not jug.contadorInvulnerable%12==0 or not jug.invulnerable:
			pantalla.blit(jug.image, (jug.jugadorPosX,jug.rect.top+20,267,267))
		balas.draw(pantalla)
		osos.draw(pantalla)
		pantalla.blit(final_nivel.image, (final_nivel.rect.centerx, final_nivel.rect.centery,128,192))
		pantalla.blit(p_jug, p_jug_rect)
		dibujarInterfaz(pantalla, jug, vida, osos)
		pygame.display.flip()
	puntuacion_final = jug.puntuacion + jug.vida
	if not vida > 0:
		return False
	elif fin:
		return True

def gameOver():
	for i in allsprites:
		i.kill()
	game_over = load_image('images/game_over.png')
	game_over_image = pygame.transform.scale(game_over, (WIDTH,HEIGHT))
	continuar_imagen = load_image('images/enter.png',True)
	continuar_image = pygame.transform.scale(continuar_imagen,(25,25))
	salir_imagen = load_image('images/escape.png',True)
	salir_image = pygame.transform.scale(salir_imagen,(25,25))
	continuar_txt, continuar_txt_rect = texto('Continuar','fonts/SaucerBB.ttf',WIDTH-150,HEIGHT-45,(255,255,255))
	salir_txt, salir_txt_rect = texto('Salir','fonts/SaucerBB.ttf',120,HEIGHT-45,(255,255,255))
	while True:
		time = clock.tick(60)
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)			
		pantalla.blit(game_over_image, (0,0,WIDTH,HEIGHT))
		pantalla.blit(continuar_image, (WIDTH-60, HEIGHT-60,50,50))
		pantalla.blit(continuar_txt, continuar_txt_rect)
		pantalla.blit(salir_txt, salir_txt_rect)		
		pantalla.blit(salir_image, (45, HEIGHT-60,50,50))		
		keys = pygame.key.get_pressed()
		pygame.display.flip()		
		if keys[K_RETURN]:
			return True
		elif keys[K_ESCAPE]:
			return False
			
	return 0
	
def youWin():
	for i in allsprites:
		i.kill()
	you_win = load_image('images/you_win.png')
	you_win_image = pygame.transform.scale(you_win, (WIDTH,HEIGHT))
	continuar_imagen = load_image('images/enter.png',True)
	continuar_image = pygame.transform.scale(continuar_imagen,(25,25))	
	fin_txt, fin_txt_rect = texto('Pulsa        para salir','fonts/SaucerBB.ttf',WIDTH/2,HEIGHT/2+200,(255,255,255)) 
	while True:
		time = clock.tick(60)
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)			
		pantalla.blit(you_win_image, (0,0,WIDTH,HEIGHT))
		pantalla.blit(continuar_image, (WIDTH/2-45, HEIGHT/2+185,50,50))
		pantalla.blit(fin_txt, fin_txt_rect)		
		keys = pygame.key.get_pressed()
		pygame.display.flip()		
		if keys[K_RETURN]:
			return False
			
	return 0	

if __name__ == '__main__':
	continuar = True
	while continuar:
		pygame.init()
		if not main():
			continuar = gameOver()
		else:
			continuar = youWin()
	sys.exit(0)				
