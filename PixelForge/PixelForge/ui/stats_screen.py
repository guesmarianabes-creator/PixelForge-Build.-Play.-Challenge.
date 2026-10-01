import pygame

from ui.hud import (
    font,
    button,
    TEXT,
    MUTED,
    ACCENT,
    ACCENT_2,
    PANEL,
    PANEL_2,
    BG
)


class StatsScreen:

    def __init__(self, screen, stats):

        self.screen = screen
        self.stats = stats

        self.back = pygame.Rect(
            50, 645, 180, 48
        )

        self.reset = pygame.Rect(
            850, 645, 180, 48
        )

        self.hover_back = False
        self.hover_reset = False

        self.confirm_reset = False

    # ============================================================
    # EVENTOS
    # ============================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                return "menu"

            if event.key == pygame.K_r:

                self.stats.reset()

                self.confirm_reset = True

                return None

        if event.type == pygame.MOUSEMOTION:

            self.hover_back = self.back.collidepoint(
                event.pos
            )

            self.hover_reset = self.reset.collidepoint(
                event.pos
            )

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:

                return None

            if self.back.collidepoint(
                event.pos
            ):

                return "menu"

            if self.reset.collidepoint(
                event.pos
            ):

                self.stats.reset()

                self.confirm_reset = True

        return None

    # ============================================================
    # CARD
    # ============================================================

    def draw_card(
        self,
        rect,
        title,
        values
    ):

        pygame.draw.rect(
            self.screen,
            PANEL,
            rect,
            border_radius=16
        )

        pygame.draw.rect(
            self.screen,
            (48, 55, 78),
            rect,
            width=1,
            border_radius=16
        )

        # --------------------------------------------------------
        # TÍTULO
        # --------------------------------------------------------

        title_img = font(
            19,
            True
        ).render(
            title,
            True,
            ACCENT
        )

        self.screen.blit(
            title_img,
            (
                rect.left + 20,
                rect.top + 15
            )
        )

        # --------------------------------------------------------
        # VALORES
        # --------------------------------------------------------

        y = rect.top + 53

        for label, value in values:

            label_img = font(
                15
            ).render(
                label,
                True,
                MUTED
            )

            value_img = font(
                16,
                True
            ).render(
                str(value),
                True,
                TEXT
            )

            self.screen.blit(
                label_img,
                (
                    rect.left + 20,
                    y
                )
            )

            self.screen.blit(
                value_img,
                (
                    rect.right - 25
                    - value_img.get_width(),
                    y
                )
            )

            y += 27

    # ============================================================
    # DESENHAR
    # ============================================================

    def draw(self):

        data = self.stats.get_stats()

        # --------------------------------------------------------
        # TÍTULO
        # --------------------------------------------------------

        title = font(
            38,
            True
        ).render(
            "ESTATÍSTICAS",
            True,
            TEXT
        )

        self.screen.blit(
            title,
            (
                50,
                28
            )
        )

        subtitle = font(
            15
        ).render(
            "Seu desempenho no PixelForge",
            True,
            MUTED
        )

        self.screen.blit(
            subtitle,
            (
                53,
                72
            )
        )

        # --------------------------------------------------------
        # GERAL
        # --------------------------------------------------------

        general = data["general"]

        self.draw_card(
            pygame.Rect(
                50,
                115,
                300,
                205
            ),
            "GERAL",
            [
                (
                    "Partidas jogadas",
                    general["games_played"]
                ),
                (
                    "Vitórias",
                    general["wins"]
                ),
                (
                    "Derrotas",
                    general["losses"]
                ),
                (
                    "Empates",
                    general["draws"]
                )
            ]
        )

        # --------------------------------------------------------
        # PEDRA PAPEL TESOURA
        # --------------------------------------------------------

        ppt = data["rock_paper_scissors"]

        self.draw_card(
            pygame.Rect(
                370,
                115,
                300,
                205
            ),
            "PEDRA, PAPEL E TESOURA",
            [
                (
                    "Partidas",
                    ppt["played"]
                ),
                (
                    "Vitórias",
                    ppt["wins"]
                ),
                (
                    "Derrotas",
                    ppt["losses"]
                ),
                (
                    "Empates",
                    ppt["draws"]
                )
            ]
        )

        # --------------------------------------------------------
        # JOGO DA VELHA
        # --------------------------------------------------------

        velha = data["tic_tac_toe"]

        self.draw_card(
            pygame.Rect(
                690,
                115,
                300,
                205
            ),
            "JOGO DA VELHA",
            [
                (
                    "Partidas",
                    velha["played"]
                ),
                (
                    "Vitórias",
                    velha["wins"]
                ),
                (
                    "Derrotas",
                    velha["losses"]
                ),
                (
                    "Empates",
                    velha["draws"]
                )
            ]
        )

        # --------------------------------------------------------
        # FORCA
        # --------------------------------------------------------

        forca = data["hangman"]

        self.draw_card(
            pygame.Rect(
                210,
                345,
                300,
                205
            ),
            "FORCA",
            [
                (
                    "Partidas",
                    forca["played"]
                ),
                (
                    "Vitórias",
                    forca["wins"]
                ),
                (
                    "Derrotas",
                    forca["losses"]
                ),
                (
                    "Empates",
                    forca["draws"]
                )
            ]
        )

        # --------------------------------------------------------
        # SNAKE
        # --------------------------------------------------------

        snake = data["snake"]

        self.draw_card(
            pygame.Rect(
                570,
                345,
                300,
                205
            ),
            "SNAKE",
            [
                (
                    "Partidas",
                    snake["played"]
                ),
                (
                    "Melhor pontuação",
                    snake["best_score"]
                )
            ]
        )

        # --------------------------------------------------------
        # MENSAGEM DE RESET
        # --------------------------------------------------------

        if self.confirm_reset:

            message = font(
                14,
                True
            ).render(
                "Estatísticas resetadas.",
                True,
                ACCENT
            )

            self.screen.blit(
                message,
                message.get_rect(
                    center=(540, 600)
                )
            )

        # --------------------------------------------------------
        # BOTÃO VOLTAR
        # --------------------------------------------------------

        button(
            self.screen,
            self.back,
            "← VOLTAR",
            hover=self.hover_back
        )

        # --------------------------------------------------------
        # BOTÃO RESETAR
        # --------------------------------------------------------

        button(
            self.screen,
            self.reset,
            "RESETAR",
            hover=self.hover_reset
        )

        # --------------------------------------------------------
        # DICA
        # --------------------------------------------------------

        hint = font(
            13
        ).render(
            "ESC para voltar  •  R para resetar",
            True,
            MUTED
        )

        self.screen.blit(
            hint,
            hint.get_rect(
                center=(540, 680)
            )
        )