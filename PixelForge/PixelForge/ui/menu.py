import pygame

from ui.hud import (
    font,
    button,
    TEXT,
    MUTED,
    ACCENT
)


class MainMenu:

    def __init__(self, screen):

        self.screen = screen

        self.play_rect = pygame.Rect(
            390, 360, 320, 62
        )

        self.stats_rect = pygame.Rect(
            420, 440, 240, 52
        )

        self.quit_rect = pygame.Rect(
            450, 510, 200, 52
        )

        self.hover_play = False
        self.hover_stats = False
        self.hover_quit = False

    # ============================================================
    # EVENTOS
    # ============================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                return "play"

            if event.key == pygame.K_s:

                return "stats"

            if event.key == pygame.K_ESCAPE:

                return "quit"

        if event.type == pygame.MOUSEMOTION:

            self.hover_play = self.play_rect.collidepoint(
                event.pos
            )

            self.hover_stats = self.stats_rect.collidepoint(
                event.pos
            )

            self.hover_quit = self.quit_rect.collidepoint(
                event.pos
            )

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.play_rect.collidepoint(
                    event.pos
                ):

                    return "play"

                if self.stats_rect.collidepoint(
                    event.pos
                ):

                    return "stats"

                if self.quit_rect.collidepoint(
                    event.pos
                ):

                    return "quit"

        return None

    # ============================================================
    # DESENHAR
    # ============================================================

    def draw(self):

        w, h = self.screen.get_size()

        # --------------------------------------------------------
        # LOGO
        # --------------------------------------------------------

        logo = font(
            76,
            True
        ).render(
            "PIXELFORGE",
            True,
            TEXT
        )

        self.screen.blit(
            logo,
            logo.get_rect(
                center=(w // 2, 155)
            )
        )

        # --------------------------------------------------------
        # TAGLINE
        # --------------------------------------------------------

        line = font(
            20
        ).render(
            "BUILD. PLAY. CHALLENGE.",
            True,
            ACCENT
        )

        self.screen.blit(
            line,
            line.get_rect(
                center=(w // 2, 215)
            )
        )

        # --------------------------------------------------------
        # DESCRIÇÃO
        # --------------------------------------------------------

        desc = font(
            18
        ).render(
            "Uma plataforma de minijogos criada em Python + Pygame.",
            True,
            MUTED
        )

        self.screen.blit(
            desc,
            desc.get_rect(
                center=(w // 2, 265)
            )
        )

        # --------------------------------------------------------
        # JOGAR
        # --------------------------------------------------------

        button(
            self.screen,
            self.play_rect,
            "JOGAR AGORA",
            selected=True,
            hover=self.hover_play
        )

        icon_x = (
            self.play_rect.left + 42
        )

        icon_y = (
            self.play_rect.centery
        )

        pygame.draw.polygon(
            self.screen,
            (8, 10, 18),
            [
                (
                    icon_x - 6,
                    icon_y - 10
                ),
                (
                    icon_x - 6,
                    icon_y + 10
                ),
                (
                    icon_x + 9,
                    icon_y
                )
            ]
        )

        # --------------------------------------------------------
        # ESTATÍSTICAS
        # --------------------------------------------------------

        button(
            self.screen,
            self.stats_rect,
            "ESTATÍSTICAS",
            hover=self.hover_stats
        )

        # --------------------------------------------------------
        # SAIR
        # --------------------------------------------------------

        button(
            self.screen,
            self.quit_rect,
            "SAIR",
            hover=self.hover_quit
        )

        # --------------------------------------------------------
        # DICA
        # --------------------------------------------------------

        hint = font(
            14
        ).render(
            "ENTER para jogar  •  S para estatísticas  •  ESC para sair",
            True,
            MUTED
        )

        self.screen.blit(
            hint,
            hint.get_rect(
                center=(w // 2, 610)
            )
        )