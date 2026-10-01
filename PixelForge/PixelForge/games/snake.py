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


class Snake(BaseGame):

    # ============================================================
    # CONFIGURAÇÕES
    # ============================================================

    CELL = 25
    COLS = 28
    ROWS = 18

    DIFFICULTIES = {
        "easy": {
            "name": "FÁCIL",
            "delay": 9,
            "description": "Velocidade reduzida"
        },
        "medium": {
            "name": "MÉDIO",
            "delay": 6,
            "description": "Desafio equilibrado"
        },
        "hard": {
            "name": "DIFÍCIL",
            "delay": 4,
            "description": "Velocidade máxima"
        }
    }

    # ============================================================
    # INICIALIZAÇÃO
    # ============================================================

    def __init__(self, screen, stats=None):

        self.screen = screen
        self.stats = stats

        self.state = "difficulty"
        self.difficulty = None

        self.snake = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.food = None

        self.score = 0
        self.best_score = 0

        self.dead = False

        # Evita registrar a mesma partida duas vezes
        self.stats_recorded = False

        self.timer = 0
        self.move_delay = 6

        self.back = pygame.Rect(
            50, 620, 180, 48
        )

        self.difficulty_buttons = {
            "easy": pygame.Rect(
                120, 300, 250, 150
            ),

            "medium": pygame.Rect(
                425, 300, 250, 150
            ),

            "hard": pygame.Rect(
                730, 300, 250, 150
            )
        }

        self.hover_difficulty = None

    # ============================================================
    # INICIAR JOGO
    # ============================================================

    def start_game(self, difficulty):

        self.difficulty = difficulty

        settings = self.DIFFICULTIES[difficulty]

        self.move_delay = settings["delay"]

        self.snake = [
            (14, 9),
            (13, 9),
            (12, 9)
        ]

        self.direction = (1, 0)
        self.next_direction = (1, 0)

        self.score = 0

        self.dead = False

        self.stats_recorded = False

        self.timer = 0

        self.food = self.spawn_food()

        self.state = "game"

    # ============================================================
    # GERAR COMIDA
    # ============================================================

    def spawn_food(self):

        while True:

            position = (
                random.randrange(self.COLS),
                random.randrange(self.ROWS)
            )

            if position not in self.snake:

                return position

    # ============================================================
    # EVENTOS
    # ============================================================

    def handle_event(self, event):

        # --------------------------------------------------------
        # TECLADO
        # --------------------------------------------------------

        if event.type == pygame.KEYDOWN:

            # ESC
            if event.key == pygame.K_ESCAPE:

                if self.state == "difficulty":

                    return "menu"

                self.state = "difficulty"

                return None

            # Tela de dificuldade
            if self.state == "difficulty":

                return None

            # Reiniciar
            if event.key == pygame.K_r:

                self.start_game(
                    self.difficulty
                )

                return None

            # ----------------------------------------------------
            # MOVIMENTO
            # ----------------------------------------------------

            keys = {

                pygame.K_UP: (0, -1),
                pygame.K_w: (0, -1),

                pygame.K_DOWN: (0, 1),
                pygame.K_s: (0, 1),

                pygame.K_LEFT: (-1, 0),
                pygame.K_a: (-1, 0),

                pygame.K_RIGHT: (1, 0),
                pygame.K_d: (1, 0)
            }

            if event.key in keys and not self.dead:

                new_direction = keys[event.key]

                # Não permite virar diretamente para trás
                if new_direction != (
                    -self.direction[0],
                    -self.direction[1]
                ):

                    self.next_direction = new_direction

        # --------------------------------------------------------
        # MOUSE
        # --------------------------------------------------------

        if event.type == pygame.MOUSEMOTION:

            if self.state == "difficulty":

                self.hover_difficulty = None

                for difficulty, rect in self.difficulty_buttons.items():

                    if rect.collidepoint(event.pos):

                        self.hover_difficulty = difficulty

        # --------------------------------------------------------
        # CLIQUE
        # --------------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button != 1:

                return None

            if self.state == "difficulty":

                for difficulty, rect in self.difficulty_buttons.items():

                    if rect.collidepoint(event.pos):

                        self.start_game(
                            difficulty
                        )

                        return None

            else:

                if self.back.collidepoint(
                    event.pos
                ):

                    self.state = "difficulty"

                    return None

        return None

    # ============================================================
    # UPDATE
    # ============================================================

    def update(self):

        if self.state != "game":

            return

        if self.dead:

            return

        self.timer += 1

        if self.timer < self.move_delay:

            return

        self.timer = 0

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]

        direction_x, direction_y = self.direction

        new_head = (
            head_x + direction_x,
            head_y + direction_y
        )

        # --------------------------------------------------------
        # COLISÃO COM PAREDE
        # --------------------------------------------------------

        if (
            new_head[0] < 0
            or new_head[0] >= self.COLS
            or new_head[1] < 0
            or new_head[1] >= self.ROWS
        ):

            self.game_over()

            return

        # --------------------------------------------------------
        # COLISÃO COM O PRÓPRIO CORPO
        # --------------------------------------------------------

        if new_head in self.snake:

            self.game_over()

            return

        # --------------------------------------------------------
        # ADICIONA NOVA CABEÇA
        # --------------------------------------------------------

        self.snake.insert(
            0,
            new_head
        )

        # --------------------------------------------------------
        # COMEU
        # --------------------------------------------------------

        if new_head == self.food:

            self.score += 10

            if self.score > self.best_score:

                self.best_score = self.score

            self.food = self.spawn_food()

        else:

            self.snake.pop()

    # ============================================================
    # GAME OVER
    # ============================================================

    def game_over(self):

        if self.dead:

            return

        self.dead = True

        if self.score > self.best_score:

            self.best_score = self.score

        # --------------------------------------------------------
        # REGISTRA ESTATÍSTICAS
        # --------------------------------------------------------

        if (
            self.stats
            and not self.stats_recorded
        ):

            self.stats.record_snake_game(
                self.score
            )

            self.stats_recorded = True

    # ============================================================
    # DESENHAR GRADE
    # ============================================================

    def draw_grid(self, ox, oy):

        grid_color = (
            22,
            27,
            42
        )

        for x in range(
            self.COLS + 1
        ):

            pygame.draw.line(
                self.screen,
                grid_color,
                (
                    ox + x * self.CELL,
                    oy
                ),
                (
                    ox + x * self.CELL,
                    oy + self.ROWS * self.CELL
                ),
                1
            )

        for y in range(
            self.ROWS + 1
        ):

            pygame.draw.line(
                self.screen,
                grid_color,
                (
                    ox,
                    oy + y * self.CELL
                ),
                (
                    ox + self.COLS * self.CELL,
                    oy + y * self.CELL
                ),
                1
            )

    # ============================================================
    # DESENHAR COMIDA
    # ============================================================

    def draw_food(self, ox, oy):

        fx, fy = self.food

        center = (
            ox + fx * self.CELL + self.CELL // 2,
            oy + fy * self.CELL + self.CELL // 2
        )

        # Corpo da comida
        pygame.draw.circle(
            self.screen,
            DANGER,
            center,
            9
        )

        # Brilho
        pygame.draw.circle(
            self.screen,
            TEXT,
            (
                center[0] - 3,
                center[1] - 3
            ),
            2
        )

        # Pequeno caule
        pygame.draw.line(
            self.screen,
            ACCENT,
            (
                center[0] + 2,
                center[1] - 8
            ),
            (
                center[0] + 6,
                center[1] - 13
            ),
            3
        )

    # ============================================================
    # DESENHAR COBRA
    # ============================================================

    def draw_snake(self, ox, oy):

        for index, (x, y) in enumerate(
            self.snake
        ):

            rect = pygame.Rect(
                ox + x * self.CELL + 2,
                oy + y * self.CELL + 2,
                self.CELL - 4,
                self.CELL - 4
            )

            if index == 0:

                color = ACCENT

            else:

                color = (
                    75,
                    190,
                    155
                )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=6
            )

        # --------------------------------------------------------
        # OLHOS DA CABEÇA
        # --------------------------------------------------------

        if self.snake:

            hx, hy = self.snake[0]

            cx = (
                ox
                + hx * self.CELL
                + self.CELL // 2
            )

            cy = (
                oy
                + hy * self.CELL
                + self.CELL // 2
            )

            eye_color = BG

            # Posição dos olhos dependendo da direção
            if self.direction == (1, 0):

                eyes = [
                    (cx + 5, cy - 5),
                    (cx + 5, cy + 5)
                ]

            elif self.direction == (-1, 0):

                eyes = [
                    (cx - 5, cy - 5),
                    (cx - 5, cy + 5)
                ]

            elif self.direction == (0, -1):

                eyes = [
                    (cx - 5, cy - 5),
                    (cx + 5, cy - 5)
                ]

            else:

                eyes = [
                    (cx - 5, cy + 5),
                    (cx + 5, cy + 5)
                ]

            for eye in eyes:

                pygame.draw.circle(
                    self.screen,
                    eye_color,
                    eye,
                    2
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
            "SNAKE",
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

            hovered = (
                self.hover_difficulty
                == difficulty
            )

            color = (
                ACCENT
                if hovered
                else PANEL_2
            )

            border = (
                ACCENT
                if hovered
                else (
                    48,
                    55,
                    78
                )
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

            settings = self.DIFFICULTIES[
                difficulty
            ]

            main_color = (
                BG
                if hovered
                else TEXT
            )

            secondary_color = (
                BG
                if hovered
                else MUTED
            )

            name = font(
                27,
                True
            ).render(
                settings["name"],
                True,
                main_color
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

            speed = font(
                20,
                True
            ).render(
                "VELOCIDADE",
                True,
                main_color
            )

            self.screen.blit(
                speed,
                speed.get_rect(
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
                secondary_color
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
            "SNAKE",
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
        # SCORE
        # --------------------------------------------------------

        score = font(
            21,
            True
        ).render(
            f"SCORE  {self.score}",
            True,
            ACCENT
        )

        self.screen.blit(
            score,
            (760, 45)
        )

        # --------------------------------------------------------
        # BEST
        # --------------------------------------------------------

        best = font(
            17
        ).render(
            f"BEST  {self.best_score}",
            True,
            MUTED
        )

        self.screen.blit(
            best,
            (900, 48)
        )

        # --------------------------------------------------------
        # ÁREA DO JOGO
        # --------------------------------------------------------

        ox = 200
        oy = 105

        board_rect = pygame.Rect(
            ox - 8,
            oy - 8,
            self.COLS * self.CELL + 16,
            self.ROWS * self.CELL + 16
        )

        pygame.draw.rect(
            self.screen,
            PANEL,
            board_rect,
            border_radius=12
        )

        self.draw_grid(
            ox,
            oy
        )

        self.draw_food(
            ox,
            oy
        )

        self.draw_snake(
            ox,
            oy
        )

        # --------------------------------------------------------
        # GAME OVER
        # --------------------------------------------------------

        if self.dead:

            overlay = pygame.Surface(
                (
                    self.COLS * self.CELL,
                    self.ROWS * self.CELL
                ),
                pygame.SRCALPHA
            )

            overlay.fill(
                (
                    8,
                    10,
                    18,
                    175
                )
            )

            self.screen.blit(
                overlay,
                (ox, oy)
            )

            game_over = font(
                38,
                True
            ).render(
                "GAME OVER",
                True,
                DANGER
            )

            self.screen.blit(
                game_over,
                game_over.get_rect(
                    center=(
                        ox
                        + self.COLS
                        * self.CELL
                        // 2,
                        oy + 180
                    )
                )
            )

            score_text = font(
                20,
                True
            ).render(
                f"Pontuação: {self.score}",
                True,
                TEXT
            )

            self.screen.blit(
                score_text,
                score_text.get_rect(
                    center=(
                        ox
                        + self.COLS
                        * self.CELL
                        // 2,
                        oy + 230
                    )
                )
            )

            restart = font(
                16
            ).render(
                "Pressione R para jogar novamente",
                True,
                MUTED
            )

            self.screen.blit(
                restart,
                restart.get_rect(
                    center=(
                        ox
                        + self.COLS
                        * self.CELL
                        // 2,
                        oy + 270
                    )
                )
            )

        # --------------------------------------------------------
        # BOTÃO VOLTAR
        # --------------------------------------------------------

        button(
            self.screen,
            self.back,
            "← VOLTAR"
        )

        # --------------------------------------------------------
        # CONTROLES
        # --------------------------------------------------------

        controls = font(
            14
        ).render(
            "WASD / SETAS para mover  •  R para reiniciar  •  ESC para voltar",
            True,
            MUTED
        )

        self.screen.blit(
            controls,
            controls.get_rect(
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