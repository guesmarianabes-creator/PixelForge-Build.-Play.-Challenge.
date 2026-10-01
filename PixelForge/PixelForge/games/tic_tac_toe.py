import random
import pygame

from games.base import BaseGame

from ui.hud import (
    font,
    button,
    TEXT,
    MUTED,
    ACCENT,
    ACCENT_2,
    DANGER,
    PANEL_2
)

from network.multiplayer import MultiplayerClient


class TicTacToe(BaseGame):

    def __init__(self, screen, stats=None):

        self.screen = screen
        self.stats = stats

        # ==================================================
        # MODO
        # ==================================================

        self.mode = "cpu"

        self.network = None
        self.player_id = None

        # ==================================================
        # TABULEIRO
        # ==================================================

        self.board = [""] * 9

        self.player = "X"
        self.machine = "O"

        self.current_player = "X"

        self.difficulty = None

        self.result = ""

        self.thinking = False
        self.thinking_timer = 0

        # ==================================================
        # MULTIPLAYER
        # ==================================================

        self.multiplayer_ready = False

        self.multiplayer_result_recorded = False

        self.status = ""

        # ==================================================
        # TABULEIRO
        # ==================================================

        self.cell_size = 120

        self.board_x = 300
        self.board_y = 150

        self.cells = []

        for row in range(3):

            for col in range(3):

                rect = pygame.Rect(
                    self.board_x + col * self.cell_size,
                    self.board_y + row * self.cell_size,
                    self.cell_size - 5,
                    self.cell_size - 5
                )

                self.cells.append(rect)

        # ==================================================
        # DIFICULDADE
        # ==================================================

        self.difficulty_rects = {

            "FACIL": pygame.Rect(
                180,
                210,
                180,
                60
            ),

            "MEDIO": pygame.Rect(
                390,
                210,
                180,
                60
            ),

            "DIFICIL": pygame.Rect(
                600,
                210,
                180,
                60
            )
        }

        # ==================================================
        # MULTIPLAYER
        # ==================================================

        self.multiplayer_rect = pygame.Rect(
            390,
            300,
            240,
            55
        )

        # ==================================================
        # BOTÕES
        # ==================================================

        self.back_rect = pygame.Rect(
            50,
            540,
            180,
            50
        )

        self.reset_rect = pygame.Rect(
            700,
            540,
            180,
            50
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.board = [""] * 9

        self.current_player = "X"

        self.result = ""

        self.thinking = False

        self.thinking_timer = 0

        self.multiplayer_result_recorded = False

        if self.mode == "multi":

            if self.player_id == 1:

                self.status = (
                    "Sua vez — você é X"
                )

            else:

                self.status = (
                    "Aguardando Jogador 1..."
                )

    # ==================================================
    # VERIFICAR VENCEDOR
    # ==================================================

    def check_winner(self, board=None):

        if board is None:

            board = self.board

        combinations = [

            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            (0, 4, 8),
            (2, 4, 6)
        ]

        for a, b, c in combinations:

            if (
                board[a]
                and board[a] == board[b]
                and board[a] == board[c]
            ):

                return board[a]

        if "" not in board:

            return "DRAW"

        return None

    # ==================================================
    # MOVIMENTOS DISPONÍVEIS
    # ==================================================

    def available_moves(self, board=None):

        if board is None:

            board = self.board

        return [
            i
            for i, value in enumerate(board)
            if value == ""
        ]

    # ==================================================
    # MOVIMENTO DA MÁQUINA
    # ==================================================

    def machine_move(self):

        moves = self.available_moves()

        if not moves:

            return None

        # ==================================================
        # FÁCIL
        # ==================================================

        if self.difficulty == "FACIL":

            return random.choice(moves)

        # ==================================================
        # MÉDIO
        # ==================================================

        if self.difficulty == "MEDIO":

            # Tenta ganhar

            for move in moves:

                test_board = self.board.copy()

                test_board[move] = self.machine

                if self.check_winner(
                    test_board
                ) == self.machine:

                    return move

            # Tenta bloquear

            for move in moves:

                test_board = self.board.copy()

                test_board[move] = self.player

                if self.check_winner(
                    test_board
                ) == self.player:

                    return move

            # Centro

            if 4 in moves:

                return 4

            # Cantos

            corners = [
                move
                for move in moves
                if move in [0, 2, 6, 8]
            ]

            if corners:

                return random.choice(
                    corners
                )

            return random.choice(moves)

        # ==================================================
        # DIFÍCIL
        # ==================================================

        best_score = -1000

        best_move = None

        for move in moves:

            test_board = self.board.copy()

            test_board[move] = self.machine

            score = self.minimax(
                test_board,
                False
            )

            if score > best_score:

                best_score = score

                best_move = move

        return best_move

    # ==================================================
    # MINIMAX
    # ==================================================

    def minimax(self, board, maximizing):

        winner = self.check_winner(board)

        if winner == self.machine:

            return 10

        if winner == self.player:

            return -10

        if winner == "DRAW":

            return 0

        moves = self.available_moves(board)

        if maximizing:

            best_score = -1000

            for move in moves:

                new_board = board.copy()

                new_board[move] = self.machine

                score = self.minimax(
                    new_board,
                    False
                )

                best_score = max(
                    best_score,
                    score
                )

            return best_score

        best_score = 1000

        for move in moves:

            new_board = board.copy()

            new_board[move] = self.player

            score = self.minimax(
                new_board,
                True
            )

            best_score = min(
                best_score,
                score
            )

        return best_score

    # ==================================================
    # REGISTRAR RESULTADO - CPU
    # ==================================================

    def register_result(self, result):

        if not self.stats:

            return

        if result == self.player:

            self.stats.record_win(
                "tic_tac_toe"
            )

        elif result == self.machine:

            self.stats.record_loss(
                "tic_tac_toe"
            )

        elif result == "DRAW":

            self.stats.record_draw(
                "tic_tac_toe"
            )

    # ==================================================
    # REGISTRAR RESULTADO - MULTIPLAYER
    # ==================================================

    def register_multiplayer_result(
        self,
        result
    ):

        if self.multiplayer_result_recorded:

            return

        self.multiplayer_result_recorded = True

        if not self.stats:

            return

        if result == "win":

            self.stats.record_win(
                "tic_tac_toe"
            )

        elif result == "loss":

            self.stats.record_loss(
                "tic_tac_toe"
            )

        elif result == "draw":

            self.stats.record_draw(
                "tic_tac_toe"
            )

    # ==================================================
    # INICIAR MULTIPLAYER
    # ==================================================

    def start_multiplayer(self):

        if self.network:

            self.network.close()

        self.network = MultiplayerClient()

        self.mode = "multi"

        self.player_id = None

        self.multiplayer_ready = False

        self.multiplayer_result_recorded = False

        self.board = [""] * 9

        self.result = ""

        self.current_player = "X"

        self.status = (
            "Conectando ao servidor..."
        )

        if not self.network.connect():

            self.network = None

            self.mode = "cpu"

            self.status = ""

            self.result = (
                "Servidor não encontrado."
            )

    # ==================================================
    # SAIR DO MULTIPLAYER
    # ==================================================

    def stop_multiplayer(self):

        if self.network:

            self.network.close()

        self.network = None

        self.mode = "cpu"

        self.player_id = None

        self.multiplayer_ready = False

        self.board = [""] * 9

        self.result = ""

        self.difficulty = None

        self.status = ""

    # ==================================================
    # PROCESSAR REDE
    # ==================================================

    def process_network(self):

        if not self.network:

            return

        messages = (
            self.network.get_messages()
        )

        for message in messages:

            message_type = message.get(
                "type"
            )

            # ==================================================
            # WELCOME
            # ==================================================

            if message_type == "welcome":

                self.player_id = message.get(
                    "player"
                )

                if self.player_id == 1:

                    self.player = "X"

                    self.status = (
                        "Você é X — sua vez!"
                    )

                else:

                    self.player = "O"

                    self.status = (
                        "Você é O — "
                        "aguardando sua vez..."
                    )

            # ==================================================
            # JOGADOR ENTROU
            # ==================================================

            elif message_type == "player_joined":

                if self.player_id == 1:

                    self.status = (
                        "Adversário conectado. "
                        "Sua vez!"
                    )

                else:

                    self.status = (
                        "Adversário conectado. "
                        "Aguardando sua vez..."
                    )

            # ==================================================
            # ESTADO DO JOGO
            # ==================================================

            elif message_type == "ttt_state":

                board = message.get(
                    "board"
                )

                current = message.get(
                    "current_player"
                )

                if isinstance(
                    board,
                    list
                ) and len(board) == 9:

                    self.board = board

                self.current_player = current

                self.result = ""

                if self.current_player == self.player:

                    self.status = (
                        "Sua vez!"
                    )

                else:

                    self.status = (
                        "Vez do adversário..."
                    )

            # ==================================================
            # RESULTADO
            # ==================================================

            elif message_type == "ttt_result":

                winner = message.get(
                    "winner"
                )

                board = message.get(
                    "board"
                )

                if isinstance(
                    board,
                    list
                ) and len(board) == 9:

                    self.board = board

                if winner == "DRAW":

                    self.result = "DRAW"

                    self.status = "Empate!"

                    self.register_multiplayer_result(
                        "draw"
                    )

                elif winner == self.player:

                    self.result = winner

                    self.status = "VOCÊ VENCEU!"

                    self.register_multiplayer_result(
                        "win"
                    )

                else:

                    self.result = winner

                    self.status = (
                        "O ADVERSÁRIO VENCEU!"
                    )

                    self.register_multiplayer_result(
                        "loss"
                    )

            # ==================================================
            # ADVERSÁRIO SAIU
            # ==================================================

            elif message_type == "player_left":

                self.result = ""

                self.status = (
                    "O adversário saiu."
                )

                self.board = [""] * 9

                self.player_id = None

    # ==================================================
    # EVENTOS
    # ==================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            # ESC = sair

            if event.key == pygame.K_ESCAPE:

                if self.network:

                    self.network.close()

                return "menu"

            # R = reiniciar CPU

            if event.key == pygame.K_r:

                if self.mode == "cpu":

                    self.reset()

            # M = multiplayer

            if event.key == pygame.K_m:

                if self.mode == "cpu":

                    self.start_multiplayer()

            # C = voltar para CPU

            if event.key == pygame.K_c:

                if self.mode == "multi":

                    self.stop_multiplayer()

        # ==================================================
        # MOUSE
        # ==================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:

                return None

            # ==================================================
            # ESCOLHA DE MODO
            # ==================================================

            if (
                not self.difficulty
                and self.mode == "cpu"
            ):

                # Dificuldade

                for difficulty, rect in (
                    self.difficulty_rects.items()
                ):

                    if rect.collidepoint(
                        event.pos
                    ):

                        self.difficulty = difficulty

                        self.reset()

                        return None

                # Multiplayer

                if self.multiplayer_rect.collidepoint(
                    event.pos
                ):

                    self.start_multiplayer()

                    return None

            # ==================================================
            # MULTIPLAYER
            # ==================================================

            if self.mode == "multi":

                # Voltar

                if self.back_rect.collidepoint(
                    event.pos
                ):

                    if self.network:

                        self.network.close()

                    return "menu"

                # Reiniciar

                if self.reset_rect.collidepoint(
                    event.pos
                ):

                    if self.network:

                        self.network.send(
                            {
                                "type": "ttt_reset"
                            }
                        )

                    return None

                # Não pode jogar depois do resultado

                if self.result:

                    return None

                # Ainda não recebeu o ID

                if self.player_id is None:

                    return None

                # Não é sua vez

                if self.current_player != self.player:

                    return None

                # Escolher casa

                for index, rect in enumerate(
                    self.cells
                ):

                    if (
                        rect.collidepoint(
                            event.pos
                        )
                        and self.board[index] == ""
                    ):

                        self.network.send(
                            {
                                "type": "ttt_move",
                                "position": index
                            }
                        )

                        return None

                return None

            # ==================================================
            # JOGO CONTRA MÁQUINA
            # ==================================================

            if (
                self.difficulty
                and not self.result
                and not self.thinking
                and self.current_player == self.player
            ):

                for index, rect in enumerate(
                    self.cells
                ):

                    if (
                        rect.collidepoint(
                            event.pos
                        )
                        and self.board[index] == ""
                    ):

                        self.board[index] = self.player

                        winner = self.check_winner()

                        if winner:

                            self.result = winner

                            self.register_result(
                                winner
                            )

                        else:

                            self.current_player = self.machine

                            self.thinking = True

                            self.thinking_timer = 35

                        return None

            # ==================================================
            # VOLTAR
            # ==================================================

            if self.back_rect.collidepoint(
                event.pos
            ):

                return "menu"

            # ==================================================
            # REINICIAR
            # ==================================================

            if self.reset_rect.collidepoint(
                event.pos
            ):

                self.reset()

        return None

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.mode == "multi":

            self.process_network()

            return

        if not self.thinking:

            return

        self.thinking_timer -= 1

        if self.thinking_timer <= 0:

            move = self.machine_move()

            if move is not None:

                self.board[move] = self.machine

            winner = self.check_winner()

            if winner:

                self.result = winner

                self.register_result(
                    winner
                )

                self.thinking = False

                return

            self.current_player = self.player

            self.thinking = False

    # ==================================================
    # DESENHAR TABULEIRO
    # ==================================================

    def draw_board(self):

        for index, rect in enumerate(
            self.cells
        ):

            can_play = (
                self.mode == "multi"
                and self.player_id
                and self.current_player == self.player
            ) or (
                self.mode == "cpu"
                and self.current_player == self.player
            )

            hover = (
                rect.collidepoint(
                    pygame.mouse.get_pos()
                )
                and not self.result
                and not self.thinking
                and self.board[index] == ""
                and can_play
            )

            if hover:

                color = (
                    40,
                    48,
                    72
                )

            else:

                color = PANEL_2

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                (
                    48,
                    55,
                    78
                ),
                rect,
                width=1,
                border_radius=12
            )

            value = self.board[index]

            if value == "X":

                img = font(
                    50,
                    True
                ).render(
                    "X",
                    True,
                    ACCENT
                )

                self.screen.blit(
                    img,
                    img.get_rect(
                        center=rect.center
                    )
                )

            elif value == "O":

                img = font(
                    50,
                    True
                ).render(
                    "O",
                    True,
                    ACCENT_2
                )

                self.screen.blit(
                    img,
                    img.get_rect(
                        center=rect.center
                    )
                )

    # ==================================================
    # DESENHO
    # ==================================================

    def draw(self):

        w, h = self.screen.get_size()

        # ==================================================
        # ESCOLHA DE MODO
        # ==================================================

        if (
            not self.difficulty
            and self.mode == "cpu"
        ):

            title = font(
                34,
                True
            ).render(
                "JOGO DA VELHA",
                True,
                TEXT
            )

            self.screen.blit(
                title,
                title.get_rect(
                    center=(w // 2, 100)
                )
            )

            subtitle = font(
                17
            ).render(
                "Escolha a dificuldade ou jogue multiplayer",
                True,
                MUTED
            )

            self.screen.blit(
                subtitle,
                subtitle.get_rect(
                    center=(w // 2, 145)
                )
            )

            for difficulty, rect in (
                self.difficulty_rects.items()
            ):

                hover = rect.collidepoint(
                    pygame.mouse.get_pos()
                )

                button(
                    self.screen,
                    rect,
                    difficulty,
                    hover=hover
                )

            hover_multi = (
                self.multiplayer_rect.collidepoint(
                    pygame.mouse.get_pos()
                )
            )

            button(
                self.screen,
                self.multiplayer_rect,
                "MULTIPLAYER",
                hover=hover_multi
            )

            return

        # ==================================================
        # CABEÇALHO
        # ==================================================

        title = font(
            32,
            True
        ).render(
            "JOGO DA VELHA",
            True,
            TEXT
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(w // 2, 45)
            )
        )

        if self.mode == "multi":

            subtitle = font(
                15,
                True
            ).render(
                "MULTIPLAYER",
                True,
                ACCENT
            )

        else:

            subtitle = font(
                15,
                True
            ).render(
                f"DIFICULDADE: {self.difficulty}",
                True,
                ACCENT
            )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(w // 2, 80)
            )
        )

        # ==================================================
        # STATUS
        # ==================================================

        if self.mode == "multi":

            status_text = self.status

            if self.result == "DRAW":

                status_color = MUTED

            elif self.result == self.player:

                status_color = ACCENT

            elif self.result:

                status_color = DANGER

            else:

                status_color = TEXT

        else:

            if self.thinking:

                status_text = (
                    "A máquina está pensando..."
                )

                status_color = ACCENT_2

            elif self.result == self.player:

                status_text = "VOCÊ VENCEU!"

                status_color = ACCENT

            elif self.result == self.machine:

                status_text = "A MÁQUINA VENCEU!"

                status_color = DANGER

            elif self.result == "DRAW":

                status_text = "EMPATE!"

                status_color = MUTED

            elif self.current_player == self.player:

                status_text = "SUA VEZ"

                status_color = TEXT

            else:

                status_text = "VEZ DA MÁQUINA"

                status_color = MUTED

        status = font(
            20,
            True
        ).render(
            status_text,
            True,
            status_color
        )

        self.screen.blit(
            status,
            status.get_rect(
                center=(w // 2, 110)
            )
        )

        # ==================================================
        # TABULEIRO
        # ==================================================

        self.draw_board()

        # ==================================================
        # BOTÕES
        # ==================================================

        button(
            self.screen,
            self.back_rect,
            "VOLTAR",
            hover=self.back_rect.collidepoint(
                pygame.mouse.get_pos()
            )
        )

        button(
            self.screen,
            self.reset_rect,
            "REINICIAR",
            hover=self.reset_rect.collidepoint(
                pygame.mouse.get_pos()
            )
        )

        if self.mode == "multi":

            hint = font(
                13
            ).render(
                "ESC para sair do multiplayer",
                True,
                MUTED
            )

            self.screen.blit(
                hint,
                hint.get_rect(
                    center=(540, 620)
                )
            )