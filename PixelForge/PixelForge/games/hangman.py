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
    PANEL,
    PANEL_2,
    BG
)


class Hangman(BaseGame):

    # ============================================================
    # CONFIGURAÇÕES
    # ============================================================

    WORDS = [
        "PYTHON",
        "PYGAME",
        "ALGORITMO",
        "PIXEL",
        "COMPUTADOR",
        "PROGRAMACAO",
        "TECNOLOGIA",
        "SOFTWARE",
        "HARDWARE",
        "INTERNET",
        "DATABASE",
        "SISTEMA",
        "CODIGO",
        "PROGRAMA",
        "ENGENHARIA",
        "DADOS",
        "SERVIDOR",
        "MEMORIA",
        "PROCESSADOR",
    ]

    DIFFICULTIES = {
        "easy": {
            "name": "FÁCIL",
            "errors": 8,
            "description": "Mais chances para errar"
        },
        "medium": {
            "name": "MÉDIO",
            "errors": 6,
            "description": "Desafio equilibrado"
        },
        "hard": {
            "name": "DIFÍCIL",
            "errors": 5,
            "description": "Poucas chances"
        }
    }

    # ============================================================
    # INICIALIZAÇÃO
    # ============================================================

    def __init__(self, screen):
        self.screen = screen

        self.state = "difficulty"
        self.difficulty = None

        self.word = ""
        self.guessed = set()
        self.errors = 0
        self.max_errors = 6

        self.message = ""
        self.game_over = False
        self.won = False

        self.hint_used = False

        self.back = pygame.Rect(
            50, 620, 180, 48
        )

        self.hint_button = pygame.Rect(
            830, 510, 180, 50
        )

        self.difficulty_buttons = {
            "easy": pygame.Rect(120, 300, 250, 150),
            "medium": pygame.Rect(425, 300, 250, 150),
            "hard": pygame.Rect(730, 300, 250, 150)
        }

        self.hover_difficulty = None
        self.hover_hint = False

    # ============================================================
    # INICIAR PARTIDA
    # ============================================================

    def start_game(self, difficulty):

        self.difficulty = difficulty

        settings = self.DIFFICULTIES[difficulty]

        self.max_errors = settings["errors"]

        self.word = random.choice(self.WORDS)

        self.guessed = set()
        self.errors = 0

        self.message = "Digite uma letra para começar"

        self.game_over = False
        self.won = False
        self.hint_used = False

        self.state = "game"

    # ============================================================
    # EVENTOS
    # ============================================================

    def handle_event(self, event):

        # --------------------------------------------------------
        # TECLADO
        # --------------------------------------------------------

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if self.state == "difficulty":
                    return "menu"

                self.state = "difficulty"
                return None

            if self.state == "difficulty":
                return None

            if event.key == pygame.K_r:

                if self.difficulty:
                    self.start_game(self.difficulty)

                return None

            # ----------------------------------------------------
            # DIGITAR LETRA
            # ----------------------------------------------------

            if (
                pygame.K_a <= event.key <= pygame.K_z
                and not self.game_over
            ):

                letter = chr(event.key).upper()

                self.guess_letter(letter)

        # --------------------------------------------------------
        # MOUSE
        # --------------------------------------------------------

        if event.type == pygame.MOUSEMOTION:

            if self.state == "difficulty":

                self.hover_difficulty = None

                for difficulty, rect in self.difficulty_buttons.items():

                    if rect.collidepoint(event.pos):
                        self.hover_difficulty = difficulty

            else:

                self.hover_hint = (
                    self.hint_button.collidepoint(event.pos)
                    and not self.game_over
                    and not self.hint_used
                )

        # --------------------------------------------------------
        # CLIQUE
        # --------------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:
                return None

            # Tela de dificuldade
            if self.state == "difficulty":

                for difficulty, rect in self.difficulty_buttons.items():

                    if rect.collidepoint(event.pos):

                        self.start_game(difficulty)

                        return None

            # Jogo
            else:

                if self.back.collidepoint(event.pos):

                    self.state = "difficulty"

                    return None

                if (
                    self.hint_button.collidepoint(event.pos)
                    and not self.game_over
                    and not self.hint_used
                ):

                    self.use_hint()

        return None

    # ============================================================
    # JOGADA
    # ============================================================

    def guess_letter(self, letter):

        if letter in self.guessed:
            self.message = f"A letra {letter} já foi utilizada."
            return

        self.guessed.add(letter)

        if letter in self.word:

            self.message = f"A letra {letter} está na palavra!"

            if all(
                character in self.guessed
                for character in self.word
            ):

                self.won = True
                self.game_over = True

                self.message = (
                    "Você venceu! "
                    "Pressione R para jogar novamente."
                )

        else:

            self.errors += 1

            self.message = (
                f"A letra {letter} não está na palavra."
            )

            if self.errors >= self.max_errors:

                self.game_over = True
                self.won = False

                self.message = (
                    "Fim de jogo! "
                    "Pressione R para tentar novamente."
                )

    # ============================================================
    # SISTEMA DE DICA
    # ============================================================

    def use_hint(self):

        if self.hint_used or self.game_over:
            return

        hidden_letters = [
            letter
            for letter in self.word
            if letter not in self.guessed
        ]

        if not hidden_letters:
            return

        letter = random.choice(hidden_letters)

        self.guessed.add(letter)

        self.hint_used = True

        self.message = (
            f"Dica utilizada! A letra revelada foi {letter}."
        )

        if all(
            character in self.guessed
            for character in self.word
        ):

            self.won = True
            self.game_over = True

            self.message = (
                "Você venceu usando a dica! "
                "Pressione R para jogar novamente."
            )

    # ============================================================
    # UPDATE
    # ============================================================

    def update(self):
        pass

    # ============================================================
    # DESENHAR FORCA
    # ============================================================

    def draw_hangman(self):

        # Área da forca
        base_x = 120
        base_y = 500

        color = TEXT

        # Base
        pygame.draw.line(
            self.screen,
            color,
            (base_x, base_y),
            (base_x + 190, base_y),
            6
        )

        # Poste
        pygame.draw.line(
            self.screen,
            color,
            (base_x + 40, base_y),
            (base_x + 40, base_y - 270),
            6
        )

        # Topo
        pygame.draw.line(
            self.screen,
            color,
            (base_x + 40, base_y - 270),
            (base_x + 155, base_y - 270),
            6
        )

        # Corda
        pygame.draw.line(
            self.screen,
            MUTED,
            (base_x + 155, base_y - 270),
            (base_x + 155, base_y - 225),
            4
        )

        # --------------------------------------------------------
        # CABEÇA
        # --------------------------------------------------------

        if self.errors >= 1:

            pygame.draw.circle(
                self.screen,
                TEXT,
                (base_x + 155, base_y - 195),
                30,
                4
            )

        # --------------------------------------------------------
        # CORPO
        # --------------------------------------------------------

        if self.errors >= 2:

            pygame.draw.line(
                self.screen,
                TEXT,
                (base_x + 155, base_y - 165),
                (base_x + 155, base_y - 80),
                5
            )

        # --------------------------------------------------------
        # BRAÇO ESQUERDO
        # --------------------------------------------------------

        if self.errors >= 3:

            pygame.draw.line(
                self.screen,
                TEXT,
                (base_x + 155, base_y - 145),
                (base_x + 115, base_y - 105),
                5
            )

        # --------------------------------------------------------
        # BRAÇO DIREITO
        # --------------------------------------------------------

        if self.errors >= 4:

            pygame.draw.line(
                self.screen,
                TEXT,
                (base_x + 155, base_y - 145),
                (base_x + 195, base_y - 105),
                5
            )

        # --------------------------------------------------------
        # PERNA ESQUERDA
        # --------------------------------------------------------

        if self.errors >= 5:

            pygame.draw.line(
                self.screen,
                TEXT,
                (base_x + 155, base_y - 80),
                (base_x + 115, base_y - 30),
                5
            )

        # --------------------------------------------------------
        # PERNA DIREITA
        # --------------------------------------------------------

        if self.errors >= 6:

            pygame.draw.line(
                self.screen,
                TEXT,
                (base_x + 155, base_y - 80),
                (base_x + 195, base_y - 30),
                5
            )

        # --------------------------------------------------------
        # ERROS EXTRAS
        # --------------------------------------------------------

        if self.errors >= 7:

            pygame.draw.line(
                self.screen,
                DANGER,
                (base_x + 143, base_y - 205),
                (base_x + 151, base_y - 197),
                3
            )

            pygame.draw.line(
                self.screen,
                DANGER,
                (base_x + 151, base_y - 205),
                (base_x + 143, base_y - 197),
                3
            )

        if self.errors >= 8:

            pygame.draw.line(
                self.screen,
                DANGER,
                (base_x + 159, base_y - 205),
                (base_x + 167, base_y - 197),
                3
            )

            pygame.draw.line(
                self.screen,
                DANGER,
                (base_x + 167, base_y - 205),
                (base_x + 159, base_y - 197),
                3
            )

    # ============================================================
    # TELA DE DIFICULDADE
    # ============================================================

    def draw_difficulty(self):

        w, h = self.screen.get_size()

        # Título
        title = font(
            42,
            True
        ).render(
            "FORCA",
            True,
            TEXT
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(w // 2, 105)
            )
        )

        subtitle = font(
            18
        ).render(
            "Escolha o nível de dificuldade",
            True,
            MUTED
        )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(w // 2, 150)
            )
        )

        # Cards
        for difficulty, rect in self.difficulty_buttons.items():

            selected = (
                self.hover_difficulty == difficulty
            )

            color = (
                ACCENT
                if selected
                else PANEL_2
            )

            border = (
                ACCENT
                if selected
                else (48, 55, 78)
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=18
            )

            pygame.draw.rect(
                self.screen,
                border,
                rect,
                width=2,
                border_radius=18
            )

            settings = self.DIFFICULTIES[difficulty]

            name_color = (
                BG
                if selected
                else TEXT
            )

            desc_color = (
                BG
                if selected
                else MUTED
            )

            name = font(
                27,
                True
            ).render(
                settings["name"],
                True,
                name_color
            )

            self.screen.blit(
                name,
                name.get_rect(
                    center=(
                        rect.centerx,
                        rect.top + 48
                    )
                )
            )

            errors = font(
                20,
                True
            ).render(
                f"{settings['errors']} erros",
                True,
                name_color
            )

            self.screen.blit(
                errors,
                errors.get_rect(
                    center=(
                        rect.centerx,
                        rect.top + 87
                    )
                )
            )

            description = font(
                14
            ).render(
                settings["description"],
                True,
                desc_color
            )

            self.screen.blit(
                description,
                description.get_rect(
                    center=(
                        rect.centerx,
                        rect.top + 120
                    )
                )
            )

        # Rodapé
        hint = font(
            14
        ).render(
            "ESC para voltar ao menu",
            True,
            MUTED
        )

        self.screen.blit(
            hint,
            hint.get_rect(
                center=(w // 2, 585)
            )
        )

    # ============================================================
    # TELA DO JOGO
    # ============================================================

    def draw_game(self):

        w, h = self.screen.get_size()

        # --------------------------------------------------------
        # CABEÇALHO
        # --------------------------------------------------------

        title = font(
            34,
            True
        ).render(
            "FORCA",
            True,
            TEXT
        )

        self.screen.blit(
            title,
            (55, 30)
        )

        difficulty_name = self.DIFFICULTIES[
            self.difficulty
        ]["name"]

        difficulty_img = font(
            15,
            True
        ).render(
            difficulty_name,
            True,
            ACCENT
        )

        self.screen.blit(
            difficulty_img,
            (58, 72)
        )

        # --------------------------------------------------------
        # ERROS
        # --------------------------------------------------------

        error_color = (
            DANGER
            if self.errors >= self.max_errors - 2
            else ACCENT
        )

        errors_img = font(
            21,
            True
        ).render(
            f"ERROS  {self.errors}/{self.max_errors}",
            True,
            error_color
        )

        self.screen.blit(
            errors_img,
            (820, 45)
        )

        # --------------------------------------------------------
        # FORCA
        # --------------------------------------------------------

        self.draw_hangman()

        # --------------------------------------------------------
        # PALAVRA
        # --------------------------------------------------------

        display = " ".join(
            character
            if character in self.guessed
            else "_"
            for character in self.word
        )

        word_img = font(
            38,
            True
        ).render(
            display,
            True,
            TEXT
        )

        self.screen.blit(
            word_img,
            word_img.get_rect(
                center=(730, 190)
            )
        )

        # --------------------------------------------------------
        # LETRAS UTILIZADAS
        # --------------------------------------------------------

        guessed_text = (
            "LETRAS USADAS  "
            + " ".join(
                sorted(self.guessed)
            )
            if self.guessed
            else "LETRAS USADAS  —"
        )

        guessed_img = font(
            16
        ).render(
            guessed_text,
            True,
            MUTED
        )

        self.screen.blit(
            guessed_img,
            guessed_img.get_rect(
                center=(730, 260)
            )
        )

        # --------------------------------------------------------
        # MENSAGEM
        # --------------------------------------------------------

        if self.won:

            message_color = ACCENT

        elif self.game_over:

            message_color = DANGER

        else:

            message_color = TEXT

        msg = font(
            18,
            True
        ).render(
            self.message,
            True,
            message_color
        )

        self.screen.blit(
            msg,
            msg.get_rect(
                center=(730, 330)
            )
        )

        # --------------------------------------------------------
        # RESULTADO
        # --------------------------------------------------------

        if self.game_over:

            if self.won:

                result_text = "VOCÊ VENCEU!"

                result_color = ACCENT

            else:

                result_text = f"A PALAVRA ERA: {self.word}"

                result_color = DANGER

            result = font(
                27,
                True
            ).render(
                result_text,
                True,
                result_color
            )

            self.screen.blit(
                result,
                result.get_rect(
                    center=(730, 400)
                )
            )

        # --------------------------------------------------------
        # DICA
        # --------------------------------------------------------

        hint_color = (
            ACCENT_2
            if not self.hint_used and not self.game_over
            else PANEL_2
        )

        pygame.draw.rect(
            self.screen,
            hint_color,
            self.hint_button,
            border_radius=12
        )

        hint_text_color = (
            BG
            if not self.hint_used and not self.game_over
            else MUTED
        )

        hint_text = font(
            17,
            True
        ).render(
            "USAR DICA",
            True,
            hint_text_color
        )

        self.screen.blit(
            hint_text,
            hint_text.get_rect(
                center=self.hint_button.center
            )
        )

        # --------------------------------------------------------
        # MENU
        # --------------------------------------------------------

        button(
            self.screen,
            self.back,
            "← VOLTAR"
        )

        # --------------------------------------------------------
        # RODAPÉ
        # --------------------------------------------------------

        footer = font(
            14
        ).render(
            "Digite letras pelo teclado  •  R para reiniciar  •  ESC para voltar",
            True,
            MUTED
        )

        self.screen.blit(
            footer,
            footer.get_rect(
                center=(w // 2, 670)
            )
        )

    # ============================================================
    # DRAW
    # ============================================================

    def draw(self):

        self.screen.fill(BG)

        if self.state == "difficulty":

            self.draw_difficulty()

        elif self.state == "game":

            self.draw_game()