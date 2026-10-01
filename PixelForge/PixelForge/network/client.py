import socket
import threading
import json


HOST = "127.0.0.1"
PORT = 5000


def send_message(sock, data):

    message = json.dumps(
        data,
        ensure_ascii=False
    ) + "\n"

    sock.sendall(
        message.encode("utf-8")
    )


def receive_messages(sock):

    buffer = ""

    try:

        while True:

            data = sock.recv(4096)

            if not data:

                print(
                    "\nConexão encerrada pelo servidor."
                )

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

                    continue

                handle_message(message)

    except ConnectionResetError:

        print(
            "\nConexão perdida."
        )

    except OSError:

        print(
            "\nConexão encerrada."
        )


def handle_message(message):

    message_type = message.get(
        "type"
    )

    if message_type == "welcome":

        player = message.get(
            "player"
        )

        print(
            f"\nVocê é o Jogador {player}."
        )

    elif message_type == "player_joined":

        player = message.get(
            "player"
        )

        print(
            f"\nJogador {player} entrou na partida."
        )

    elif message_type == "player_left":

        player = message.get(
            "player"
        )

        print(
            f"\nJogador {player} saiu da partida."
        )

    elif message_type == "server_full":

        print(
            "\nO servidor já está cheio."
        )

    elif message_type == "message":

        player = message.get(
            "player"
        )

        text = message.get(
            "message",
            ""
        )

        print(
            f"\nJogador {player}: {text}"
        )

    else:

        print(
            f"\nMensagem recebida: {message}"
        )


def start_client():

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:

        print(
            f"Conectando ao servidor {HOST}:{PORT}..."
        )

        sock.connect(
            (HOST, PORT)
        )

        print(
            "Conectado ao PixelForge!"
        )

        receiver = threading.Thread(
            target=receive_messages,
            args=(sock,),
            daemon=True
        )

        receiver.start()

        print(
            "\nDigite mensagens para testar a conexão."
        )

        print(
            "Digite 'sair' para desconectar.\n"
        )

        while True:

            text = input("> ")

            if text.lower() == "sair":

                break

            if not text.strip():
                continue

            send_message(
                sock,
                {
                    "type": "message",
                    "message": text
                }
            )

    except ConnectionRefusedError:

        print(
            "\nNão foi possível conectar ao servidor."
        )

        print(
            "Verifique se o server.py está rodando."
        )

    except OSError as error:

        print(
            f"\nErro de conexão: {error}"
        )

    finally:

        try:
            sock.close()
        except OSError:
            pass

        print(
            "\nCliente encerrado."
        )


if __name__ == "__main__":
    start_client()