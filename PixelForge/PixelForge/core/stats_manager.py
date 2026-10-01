import json
import os


class StatsManager:

    def __init__(self):

        self.data_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            "data"
        )

        self.file_path = os.path.join(
            self.data_dir,
            "stats.json"
        )

        os.makedirs(
            self.data_dir,
            exist_ok=True
        )

        self.stats = self.default_stats()

        self.load()

    def default_stats(self):

        return {
            "general": {
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            },

            "rock_paper_scissors": {
                "played": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            },

            "tic_tac_toe": {
                "played": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            },

            "hangman": {
                "played": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0
            },

            "snake": {
                "played": 0,
                "best_score": 0
            }
        }

    def load(self):

        if not os.path.exists(
            self.file_path
        ):

            self.save()

            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                saved_stats = json.load(
                    file
                )

            self.merge_stats(
                saved_stats
            )

        except (
            json.JSONDecodeError,
            OSError
        ):

            print(
                "Aviso: não foi possível carregar as estatísticas."
            )

            self.stats = self.default_stats()

            self.save()

    def merge_stats(
        self,
        saved_stats
    ):

        default = self.default_stats()

        for category, values in default.items():

            if category not in saved_stats:

                saved_stats[category] = values

                continue

            for key, default_value in values.items():

                if key not in saved_stats[category]:

                    saved_stats[category][key] = default_value

        self.stats = saved_stats

    def save(self):

        try:

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.stats,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError:

            print(
                "Erro: não foi possível salvar as estatísticas."
            )

    def record_win(
        self,
        game
    ):

        if game not in self.stats:

            return

        self.stats["general"]["games_played"] += 1
        self.stats["general"]["wins"] += 1

        self.stats[game]["played"] += 1
        self.stats[game]["wins"] += 1

        self.save()

    def record_loss(
        self,
        game
    ):

        if game not in self.stats:

            return

        self.stats["general"]["games_played"] += 1
        self.stats["general"]["losses"] += 1

        self.stats[game]["played"] += 1
        self.stats[game]["losses"] += 1

        self.save()

    def record_draw(
        self,
        game
    ):

        if game not in self.stats:

            return

        self.stats["general"]["games_played"] += 1
        self.stats["general"]["draws"] += 1

        self.stats[game]["played"] += 1
        self.stats[game]["draws"] += 1

        self.save()

    def record_snake_game(
        self,
        score
    ):

        self.stats["general"]["games_played"] += 1

        self.stats["snake"]["played"] += 1

        current_best = (
            self.stats["snake"]["best_score"]
        )

        if score > current_best:

            self.stats["snake"]["best_score"] = score

        self.save()

    def record_snake_score(
        self,
        score
    ):

        current_best = (
            self.stats["snake"]["best_score"]
        )

        if score > current_best:

            self.stats["snake"]["best_score"] = score

            self.save()

            return True

        return False

    def get_stats(self):

        return self.stats

    def reset(self):

        self.stats = self.default_stats()

        self.save()