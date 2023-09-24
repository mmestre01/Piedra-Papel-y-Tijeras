import pygame
import random

# Inicializar pygame
pygame.init()

# Constantes
ANCHO = 1200
ALTO = 800

# Colores
BLANCO = (255, 255, 255)

# Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Simulación Piedra, Papel o Tijera')

# Clases
class Objeto(pygame.sprite.Sprite):
    def __init__(self, image_file, x=None, y=None):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        
        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(0, ALTO - self.rect.height)
        
        self.velocidad_x = random.uniform(-0.2, 0.2)
        self.velocidad_y = random.uniform(-0.2, 0.2)
        self.contador = 0  # Contador de actualizaciones

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)


    def cambiar_direccion(self):
        # Cambiar dirección con una probabilidad muy baja, p.ej. 1%
        if random.random() < 0.01:
            self.velocidad_x = random.uniform(-0.2, 0.2)
            self.velocidad_y = random.uniform(-0.2, 0.2)

    def update(self):
        # Mover el objeto en cada actualización
        self.pos_x += self.velocidad_x
        self.pos_y += self.velocidad_y

        # Actualizar posición entera para el dibujo
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        # Cambiar de dirección ocasionalmente
        self.cambiar_direccion()

        # Invertir dirección si choca con bordes
        if self.rect.x < 0 or self.rect.x > ANCHO - self.rect.width:
            self.velocidad_x = -self.velocidad_x
        if self.rect.y < 0 or self.rect.y > ALTO - self.rect.height:
            self.velocidad_y = -self.velocidad_y

class Piedra(Objeto):
    def __init__(self, x=None, y=None):
        super().__init__('piedra.png', x, y)
        if x is None and y is None:
            self.rect.x = random.randint(ANCHO // 2, ANCHO - self.rect.width)
            self.rect.y = random.randint(0, ALTO // 2 - self.rect.height)

class Papel(Objeto):
    def __init__(self, x=None, y=None):
        super().__init__('papel.png', x, y)
        if x is None and y is None:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(ALTO // 2, ALTO - self.rect.height)

class Tijera(Objeto):
    def __init__(self, x=None, y=None):
        super().__init__('tijera.png', x, y)
        if x is None and y is None:
            self.rect.x = random.randint(0, ANCHO // 2 - self.rect.width)
            self.rect.y = random.randint(0, ALTO // 2 - self.rect.height)


def manejar_colision(objeto1, objeto2):
    if isinstance(objeto1, Piedra) and isinstance(objeto2, Tijera) or isinstance(objeto1, Tijera) and isinstance(objeto2, Piedra):
        x, y = objeto2.rect.x, objeto2.rect.y
        objeto2.kill()
        tijera_nueva = Piedra(x, y)
        todos.add(tijera_nueva)
        piedras.add(tijera_nueva)
        return True  # Colisión manejada

    elif isinstance(objeto1, Tijera) and isinstance(objeto2, Papel) or isinstance(objeto1, Papel) and isinstance(objeto2, Tijera):
        x, y = objeto2.rect.x, objeto2.rect.y
        objeto2.kill()
        papel_nuevo = Tijera(x, y)
        todos.add(papel_nuevo)
        tijeras.add(papel_nuevo)
        return True  # Colisión manejada

    elif isinstance(objeto1, Papel) and isinstance(objeto2, Piedra) or isinstance(objeto1, Piedra) and isinstance(objeto2, Papel):
        x, y = objeto2.rect.x, objeto2.rect.y
        objeto2.kill()
        piedra_nueva = Papel(x, y)
        todos.add(piedra_nueva)
        papeles.add(piedra_nueva)
        return True  # Colisión manejada

    return False  # No se manejó ninguna colisión

def mostrar_ganador(ganador, imagen_ganador):
    pantalla.fill(BLANCO)
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render("Ha ganado " + ganador, True, (0, 0, 0))
    pantalla.blit(texto, ((ANCHO - texto.get_width()) // 2, ALTO // 4))
    imagen = pygame.image.load(imagen_ganador)
    pantalla.blit(imagen, ((ANCHO - imagen.get_width()) // 2, ALTO // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos para que se pueda leer el mensaje
    pantalla.fill(BLANCO)
    todos.draw(pantalla)
    pygame.display.flip()
    pygame.quit()



# Crear grupos de sprites
todos = pygame.sprite.Group()
piedras = pygame.sprite.Group()
papeles = pygame.sprite.Group()
tijeras = pygame.sprite.Group()

for i in range(15): # Por ejemplo, 10 de cada objeto
    piedra = Piedra()
    papel = Papel()
    tijera = Tijera()

    todos.add(piedra, papel, tijera)
    piedras.add(piedra)
    papeles.add(papel)
    tijeras.add(tijera)

# Loop principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    todos.update()  # Actualiza la posición de los objetos

    # Lógica de colisiones y transformaciones
    colisiones_piedra_tijera = pygame.sprite.groupcollide(piedras, tijeras, False, False)
    colisiones_tijera_papel = pygame.sprite.groupcollide(tijeras, papeles, False, False)
    colisiones_papel_piedra = pygame.sprite.groupcollide(papeles, piedras, False, False)

    for piedra, tijeras_colisionadas in colisiones_piedra_tijera.items():
        for tijera in tijeras_colisionadas:
            if manejar_colision(piedra, tijera):  # Si se manejó la colisión, rompe el bucle interno
                break

    for tijera, papeles_colisionados in colisiones_tijera_papel.items():
        for papel in papeles_colisionados:
            if manejar_colision(tijera, papel):  # Si se manejó la colisión, rompe el bucle interno
                break

    for papel, piedras_colisionadas in colisiones_papel_piedra.items():
        for piedra in piedras_colisionadas:
            if manejar_colision(papel, piedra):  # Si se manejó la colisión, rompe el bucle interno
                break
    if (len(piedras) == 0 and len(papeles) == 0) or (len(tijeras) == 0 and len(papeles) == 0) or (len(piedras) == 0 and len(tijeras) == 0):
        if len(piedras) > 0:
            mostrar_ganador("Piedra", 'piedra.png')
        elif len(papeles) > 0:
            mostrar_ganador("Papel", 'papel.png')
        elif len(tijeras) > 0:
            mostrar_ganador("Tijera", 'tijera.png') 
    pantalla.fill(BLANCO)
    todos.draw(pantalla)
    pygame.display.flip()

pygame.quit()
