import socket
import threading
import json


HOST = "0.0.0.0"
PORT = 5000

MAX_PLAYERS = 2


clients = {}

clients_lock = threading.Lock()


# =========================================================
# CONTROLE DO PEDRA, PAPEL E TESOURA
# =========================================================

rps_choices = {}

rps_round = 1

rps_lock = threading.Lock()


# =========================================================
# CONTROLE DO JOGO DA VELHA
# =========================================================

ttt_board = [""] * 9

ttt_current_player = "X"

ttt_game_started = False

ttt_lock = threading.Lock()


# =========================================================
# ENVIO DE MENSAGENS
# =========================================================

def send_message(conn, data):

    try:

        message = json.dumps(
            data,
            ensure_ascii=False
        ) + "\n"

        conn.sendall(
            message.encode("utf-8")
        )

        return True

    except OSError:

        return False


def broadcast(data):

    with clients_lock:

        connections = list(
            clients.keys()
        )

    for conn in connections:

        send_message(
            conn,
            data
        )


def send_to_opponent(
    sender_conn,
    data
):

    with clients_lock:

        connections = list(
            clients.keys()
        )

    for conn in connections:

        if conn != sender_conn:

            send_message(
                conn,
                data
            )


def get_available_player():

    used_players = set(
        clients.values()
    )

    for player in range(
        1,
        MAX_PLAYERS + 1
    ):

        if player not in used_players:

            return player

    return None


# =========================================================
# PEDRA, PAPEL E TESOURA
# =========================================================

def get_rps_result(
    player1_choice,
    player2_choice
):

    if player1_choice == player2_choice:

        return "draw"

    if (
        player1_choice == "Pedra"
        and player2_choice == "Tesoura"
    ):

        return "player1"

    if (
        player1_choice == "Papel"
        and player2_choice == "Pedra"
    ):

        return "player1"

    if (
        player1_choice == "Tesoura"
        and player2_choice == "Papel"
    ):

        return "player1"

    return "player2"


def process_rps_choice(
    conn,
    player,
    choice
):

    global rps_round

    with rps_lock:

        # ==============================================
        # EVITA JOGADA DUPLICADA
        # ==============================================

        if player in rps_choices:

            print(
                f"Jogador {player} "
                f"já escolheu nesta rodada."
            )

            return

        rps_choices[player] = choice

        print(
            f"Jogador {player} escolheu "
            f"{choice} "
            f"(rodada {rps_round})"
        )

        # ==============================================
        # AGUARDA O OUTRO JOGADOR
        # ==============================================

        if len(rps_choices) < 2:

            send_message(
                conn,
                {
                    "type": "rps_waiting"
                }
            )

            return

        # ==============================================
        # OS DOIS ESCOLHERAM
        # ==============================================

        player1_choice = rps_choices.get(
            1
        )

        player2_choice = rps_choices.get(
            2
        )

        if (
            player1_choice is None
            or player2_choice is None
        ):

            return

        result = get_rps_result(
            player1_choice,
            player2_choice
        )

        print(
            f"Resultado da rodada {rps_round}: "
            f"Jogador 1 = {player1_choice} | "
            f"Jogador 2 = {player2_choice}"
        )

        broadcast(
            {
                "type": "rps_result",

                "round": rps_round,

                "player1_choice": player1_choice,

                "player2_choice": player2_choice,

                "result": result
            }
        )

        rps_choices.clear()

        rps_round += 1


# =========================================================
# JOGO DA VELHA
# =========================================================

def ttt_check_winner(board):

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


def reset_ttt():

    global ttt_board
    global ttt_current_player
    global ttt_game_started

    ttt_board = [""] * 9

    ttt_current_player = "X"

    ttt_game_started = True


def send_ttt_state():

    broadcast(
        {
            "type": "ttt_state",

            "board": ttt_board.copy(),

            "current_player": ttt_current_player
        }
    )


def process_ttt_move(
    conn,
    player,
    position
):

    global ttt_current_player

    with ttt_lock:

        # ==============================================
        # VERIFICA SE EXISTEM DOIS JOGADORES
        # ==============================================

        with clients_lock:

            player_count = len(
                clients
            )

        if player_count < 2:

            send_message(
                conn,
                {
                    "type": "ttt_waiting",
                    "message": "Aguardando outro jogador..."
                }
            )

            return

        # ==============================================
        # VALIDA POSIÇÃO
        # ==============================================

        if not isinstance(
            position,
            int
        ):

            return

        if position < 0 or position > 8:

            return

        # ==============================================
        # DEFINE O SÍMBOLO DO JOGADOR
        # ==============================================

        if player == 1:

            symbol = "X"

        else:

            symbol = "O"

        # ==============================================
        # CONFERE A VEZ
        # ==============================================

        if symbol != ttt_current_player:

            send_message(
                conn,
                {
                    "type": "ttt_invalid",
                    "message": "Não é sua vez."
                }
            )

            return

        # ==============================================
        # CONFERE SE A CASA ESTÁ LIVRE
        # ==============================================

        if ttt_board[position] != "":

            send_message(
                conn,
                {
                    "type": "ttt_invalid",
                    "message": "Essa casa já está ocupada."
                }
            )

            return

        # ==============================================
        # REALIZA JOGADA
        # ==============================================

        ttt_board[position] = symbol

        print(
            f"Jogador {player} "
            f"jogou na posição {position}"
        )

        # ==============================================
        # VERIFICA RESULTADO
        # ==============================================

        winner = ttt_check_winner(
            ttt_board
        )

        if winner:

            print(
                f"Resultado do Jogo da Velha: "
                f"{winner}"
            )

            broadcast(
                {
                    "type": "ttt_result",

                    "winner": winner,

                    "board": ttt_board.copy()
                }
            )

            return

        # ==============================================
        # TROCA A VEZ
        # ==============================================

        if ttt_current_player == "X":

            ttt_current_player = "O"

        else:

            ttt_current_player = "X"

        # ==============================================
        # ENVIA NOVO ESTADO
        # ==============================================

        send_ttt_state()


