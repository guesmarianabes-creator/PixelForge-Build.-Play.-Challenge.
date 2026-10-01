import pygame

from ui.hud import (
    font,
    button,
    TEXT,
    MUTED,
    ACCENT,
    ACCENT_2,
    BG,
    PANEL,
    PANEL_2,
    draw_background
)


class GameSelect:

    def __init__(self, screen):

        self.screen = screen

        # =====================================================
        # CARDS DOS JOGOS
        # =====================================================

        self.cards = [

            {
                "id": "ppt",
                "number": "01",
                "title": "PEDRA, PAPEL",
                "title_2": "E TESOURA",
                "description": "Duelo rápido contra a máquina.",
                "tag": "ESTRATÉGIA",
                "rect": pygame.Rect(
                    70,
                    220,
                    465,
                    135
                ),
                "color": ACCENT
            },

            {
                "id": "velha",
                "number": "02",
                "title": "JOGO DA",
                "title_2": "VELHA",
                "description": "Enfrente a máquina em uma batalha 3x3.",
                "tag": "INTELIGÊNCIA",
                "rect": pygame.Rect(
                    565,
                    220,
                    465,
                    135
                ),
                "color": ACCENT_2
            },

            {
                "id": "forca",
                "number": "03",
                "title": "FORCA",
                "title_2": "",
                "description": "Descubra a palavra antes dos erros.",
                "tag": "PALAVRAS",
                "rect": pygame.Rect(
                    70,
                    385,
                    465,
                    135
                ),
                "color": (168, 85, 247)
            },

            {
                "id": "snake",
                "number": "04",
                "title": "SNAKE",
                "title_2": "",
                "description": "Colete pontos e sobreviva o máximo.",
                "tag": "ARCADE",
                "rect": pygame.Rect(
                    565,
                    385,
                    465,
                    135
                ),
                "color": ACCENT
            }
        ]

        # =====================================================
        # BOTÃO VOLTAR
        # =====================================================

        self.back_rect = pygame.Rect(
            70,
            565,
            210,
            52
        )

        self.hovered = None

    # =========================================================
    # EVENTOS
    # =========================================================

    def handle_event(self, event):

        # -----------------------------------------------------
        # TECLADO
        # -----------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "back"

        # -----------------------------------------------------
        # MOUSE
        # -----------------------------------------------------

        if event.type == pygame.MOUSEMOTION:

            self.hovered = None

            for card in self.cards:

                if card["rect"].collidepoint(
                    event.pos
                ):

                    self.hovered = card["id"]

                    break

        # -----------------------------------------------------
        # CLIQUE
        # -----------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return None

            for card in self.cards:

                if card["rect"].collidepoint(
                    event.pos
                ):

                    return card["id"]

            if self.back_rect.collidepoint(
                event.pos
            ):

                return "back"

        return None

    # =========================================================
    # ÍCONE PEDRA, PAPEL E TESOURA
    # =========================================================

    def draw_ppt_icon(self, x, y, color):

        # Pedra
        pygame.draw.circle(
            self.screen,
            (160, 174, 210),
            (x - 38, y),
            23
        )

        # Papel
        pygame.draw.rect(
            self.screen,
            TEXT,
            (
                x - 7,
                y - 27,
                34,
                54
            ),
            border_radius=3
        )

        # Linhas do papel
        for i in range(3):

            pygame.draw.line(
                self.screen,
                (120, 130, 160),
                (
                    x,
                    y - 14 + i * 11
                ),
                (
                    x + 18,
                    y - 14 + i * 11
                ),
                2
            )

        # Tesoura
        pygame.draw.line(
            self.screen,
            (248, 113, 113),
            (x + 38, y - 15),
            (x + 68, y - 3),
            4
        )

        pygame.draw.line(
            self.screen,
            (248, 113, 113),
            (x + 38, y + 15),
            (x + 68, y + 3),
            4
        )

        pygame.draw.circle(
            self.screen,
            (248, 113, 113),
            (x + 35, y - 15),
            5
        )

        pygame.draw.circle(
            self.screen,
            (248, 113, 113),
            (x + 35, y + 15),
            5
        )

    # =========================================================
    # ÍCONE JOGO DA VELHA
    # =========================================================

    def draw_velha_icon(self, x, y, color):

        size = 27

        grid_x = x - 38
        grid_y = y - 38

        # Grade
        for i in range(1, 3):

            pygame.draw.line(
                self.screen,
                (145, 155, 185),
                (
                    grid_x + i * size,
                    grid_y
                ),
                (
                    grid_x + i * size,
                    grid_y + 3 * size
                ),
                3
            )

            pygame.draw.line(
                self.screen,
                (145, 155, 185),
                (
                    grid_x,
                    grid_y + i * size
                ),
                (
                    grid_x + 3 * size,
                    grid_y + i * size
                ),
                3
            )

        # X
        pygame.draw.line(
            self.screen,
            ACCENT,
            (
                grid_x + 6,
                grid_y + 6
            ),
            (
                grid_x + 21,
                grid_y + 21
            ),
            4
        )

        pygame.draw.line(
            self.screen,
            ACCENT,
            (
                grid_x + 21,
                grid_y + 6
            ),
            (
                grid_x + 6,
                grid_y + 21
            ),
            4
        )

        # O
        pygame.draw.circle(
            self.screen,
            (248, 113, 113),
            (
                grid_x + 2 * size + 13,
                grid_y + 2 * size + 13
            ),
            10,
            4
        )

    # =========================================================
    # ÍCONE FORCA
    # =========================================================

    def draw_forca_icon(self, x, y, color):

        # Base
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x - 42,
                y + 32
            ),
            (
                x + 25,
                y + 32
            ),
            4
        )

        # Poste
        pygame.draw.line(
            self.screen,
            color,
            (
                x - 27,
                y + 32
            ),
            (
                x - 27,
                y - 38
            ),
            4
        )

        # Topo
        pygame.draw.line(
            self.screen,
            color,
            (
                x - 27,
                y - 38
            ),
            (
                x + 27,
                y - 38
            ),
            4
        )

        # Gancho
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x + 27,
                y - 38
            ),
            (
                x + 27,
                y - 22
            ),
            3
        )

        # Cabeça
        pygame.draw.circle(
            self.screen,
            TEXT,
            (
                x + 27,
                y - 10
            ),
            9,
            3
        )

        # Corpo
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x + 27,
                y
            ),
            (
                x + 27,
                y + 25
            ),
            3
        )

        # Braço esquerdo
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x + 27,
                y + 7
            ),
            (
                x + 10,
                y + 18
            ),
            3
        )

        # Braço direito
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x + 27,
                y + 7
            ),
            (
                x + 44,
                y + 18
            ),
            3
        )

        # Perna esquerda
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x + 27,
                y + 25
            ),
            (
                x + 13,
                y + 39
            ),
            3
        )

        # Perna direita
        pygame.draw.line(
            self.screen,
            TEXT,
            (
                x + 27,
                y + 25
            ),
            (
                x + 41,
                y + 39
            ),
            3
        )

    # =========================================================
    # ÍCONE SNAKE
    # =========================================================

    def draw_snake_icon(self, x, y, color):

        segments = [
            (x - 43, y + 14),
            (x - 21, y + 14),
            (x - 4, y),
            (x + 15, y),
            (x + 29, y - 18)
        ]

        for px, py in segments:

            pygame.draw.rect(
                self.screen,
                color,
                (
                    px,
                    py,
                    30,
                    21
                ),
                border_radius=8
            )

        # Olho
        pygame.draw.circle(
            self.screen,
            BG,
            (
                x + 40,
                y - 13
            ),
            3
        )

        # Comida
        pygame.draw.circle(
            self.screen,
            (248, 113, 113),
            (
                x + 35,
                y + 35
            ),
            9
        )

    # =========================================================
    # DESENHAR ÍCONE
    # =========================================================

    def draw_icon(
        self,
        game_id,
        x,
        y,
        color
    ):

        if game_id == "ppt":

            self.draw_ppt_icon(
                x,
                y,
                color
            )

        elif game_id == "velha":

            self.draw_velha_icon(
                x,
                y,
                color
            )

        elif game_id == "forca":

            self.draw_forca_icon(
                x,
                y,
                color
            )

        elif game_id == "snake":

            self.draw_snake_icon(
                x,
                y,
                color
            )

    # =========================================================
    # DESENHAR CARD
    # =========================================================

    def draw_card(self, card):

        rect = card["rect"]

        game_id = card["id"]

        color = card["color"]

        hovered = (
            self.hovered == game_id
        )

        # -----------------------------------------------------
        # SOMBRA
        # -----------------------------------------------------

        shadow_rect = pygame.Rect(
            rect.x + 4,
            rect.y + 6,
            rect.width,
            rect.height
        )

        pygame.draw.rect(
            self.screen,
            (5, 7, 13),
            shadow_rect,
            border_radius=18
        )

        # -----------------------------------------------------
        # FUNDO
        # -----------------------------------------------------

        if hovered:

            card_color = (
                29,
                35,
                56
            )

        else:

            card_color = PANEL_2

        pygame.draw.rect(
            self.screen,
            card_color,
            rect,
            border_radius=18
        )

        # -----------------------------------------------------
        # BORDA
        # -----------------------------------------------------

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            width=2 if hovered else 1,
            border_radius=18
        )

        # -----------------------------------------------------
        # NÚMERO
        # -----------------------------------------------------

        number = font(
            13,
            True
        ).render(
            card["number"],
            True,
            color
        )

        self.screen.blit(
            number,
            (
                rect.x + 20,
                rect.y + 16
            )
        )

        # -----------------------------------------------------
        # ÍCONE
        # -----------------------------------------------------

        self.draw_icon(
            game_id,
            rect.x + 95,
            rect.centery + 2,
            color
        )

        # -----------------------------------------------------
        # DIVISÓRIA
        # -----------------------------------------------------

        divider_x = rect.x + 190

        pygame.draw.line(
            self.screen,
            color,
            (
                divider_x,
                rect.y + 28
            ),
            (
                divider_x,
                rect.bottom - 28
            ),
            2
        )

        # -----------------------------------------------------
        # TEXTO
        # -----------------------------------------------------

        text_x = rect.x + 215

        title = font(
            20,
            True
        ).render(
            card["title"],
            True,
            TEXT
        )

        self.screen.blit(
            title,
            (
                text_x,
                rect.y + 27
            )
        )

        if card["title_2"]:

            title_2 = font(
                20,
                True
            ).render(
                card["title_2"],
                True,
                TEXT
            )

            self.screen.blit(
                title_2,
                (
                    text_x,
                    rect.y + 51
                )
            )

        # -----------------------------------------------------
        # DESCRIÇÃO
        # -----------------------------------------------------

        description_y = (
            rect.y + 77
            if card["title_2"]
            else rect.y + 58
        )

        description = font(
            12
        ).render(
            card["description"],
            True,
            MUTED
        )

        self.screen.blit(
            description,
            (
                text_x,
                description_y
            )
        )

        # -----------------------------------------------------
        # TAG
        # -----------------------------------------------------

        tag_y = rect.bottom - 29

        tag_text = font(
            10,
            True
        ).render(
            card["tag"],
            True,
            color
        )

        tag_rect = pygame.Rect(
            text_x,
            tag_y - 1,
            tag_text.get_width() + 18,
            20
        )

        pygame.draw.rect(
            self.screen,
            (21, 26, 42),
            tag_rect,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            color,
            tag_rect,
            width=1,
            border_radius=8
        )

        self.screen.blit(
            tag_text,
            (
                tag_rect.x + 9,
                tag_rect.y + 4
            )
        )

        # -----------------------------------------------------
        # INDICADOR JOGAR
        # -----------------------------------------------------

        play_color = (
            TEXT
            if hovered
            else color
        )

        play_text = font(
            11,
            True
        ).render(
            "JOGAR",
            True,
            play_color
        )

        play_x = (
            rect.right
            - play_text.get_width()
            - 38
        )

        play_y = rect.bottom - 28

        self.screen.blit(
            play_text,
            (
                play_x,
                play_y
            )
        )

        # -----------------------------------------------------
        # SETA
        # -----------------------------------------------------

        arrow_x = rect.right - 18

        arrow_y = rect.centery

        pygame.draw.line(
            self.screen,
            play_color,
            (
                arrow_x - 6,
                arrow_y - 6
            ),
            (
                arrow_x,
                arrow_y
            ),
            2
        )

        pygame.draw.line(
            self.screen,
            play_color,
            (
                arrow_x,
                arrow_y
            ),
            (
                arrow_x - 6,
                arrow_y + 6
            ),
            2
        )

        # -----------------------------------------------------
        # DESTAQUE NO HOVER
        # -----------------------------------------------------

        if hovered:

            pygame.draw.line(
                self.screen,
                color,
                (
                    rect.x + 20,
                    rect.bottom - 2
                ),
                (
                    rect.right - 20,
                    rect.bottom - 2
                ),
                3
            )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self):

        w, h = self.screen.get_size()

        # =====================================================
        # REDESENHA O FUNDO
        # =====================================================
        #
        # O GameManager já chama draw_background(),
        # mas fazemos novamente aqui para esconder o
        # draw_header antigo e ter controle total da tela.
        #

        draw_background(
            self.screen
        )

        # =====================================================
        # PEQUENA MARCA SUPERIOR
        # =====================================================

        brand = font(
            13,
            True
        ).render(
            "PIXELFORGE  /  ARCADE",
            True,
            MUTED
        )

        self.screen.blit(
            brand,
            (
                70,
                28
            )
        )

        # Linha decorativa
        pygame.draw.line(
            self.screen,
            (48, 55, 78),
            (
                70,
                52
            ),
            (
                w - 70,
                52
            ),
            1
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        title = font(
            45,
            True
        ).render(
            "ESCOLHA SEU JOGO",
            True,
            TEXT
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(
                    w // 2,
                    100
                )
            )
        )

        # =====================================================
        # SUBTÍTULO
        # =====================================================

        subtitle = font(
            17
        ).render(
            "Quatro desafios. Escolha seu próximo desafio.",
            True,
            MUTED
        )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    w // 2,
                    143
                )
            )
        )

        # =====================================================
        # LINHA DE DESTAQUE
        # =====================================================

        pygame.draw.line(
            self.screen,
            ACCENT,
            (
                w // 2 - 35,
                173
            ),
            (
                w // 2 + 35,
                173
            ),
            3
        )

        # =====================================================
        # CARDS
        # =====================================================

        for card in self.cards:

            self.draw_card(
                card
            )

        # =====================================================
        # BOTÃO VOLTAR
        # =====================================================

        button(
            self.screen,
            self.back_rect,
            "←  VOLTAR AO MENU"
        )