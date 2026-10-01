import random
import pygame

from games.base import BaseGame

from ui.hud import (
    font,
    TEXT,
    MUTED,
    ACCENT,
    button
)

from network.multiplayer import MultiplayerClient


class RockPaperScissors(BaseGame):

    choices = [
        "Pedra",
        "Papel",
        "Tesoura"
    ]

    def __init__(
        self,
        screen,
        stats=None
    ):

        self.screen = screen

        self.stats = stats

        self.mode = "cpu"

        self.network = None

        self.player_id = None

        self.player = None

        self.opponent = None

        self.cpu = None

        self.result = (
            "Escolha sua jogada!"
        )

        self.status = (
            "Modo solo contra a máquina"
        )

        self.round_number = 1

        self.round_recorded = False

        self.hover_multi = False

        self.hover_back = False

        self.back = pygame.Rect(
            50,
            620,
            180,
            48
        )

        self.multi_button = pygame.Rect(
            790,
            40,
            260,
            48
        )

    # ==================================================
    # MULTIPLAYER
    # ==================================================

    def start_multiplayer(self):

        if self.network:

            self.network.close()

        self.network = MultiplayerClient()

        self.result = (
            "Conectando..."
        )

        self.status = (
            "Conectando ao servidor..."
        )

        if self.network.connect():

            self.mode = "multi"

            self.player = None

            self.opponent = None

            self.cpu = None

            self.round_recorded = False

            self.result = (
                "Aguardando jogador..."
            )

            self.status = (
                "Entrando na partida..."
            )

        else:

            self.network = None

            self.mode = "cpu"

            self.result = (
                "Servidor não encontrado."
            )

            self.status = (
                "Inicie o server.py antes."
            )

    def stop_multiplayer(self):

        if self.network:

            self.network.close()

        self.network = None

        self.mode = "cpu"

        self.player = None

        self.opponent = None

        self.cpu = None

        self.result = (
            "Escolha sua jogada!"
        )

        self.status = (
            "Modo solo contra a máquina"
        )

    # ==================================================
    # RESULTADO
    # ==================================================

    def get_result(
        self,
        player_choice,
        opponent_choice
    ):

        if player_choice == opponent_choice:

            return "draw"

        if (
            player_choice,
            opponent_choice
        ) in [

            ("Pedra", "Tesoura"),

            ("Papel", "Pedra"),

            ("Tesoura", "Papel")

        ]:

            return "win"

        return "loss"

    def register_result(
        self,
        result
    ):

        if self.round_recorded:

            return

        self.round_recorded = True

        if not self.stats:

            return

        if result == "win":

            self.stats.record_win(
                "rock_paper_scissors"
            )

        elif result == "loss":

            self.stats.record_loss(
                "rock_paper_scissors"
            )

        elif result == "draw":

            self.stats.record_draw(
                "rock_paper_scissors"
            )

    # ==================================================
    # CPU
    # ==================================================

    def play_cpu(
        self,
        choice
    ):

        self.player = choice

        self.cpu = random.choice(
            self.choices
        )

        result = self.get_result(
            self.player,
            self.cpu
        )

        self.register_result(
            result
        )

        if result == "win":

            self.result = (
                "Você venceu!"
            )

        elif result == "loss":

            self.result = (
                "A máquina venceu!"
            )

        else:

            self.result = (
                "Empate!"
            )

        self.status = (
            "Escolha novamente para "
            "jogar outra rodada."
        )

    # ==================================================
    # MULTIPLAYER
    # ==================================================

    def play_multiplayer(
        self,
        choice
    ):

        if not self.network:

            return

        if not self.network.connected:

            return

        if self.player is not None:

            return

        self.player = choice

        self.result = (
            "Jogada enviada!"
        )

        self.status = (
            "Aguardando o adversário..."
        )

        self.network.send(
            {
                "type": "rps_choice",
                "choice": choice
            }
        )

    # ==================================================
    # REDE
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

            # ------------------------------------------
            # IDENTIFICAÇÃO
            # ------------------------------------------

            if message_type == "welcome":

                self.player_id = message.get(
                    "player"
                )

                self.status = (
                    f"Você é o Jogador "
                    f"{self.player_id}. "
                    "Aguardando adversário..."
                )

            # ------------------------------------------
            # JOGADOR ENTROU
            # ------------------------------------------

            elif message_type == "player_joined":

                player = message.get(
                    "player"
                )

                if player != self.player_id:

                    self.status = (
                        "Adversário conectado. "
                        "Escolha sua jogada!"
                    )

            # ------------------------------------------
            # AGUARDANDO
            # ------------------------------------------

            elif message_type == "rps_waiting":

                self.status = (
                    "Sua jogada foi enviada. "
                    "Aguardando o adversário..."
                )

            # ------------------------------------------
            # RESULTADO DA RODADA
            # ------------------------------------------

            elif message_type == "rps_result":

                player1_choice = message.get(
                    "player1_choice"
                )

                player2_choice = message.get(
                    "player2_choice"
                )

                result = message.get(
                    "result"
                )

                if self.player_id == 1:

                    self.opponent = (
                        player2_choice
                    )

                    if result == "player1":

                        local_result = "win"

                    elif result == "player2":

                        local_result = "loss"

                    else:

                        local_result = "draw"

                else:

                    self.opponent = (
                        player1_choice
                    )

                    if result == "player2":

                        local_result = "win"

                    elif result == "player1":

                        local_result = "loss"

                    else:

                        local_result = "draw"

                self.register_result(
                    local_result
                )

                if local_result == "win":

                    self.result = (
                        "Você venceu!"
                    )

                elif local_result == "loss":

                    self.result = (
                        "O adversário venceu!"
                    )

                else:

                    self.result = (
                        "Empate!"
                    )

                self.status = (
                    "Rodada finalizada. "
                    "Escolha novamente!"
                )

            # ------------------------------------------
            # ADVERSÁRIO SAIU
            # ------------------------------------------

            elif message_type == "player_left":

                self.opponent = None

                self.player = None

                self.result = (
                    "Partida encerrada."
                )

                self.status = (
                    "O adversário saiu."
                )

                self.round_recorded = False

    # ==================================================
    # NOVA RODADA
    # ==================================================

    def start_new_round(self):

        self.player = None

        self.opponent = None

        self.cpu = None

        self.round_recorded = False

        self.result = (
            "Escolha sua jogada!"
        )

        if self.mode == "multi":

            self.status = (
                "Escolha sua jogada."
            )

        else:

            self.status = (
                "Modo solo contra a máquina"
            )

    # ==================================================
    # EVENTOS
    # ==================================================

    def handle_event(
        self,
        event
    ):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self.network:

                    self.network.close()

                return "menu"

            if event.key == pygame.K_m:

                if self.mode == "cpu":

                    self.start_multiplayer()

                return None

            if event.key == pygame.K_c:

                if self.mode == "multi":

                    self.stop_multiplayer()

                return None

        if event.type == pygame.MOUSEMOTION:

            self.hover_multi = (
                self.multi_button.collidepoint(
                    event.pos
                )
            )

            self.hover_back = (
                self.back.collidepoint(
                    event.pos
                )
            )

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:

                return None

            if self.back.collidepoint(
                event.pos
            ):

                if self.network:

                    self.network.close()

                return "menu"

            if self.multi_button.collidepoint(
                event.pos
            ):

                if self.mode == "cpu":

                    self.start_multiplayer()

                else:

                    self.stop_multiplayer()

                return None

            for i, choice in enumerate(
                self.choices
            ):

                rect = pygame.Rect(
                    120 + i * 300,
                    430,
                    260,
                    65
                )

                if rect.collidepoint(
                    event.pos
                ):

                    if self.mode == "multi":

                        self.play_multiplayer(
                            choice
                        )

                    else:

                        if self.player is not None:

                            self.start_new_round()

                        self.play_cpu(
                            choice
                        )

                    return None

        return None

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.mode == "multi":

            self.process_network()

    # ==================================================
    # DESENHO
    # ==================================================

    def draw(self):

        self.screen.fill(
            (8, 10, 18)
        )

        if self.mode == "multi":

            subtitle = (
                "Duelo multiplayer"
            )

        else:

            subtitle = (
                "Duelo contra a máquina"
            )

        self.draw_title(
            self.screen,
            "PEDRA, PAPEL E TESOURA",
            subtitle
        )

        # ----------------------------------------------
        # MULTIPLAYER
        # ----------------------------------------------

        if self.mode == "cpu":

            button(
                self.screen,
                self.multi_button,
                "MULTIPLAYER  [M]",
                hover=self.hover_multi
            )

        else:

            button(
                self.screen,
                self.multi_button,
                "SAIR DO MULTIPLAYER  [C]",
                hover=self.hover_multi
            )

        # ----------------------------------------------
        # JOGADOR
        # ----------------------------------------------

        if self.mode == "multi":

            if self.player_id:

                player_text = font(
                    18,
                    True
                ).render(
                    f"JOGADOR {self.player_id}",
                    True,
                    ACCENT
                )

                self.screen.blit(
                    player_text,
                    (
                        50,
                        125
                    )
                )

        # ----------------------------------------------
        # ESCOLHAS
        # ----------------------------------------------

        if self.player:

            if self.mode == "cpu":

                label = (
                    f"Você: {self.player}    "
                    f"Máquina: {self.cpu}"
                )

            else:

                if self.opponent:

                    label = (
                        f"Você: {self.player}    "
                        f"Adversário: "
                        f"{self.opponent}"
                    )

                else:

                    label = (
                        f"Você: {self.player}    "
                        "Adversário: aguardando..."
                    )

            txt = font(
                22,
                True
            ).render(
                label,
                True,
                TEXT
            )

            self.screen.blit(
                txt,
                txt.get_rect(
                    center=(550, 180)
                )
            )

        # ----------------------------------------------
        # RESULTADO
        # ----------------------------------------------

        result = font(
            34,
            True
        ).render(
            self.result,
            True,
            ACCENT
        )

        self.screen.blit(
            result,
            result.get_rect(
                center=(550, 270)
            )
        )

        # ----------------------------------------------
        # STATUS
        # ----------------------------------------------

        status = font(
            16
        ).render(
            self.status,
            True,
            MUTED
        )

        self.screen.blit(
            status,
            status.get_rect(
                center=(550, 330)
            )
        )

        # ----------------------------------------------
        # BOTÕES
        # ----------------------------------------------

        for i, choice in enumerate(
            self.choices
        ):

            rect = pygame.Rect(
                120 + i * 300,
                430,
                260,
                65
            )

            button(
                self.screen,
                rect,
                choice
            )

        # ----------------------------------------------
        # VOLTAR
        # ----------------------------------------------

        button(
            self.screen,
            self.back,
            "← MENU",
            hover=self.hover_back
        )