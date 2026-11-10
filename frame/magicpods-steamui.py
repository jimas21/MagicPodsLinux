#!/usr/bin/env python3
"""Puts the MagicPods menu into Steam's VR UI (ARM64 SteamOS, e.g. Steam Frame).

Every few seconds this lists Steam's UI pages through Steam's local Chrome DevTools
endpoint (127.0.0.1:8080, present because Steam runs with -cef-enable-debugging; the
same mechanism Decky Loader uses) and makes sure the VR top bar and the quick-access
popup run the current magicpods-menu.js. The script itself then lives in those pages:
it talks to MagicPodsCore directly and keeps its elements in place.

Only the fixed contents of magicpods-menu.js are ever sent to Steam. Nothing listens
on any port. Unofficial: if a Steam update changes these pages, the menu just does not
appear and this keeps retrying quietly.

Python 3 standard library only. License: GPL-3.0 (part of MagicPods for Linux).
"""

import base64
import hashlib
import json
import os
import select
import signal
import socket
import struct
import sys
import time
import urllib.parse
import urllib.request

CDP_LIST = "http://127.0.0.1:8080/json/list"
PAGE_MARKS = ("vrOverlayKey=valve.steam.gamepadui.bar",)  # matches the bar and barpopup.* pages
MENU_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "magicpods-menu.js")
POLL_SECONDS = 3


def log(*parts):
    print(time.strftime("%H:%M:%S"), *parts, flush=True)


class CdpPage:
    """One short-lived DevTools connection to a page (minimal RFC 6455 client)."""

    def __init__(self, ws_url, timeout=4.0):
        url = urllib.parse.urlparse(ws_url)
        if url.hostname not in ("127.0.0.1", "localhost"):
            raise ValueError("refusing a non-local DevTools URL")
        self.sock = socket.create_connection((url.hostname, url.port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall(
            (f"GET {url.path} HTTP/1.1\r\nHost: {url.hostname}:{url.port}\r\nUpgrade: websocket\r\n"
             f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self.sock.recv(1)
            if not chunk or len(head) > 16384:
                raise ConnectionError("DevTools handshake failed")
            head += chunk
        if b" 101 " not in head.split(b"\r\n", 1)[0] + b" ":
            raise ConnectionError("DevTools refused the connection")
        expected = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest())
        if expected not in head:
            raise ConnectionError("DevTools handshake: bad accept key")
        self.buffer = b""
        self.next_id = 1

    def _send(self, opcode, payload):
        mask = os.urandom(4)
        n = len(payload)
        header = bytes([0x80 | opcode])
        if n < 126:
            header += bytes([0x80 | n])
        elif n < 65536:
            header += bytes([0x80 | 126]) + struct.pack("!H", n)
        else:
            header += bytes([0x80 | 127]) + struct.pack("!Q", n)
        self.sock.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def _read_message(self, deadline):
        fragments = []
        while True:
            while True:
                frame = self._parse()
                if frame:
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("DevTools reply timed out")
                ready, _, _ = select.select([self.sock], [], [], remaining)
                if ready:
                    chunk = self.sock.recv(65536)
                    if not chunk:
                        raise ConnectionError("DevTools connection closed")
                    self.buffer += chunk
            opcode, fin, payload = frame
            if opcode == 0x9:
                self._send(0xA, payload)
            elif opcode == 0x8:
                raise ConnectionError("DevTools connection closed")
            elif opcode in (0x0, 0x1):
                fragments.append(payload)
                if fin:
                    return b"".join(fragments).decode("utf-8", "replace")

    def _parse(self):
        if len(self.buffer) < 2:
            return None
        b0, b1 = self.buffer[0], self.buffer[1]
        n, offset = b1 & 0x7F, 2
        if n == 126:
            if len(self.buffer) < 4:
                return None
            n, offset = struct.unpack("!H", self.buffer[2:4])[0], 4
        elif n == 127:
            if len(self.buffer) < 10:
                return None
            n, offset = struct.unpack("!Q", self.buffer[2:10])[0], 10
        if b1 & 0x80:
            offset += 4
        if len(self.buffer) < offset + n:
            return None
        payload = self.buffer[offset:offset + n]
        self.buffer = self.buffer[offset + n:]
        return b0 & 0x0F, b0 & 0x80, payload

    def evaluate(self, expression, timeout=5.0):
        msg_id = self.next_id
        self.next_id += 1
        self._send(0x1, json.dumps({"id": msg_id, "method": "Runtime.evaluate",
                                    "params": {"expression": expression, "returnByValue": True}}).encode())
        deadline = time.monotonic() + timeout
        while True:
            msg = json.loads(self._read_message(deadline))
            if msg.get("id") == msg_id:
                result = msg.get("result", {})
                if "exceptionDetails" in result:
                    raise RuntimeError(result["exceptionDetails"].get("text", "script error"))
                return result.get("result", {}).get("value")

    def close(self):
        try:
            self._send(0x8, b"")
        except OSError:
            pass
        self.sock.close()


def load_menu():
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        source = f.read()
    version = hashlib.sha256(source.encode()).hexdigest()[:12]
    return version, source.replace("__VERSION__", version)


def sync_page(target, version, script):
    page = CdpPage(target["webSocketDebuggerUrl"])
    try:
        current = page.evaluate("window.__magicpodsMenu ? window.__magicpodsMenu.version : null")
        if current == version:
            return None
        return page.evaluate(script)
    finally:
        page.close()


def main():
    stopping = {"flag": False}

    def stop(signum, frame):
        stopping["flag"] = True

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    version, script = load_menu()
    log("menu version", version)
    last_status = None
    while not stopping["flag"]:
        try:
            with urllib.request.urlopen(CDP_LIST, timeout=3) as response:
                targets = json.load(response)
            pages = [t for t in targets if any(m in t.get("url", "") for m in PAGE_MARKS) and t.get("webSocketDebuggerUrl")]
            status = f"{len(pages)} Steam VR page(s)"
            for target in pages:
                try:
                    result = sync_page(target, version, script)
                    if result:
                        log(target.get("title", "?")[:60], "->", result)
                except (OSError, ValueError, RuntimeError, TimeoutError, ConnectionError) as error:
                    status = f"page error: {error}"
        except (OSError, ValueError) as error:
            status = f"waiting for Steam's DevTools endpoint ({error})"
        if status != last_status:
            log(status)
            last_status = status
        for _ in range(POLL_SECONDS * 10):
            if stopping["flag"]:
                break
            time.sleep(0.1)
    # Leave Steam's pages as they were.
    try:
        with urllib.request.urlopen(CDP_LIST, timeout=3) as response:
            for target in json.load(response):
                if any(m in target.get("url", "") for m in PAGE_MARKS) and target.get("webSocketDebuggerUrl"):
                    try:
                        page = CdpPage(target["webSocketDebuggerUrl"])
                        page.evaluate("window.__magicpodsMenu && window.__magicpodsMenu.teardown()")
                        page.close()
                    except Exception:
                        pass
    except Exception:
        pass
    log("stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