def process_ttt_reset():

    with ttt_lock:

        reset_ttt()

        print(
            "Jogo da Velha reiniciado."
        )

        send_ttt_state()


# =========================================================
# REMOVER JOGADOR
# =========================================================

def remove_client(conn):

    global rps_round

    with clients_lock:

        player = clients.pop(
            conn,
            None
        )

    try:

        conn.close()

    except OSError:

        pass

    if player is not None:

        print(
            f"Jogador {player} desconectado."
        )

        # ==============================================
        # RESET DO RPS
        # ==============================================

        with rps_lock:

            rps_choices.clear()

            rps_round = 1

        # ==============================================
        # RESET DO JOGO DA VELHA
        # ==============================================

        global ttt_board
        global ttt_current_player
        global ttt_game_started

        with ttt_lock:

            ttt_board = [""] * 9

            ttt_current_player = "X"

            ttt_game_started = False

        # ==============================================
        # AVISA O OUTRO JOGADOR
        # ==============================================

        broadcast(
            {
                "type": "player_left",
                "player": player
            }
        )


# =========================================================
# CLIENTE
# =========================================================

def handle_client(
    conn,
    address,
    player
):

    print(
        f"Jogador {player} conectado: "
        f"{address}"
    )

    send_message(
        conn,
        {
            "type": "welcome",
            "player": player
        }
    )

    broadcast(
        {
            "type": "player_joined",
            "player": player
        }
    )

    # ==============================================
    # SE DOIS JOGADORES ESTÃO CONECTADOS
    # PREPARA O JOGO DA VELHA
    # ==============================================

    with clients_lock:

        player_count = len(
            clients
        )

    if player_count == 2:

        with ttt_lock:

            reset_ttt()

            print(
                "Dois jogadores conectados."
            )

            print(
                "Jogo da Velha disponível."
            )

            send_ttt_state()

    buffer = ""

    try:

        while True:

            data = conn.recv(
                4096
            )

            if not data:

                break

            buffer += data.decode(
                "utf-8"
            )

            while "\n" in buffer:

                raw_message, buffer = buffer.split(
                    "\n",
                    1
                )

                if not raw_message.strip():

                    continue

                try:

                    message = json.loads(
                        raw_message
                    )

                except json.JSONDecodeError:

                    print(
                        "Mensagem inválida recebida."
                    )

                    continue

                message_type = message.get(
                    "type"
                )

                # ==========================================
                # TESTE DE CONEXÃO
                # ==========================================

                if message_type == "message":

                    text = message.get(
                        "message",
                        ""
                    )

                    print(
                        f"Jogador {player}: "
                        f"{text}"
                    )

                    send_to_opponent(
                        conn,
                        {
                            "type": "message",
                            "player": player,
                            "message": text
                        }
                    )

                # ==========================================
                # PEDRA, PAPEL E TESOURA
                # ==========================================

                elif message_type == "rps_choice":

                    choice = message.get(
                        "choice"
                    )

                    if choice not in (
                        "Pedra",
                        "Papel",
                        "Tesoura"
                    ):

                        print(
                            f"Jogada inválida "
                            f"do Jogador {player}."
                        )

                        continue

                    process_rps_choice(
                        conn,
                        player,
                        choice
                    )

                # ==========================================
                # JOGO DA VELHA - JOGADA
                # ==========================================

                elif message_type == "ttt_move":

                    position = message.get(
                        "position"
                    )

                    process_ttt_move(
                        conn,
                        player,
                        position
                    )

                # ==========================================
                # JOGO DA VELHA - REINICIAR
                # ==========================================

                elif message_type == "ttt_reset":

                    process_ttt_reset()

                # ==========================================
                # OUTRAS MENSAGENS
                # ==========================================

                else:

                    message["player"] = player

                    send_to_opponent(
                        conn,
                        message
                    )

    except ConnectionResetError:

        pass

    except OSError:

        pass

    finally:

        remove_client(
            conn
        )


# =========================================================
# SERVIDOR
# =========================================================

def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (
            HOST,
            PORT
        )
    )

    server.listen(
        MAX_PLAYERS
    )

    print("=" * 50)

    print(
        "PIXELFORGE MULTIPLAYER SERVER"
    )

    print("=" * 50)

    print(
        f"Servidor iniciado em "
        f"{HOST}:{PORT}"
    )

    print(
        f"Aguardando até "
        f"{MAX_PLAYERS} jogadores..."
    )

    print("=" * 50)

    try:

        while True:

            conn, address = server.accept()

            with clients_lock:

                if len(clients) >= MAX_PLAYERS:

                    send_message(
                        conn,
                        {
                            "type": "server_full"
                        }
                    )

                    conn.close()

                    print(
                        "Conexão recusada: "
                        "servidor cheio."
                    )

                    continue

                player = get_available_player()

                clients[conn] = player

            thread = threading.Thread(
                target=handle_client,
                args=(
                    conn,
                    address,
                    player
                ),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:

        print(
            "\nServidor encerrado."
        )

    finally:

        with clients_lock:

            connections = list(
                clients.keys()
            )

            clients.clear()

        for conn in connections:

            try:

                conn.close()

            except OSError:

                pass

        server.close()


if __name__ == "__main__":

    start_server()