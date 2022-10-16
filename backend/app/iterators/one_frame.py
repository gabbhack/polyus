from typing import Iterator


def one_frame(frame: bytes) -> Iterator[bytes]:
    yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
