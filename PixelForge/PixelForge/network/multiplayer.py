import socket
import threading
import json
import queue


class MultiplayerClient:

    def __init__(
        self,
        host="127.0.0.1",
        port=5000
    ):

        self.host = host
        self.port = port

        self.sock = None

        self.player_id = None

        self.connected = False

        self.messages = queue.Queue()

        self.send_lock = threading.Lock()

        self.receiver_thread = None

    def connect(self):

        try:

            self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.sock.connect(
                (self.host, self.port)
            )

            self.connected = True

            self.receiver_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            self.receiver_thread.start()

            return True

        except OSError:

            self.connected = False

            if self.sock:

                try:
                    self.sock.close()
                except OSError:
                    pass

            self.sock = None

            return False

    def receive_messages(self):

        buffer = ""

        try:

            while self.connected:

                data = self.sock.recv(4096)

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

                        if message.get("type") == "welcome":

                            self.player_id = message.get(
                                "player"
                            )

                        self.messages.put(
                            message
                        )

                    except json.JSONDecodeError:

                        continue

        except (
            ConnectionResetError,
            OSError
        ):
            pass

        finally:

            self.connected = False

    def send(self, data):

        if not self.connected:
            return False

        try:

            message = json.dumps(
                data,
                ensure_ascii=False
            ) + "\n"

            with self.send_lock:

                self.sock.sendall(
                    message.encode("utf-8")
                )

            return True

        except OSError:

            self.connected = False

            return False

    def get_messages(self):

        messages = []

        while True:

            try:

                message = self.messages.get_nowait()

                messages.append(
                    message
                )

            except queue.Empty:

                break

        return messages

    def close(self):

        self.connected = False

        if self.sock:

            try:
                self.sock.shutdown(
                    socket.SHUT_RDWR
                )
            except OSError:
                pass

            try:
                self.sock.close()
            except OSError:
                pass

            self.sock = None