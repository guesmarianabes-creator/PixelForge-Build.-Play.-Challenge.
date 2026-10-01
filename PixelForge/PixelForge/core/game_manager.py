import pygame

from core.stats_manager import StatsManager

from ui.menu import MainMenu
from ui.game_select import GameSelect
from ui.stats_screen import StatsScreen

from ui.hud import (
    draw_background,
    draw_header
)

from games.rock_paper_scissors import RockPaperScissors
from games.tic_tac_toe import TicTacToe
from games.hangman import Hangman
from games.snake import Snake


class GameManager:

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock

        # ========================================================
        # SISTEMA DE ESTATÍSTICAS
        # ========================================================

        self.stats = StatsManager()

        self.running = True

        # ========================================================
        # TELAS
        # ========================================================

        self.menu = MainMenu(
            screen
        )

        self.game_select = GameSelect(
            screen
        )

        self.stats_screen = StatsScreen(
            screen,
            self.stats
        )

        # ========================================================
        # ESTADO
        # ========================================================

        self.active_game = None

        self.state = "menu"

        # ========================================================
        # JOGOS
        # ========================================================

        self.games = {

            "ppt": RockPaperScissors,

            "velha": TicTacToe,

            "forca": Hangman,

            "snake": Snake
        }

    # ============================================================
    # INICIAR JOGO
    # ============================================================

    def start_game(self, game_id):

        # Todos os jogos recebem o StatsManager

        self.active_game = self.games[game_id](
            self.screen,
            self.stats
        )

        self.state = "game"

    # ============================================================
    # EVENTOS
    # ============================================================

    def handle_event(self, event):

        if event.type == pygame.QUIT:

            self.running = False

            return

        # ========================================================
        # MENU
        # ========================================================

        if self.state == "menu":

            action = self.menu.handle_event(
                event
            )

            if action == "play":

                self.state = "select"

            elif action == "stats":

                self.state = "stats"

            elif action == "quit":

                self.running = False

        # ========================================================
        # SELEÇÃO DE JOGO
        # ========================================================

        elif self.state == "select":

            action = self.game_select.handle_event(
                event
            )

            if action in self.games:

                self.start_game(
                    action
                )

            elif action == "back":

                self.state = "menu"

        # ========================================================
        # ESTATÍSTICAS
        # ========================================================

        elif self.state == "stats":

            action = self.stats_screen.handle_event(
                event
            )

            if action == "menu":

                self.state = "menu"

        # ========================================================
        # JOGO
        # ========================================================

        elif self.state == "game":

            action = self.active_game.handle_event(
                event
            )

            if action == "menu":

                self.active_game = None

                self.state = "select"

    # ============================================================
    # DESENHAR
    # ============================================================

    def draw(self):

        draw_background(
            self.screen
        )

        # --------------------------------------------------------
        # MENU
        # --------------------------------------------------------

        if self.state == "menu":

            self.menu.draw()

        # --------------------------------------------------------
        # SELEÇÃO
        # --------------------------------------------------------

        elif self.state == "select":

            draw_header(
                self.screen,
                "SELECT YOUR GAME"
            )

            self.game_select.draw()

        # --------------------------------------------------------
        # ESTATÍSTICAS
        # --------------------------------------------------------

        elif self.state == "stats":

            self.stats_screen.draw()

        # --------------------------------------------------------
        # JOGO
        # --------------------------------------------------------

        elif self.state == "game":

            self.active_game.draw()

        pygame.display.flip()

    # ============================================================
    # LOOP PRINCIPAL
    # ============================================================

    def run(self):

        while self.running:

            for event in pygame.event.get():

                self.handle_event(
                    event
                )

            if (
                self.state == "game"
                and self.active_game
            ):

                self.active_game.update()

            self.draw()

            self.clock.tick(60)