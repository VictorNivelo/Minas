import math
import pygame
import random

pygame.init()

ANCHO, ALTO = 800, 600
TAMANO_CUADRICULA = 40
ANCHO_CUADRICULA = ANCHO // TAMANO_CUADRICULA
ALTO_CUADRICULA = ALTO // TAMANO_CUADRICULA
FPS = 60
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas")
reloj = pygame.time.Clock()

controles = {
    "izquierda": pygame.K_LEFT,
    "derecha": pygame.K_RIGHT,
    "arriba": pygame.K_UP,
    "abajo": pygame.K_DOWN,
    "revelar": pygame.K_SPACE,
    "marcar": pygame.K_m,
    "pausa": pygame.K_ESCAPE,
}


class Tablero:
    def __init__(self, ancho, alto, minas):
        self.ancho = ancho
        self.alto = alto
        self.minas = minas
        self.celdas = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.reveladas = [[False for _ in range(ancho)] for _ in range(alto)]
        self.marcadas = [[False for _ in range(ancho)] for _ in range(alto)]
        self.colocar_minas()
        self.calcular_numeros()
        self.cursor = [0, 0]

    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
            if self.celdas[y][x] != -1:
                self.celdas[y][x] = -1
                minas_colocadas += 1

    def calcular_numeros(self):
        for y in range(self.alto):
            for x in range(self.ancho):
                if self.celdas[y][x] != -1:
                    self.celdas[y][x] = self.contar_minas_adyacentes(x, y)

    def contar_minas_adyacentes(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.ancho
                    and 0 <= ny < self.alto
                    and self.celdas[ny][nx] == -1
                ):
                    count += 1
        return count

    def revelar(self, x, y):
        if not self.reveladas[y][x] and not self.marcadas[y][x]:
            self.reveladas[y][x] = True
            if self.celdas[y][x] == 0:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.ancho and 0 <= ny < self.alto:
                            self.revelar(nx, ny)

    def marcar(self, x, y):
        if not self.reveladas[y][x]:
            self.marcadas[y][x] = not self.marcadas[y][x]

    def verificar_victoria(self):
        for y in range(self.alto):
            for x in range(self.ancho):
                if self.celdas[y][x] != -1 and not self.reveladas[y][x]:
                    return False
        return True

    def revelar_todas(self):
        for y in range(self.alto):
            for x in range(self.ancho):
                self.reveladas[y][x] = True

    def dibujar(self):
        for y in range(self.alto):
            for x in range(self.ancho):
                rect = pygame.Rect(
                    x * TAMANO_CUADRICULA,
                    y * TAMANO_CUADRICULA,
                    TAMANO_CUADRICULA,
                    TAMANO_CUADRICULA,
                )
                if self.reveladas[y][x]:
                    if self.celdas[y][x] == -1:
                        pygame.draw.rect(pantalla, ROJO, rect)
                        pygame.draw.circle(
                            pantalla, NEGRO, rect.center, TAMANO_CUADRICULA // 4
                        )
                        for i in range(4):
                            angle = i * (math.pi / 2)
                            end_pos = (
                                rect.centerx
                                + int(math.cos(angle) * TAMANO_CUADRICULA // 3),
                                rect.centery
                                + int(math.sin(angle) * TAMANO_CUADRICULA // 3),
                            )
                            pygame.draw.line(pantalla, NEGRO, rect.center, end_pos, 2)
                    else:
                        pygame.draw.rect(pantalla, BLANCO, rect)
                        if self.celdas[y][x] > 0:
                            fuente = pygame.font.Font(None, 36)
                            texto = fuente.render(str(self.celdas[y][x]), True, AZUL)
                            pantalla.blit(texto, texto.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(pantalla, GRIS, rect)
                    if self.marcadas[y][x]:
                        pygame.draw.polygon(
                            pantalla,
                            ROJO,
                            [
                                (rect.left + 10, rect.top + 10),
                                (rect.left + 10, rect.centery),
                                (rect.centerx, rect.top + TAMANO_CUADRICULA // 4),
                            ],
                        )
                        pygame.draw.line(
                            pantalla,
                            NEGRO,
                            (rect.left + 10, rect.top + 10),
                            (rect.left + 10, rect.bottom - 5),
                            2,
                        )
                pygame.draw.rect(pantalla, NEGRO, rect, 1)
        cursor_rect = pygame.Rect(
            self.cursor[0] * TAMANO_CUADRICULA,
            self.cursor[1] * TAMANO_CUADRICULA,
            TAMANO_CUADRICULA,
            TAMANO_CUADRICULA,
        )
        pygame.draw.rect(pantalla, VERDE, cursor_rect, 3)


def mostrar_mensaje(texto, y):
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 74)
    texto_renderizado = fuente.render(texto, True, BLANCO)
    pantalla.blit(
        texto_renderizado, (ANCHO // 2 - texto_renderizado.get_width() // 2, y)
    )
    pygame.display.flip()
    pygame.time.wait(2000)


def mostrar_mensaje_final(texto):
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Jugar de nuevo", "Salir al menú principal"]
    while True:
        pantalla.fill(NEGRO)
        texto_principal = fuente.render(texto, True, BLANCO)
        pantalla.blit(
            texto_principal, (ANCHO // 2 - texto_principal.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    return "jugar" if seleccion == 0 else "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, opcion in enumerate(opciones):
                    texto_opcion = fuente_pequeña.render(opcion, True, color)
                    rect = texto_opcion.get_rect(
                        center=(ANCHO // 2, ALTO // 2 + i * 50)
                    )
                    if rect.collidepoint(mouse_pos):
                        return "jugar" if i == 0 else "salir"
        pygame.display.flip()


def menu_principal():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Jugar", "Personalizar Controles", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente.render("Buscaminas", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        juego()
                    elif seleccion == 1:
                        personalizar_controles()
                    elif seleccion == 2:
                        pygame.quit()
                        return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, opcion in enumerate(opciones):
                    texto_opcion = fuente_pequeña.render(opcion, True, color)
                    rect = texto_opcion.get_rect(
                        center=(ANCHO // 2, ALTO // 2 + i * 50)
                    )
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            juego()
                        elif i == 1:
                            personalizar_controles()
                        elif i == 2:
                            pygame.quit()
                            return
        pygame.display.flip()


def personalizar_controles():
    fuente = pygame.font.Font(None, 36)
    fuente_Titulo = pygame.font.Font(None, 46)
    fuente_instrucciones = pygame.font.Font(None, 26)
    controles_orden = [
        "izquierda",
        "derecha",
        "arriba",
        "abajo",
        "revelar",
        "marcar",
        "pausa",
    ]
    seleccion = 0
    esperando_tecla = False
    gris_claro = (200, 200, 200)
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_Titulo.render("Personalizar Controles", True, BLANCO)
        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 50))
        for i, control in enumerate(controles_orden):
            color = AZUL if i == seleccion else BLANCO
            texto = f"{control.capitalize()}: {pygame.key.name(controles[control])}"
            if esperando_tecla and i == seleccion:
                texto = f"{control.capitalize()}: Presiona una tecla..."
            texto_renderizado = fuente.render(texto, True, color)
            pantalla.blit(
                texto_renderizado,
                (ANCHO // 2 - texto_renderizado.get_width() // 2, 120 + i * 50),
            )
        texto_instruccion = fuente_instrucciones.render(
            "Presiona ENTER para personalizar", True, gris_claro
        )
        pantalla.blit(
            texto_instruccion,
            (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO - 100),
        )
        texto_volver = fuente_instrucciones.render(
            "Presiona ESC para volver", True, gris_claro
        )
        pantalla.blit(
            texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, ALTO - 60)
        )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if esperando_tecla:
                    controles[controles_orden[seleccion]] = evento.key
                    esperando_tecla = False
                else:
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(controles_orden)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(controles_orden)
                    elif evento.key == pygame.K_RETURN:
                        esperando_tecla = True
                    elif evento.key == pygame.K_ESCAPE:
                        return
        pygame.display.flip()


def pausar():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Continuar", "Reiniciar", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        texto_pausa = fuente.render("Pausa", True, BLANCO)
        pantalla.blit(
            texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return
                    elif seleccion == 1:
                        return "reiniciar"
                    elif seleccion == 2:
                        return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, opcion in enumerate(opciones):
                    texto_opcion = fuente_pequeña.render(opcion, True, color)
                    rect = texto_opcion.get_rect(
                        center=(ANCHO // 2, ALTO // 2 + i * 50)
                    )
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            return
                        elif i == 1:
                            return "reiniciar"
                        elif i == 2:
                            return "salir"
        pygame.display.flip()


def juego():
    tablero = Tablero(ANCHO_CUADRICULA, ALTO_CUADRICULA, 10)
    game_over = False
    victoria = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if not game_over:
                    if evento.key == controles["izquierda"]:
                        tablero.cursor[0] = max(0, tablero.cursor[0] - 1)
                    elif evento.key == controles["derecha"]:
                        tablero.cursor[0] = min(
                            ANCHO_CUADRICULA - 1, tablero.cursor[0] + 1
                        )
                    elif evento.key == controles["arriba"]:
                        tablero.cursor[1] = max(0, tablero.cursor[1] - 1)
                    elif evento.key == controles["abajo"]:
                        tablero.cursor[1] = min(
                            ALTO_CUADRICULA - 1, tablero.cursor[1] + 1
                        )
                    elif evento.key == controles["revelar"]:
                        x, y = tablero.cursor
                        if tablero.celdas[y][x] == -1:
                            game_over = True
                        else:
                            tablero.revelar(x, y)
                            if tablero.verificar_victoria():
                                game_over = True
                                victoria = True
                    elif evento.key == controles["marcar"]:
                        x, y = tablero.cursor
                        tablero.marcar(x, y)
                if evento.key == controles["pausa"]:
                    seleccion = pausar()
                    if seleccion == "reiniciar":
                        return juego()
                    elif seleccion == "salir":
                        return menu_principal()
            if evento.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = (
                    evento.pos[0] // TAMANO_CUADRICULA,
                    evento.pos[1] // TAMANO_CUADRICULA,
                )
                tablero.cursor = [x, y]
                if evento.button == 1:
                    if tablero.celdas[y][x] == -1:
                        game_over = True
                    else:
                        tablero.revelar(x, y)
                        if tablero.verificar_victoria():
                            game_over = True
                            victoria = True
                elif evento.button == 3:
                    tablero.marcar(x, y)
        pantalla.fill(NEGRO)
        tablero.dibujar()
        if game_over:
            tablero.revelar_todas()
            pygame.display.flip()
            if victoria:
                accion = mostrar_mensaje_final("¡Ganaste!")
            else:
                accion = mostrar_mensaje_final("¡Perdiste!")
            if accion == "jugar":
                return juego()
            elif accion == "salir":
                return menu_principal()
        pygame.display.flip()
        reloj.tick(FPS)


menu_principal()
pygame.quit()
