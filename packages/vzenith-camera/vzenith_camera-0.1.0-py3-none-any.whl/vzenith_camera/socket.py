from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from enum import Enum
from socket import socket, AF_INET, SOCK_STREAM, MSG_DONTWAIT
from typing import Optional


class PacketType(Enum):
    DATA = 0
    HEARTBEAT = 1
    BINARY = 2


@dataclass
class PacketHeader:
    type: PacketType
    length: int
    sn: int = 0

    def to_bytes(self) -> bytes:
        return b'VZ%c%c%s' % (self.type.value, self.sn, self.length.to_bytes(4, 'big'))

    @staticmethod
    def parse(s: bytes) -> Optional[PacketHeader]:
        if len(s) == 0 or s[0:2] != b'VZ':
            return None

        return PacketHeader(type=PacketType(s[2]), length=int.from_bytes(s[4:8], 'big'), sn=s[3])


@dataclass
class Packet:
    header: PacketHeader
    data: Optional[bytes]


class TCPClient:
    DATA_ENCODING = 'gb2312'

    _socket: _socket
    _address: str
    _port: int

    @property
    def socket(self) -> socket:
        return self._socket

    @property
    def address(self) -> str:
        return self._address

    @property
    def port(self) -> int:
        return self._port

    def __init__(self):
        self._socket = socket(AF_INET, SOCK_STREAM)

    def connect(self, address: str, port: int):
        self._socket.connect((address, port))
        self._address = address
        self._port = port

        logging.debug('[%s:%d] connected', self._address, self._port)

    def send_packet(self, packet: Packet):
        s = packet.header.to_bytes()
        if packet.data is not None:
            s += packet.data

        logging.debug('[%s:%d] send: %s', self._address, self._port, s)

        self._socket.send(s)

    def send_request(self, obj: object):
        data = json.dumps(obj, ensure_ascii=False).encode(TCPClient.DATA_ENCODING)

        self.send_packet(Packet(header=PacketHeader(PacketType.DATA, len(data)), data=data))

    def recv_packet_header(self, blocking: bool = True) -> Optional[PacketHeader]:
        s = self.recv_bytes(8, blocking)

        if s is None:
            return None

        return PacketHeader.parse(s)

    def recv_response(self, blocking: bool = True) -> Optional[dict]:
        header = self.recv_packet_header(blocking)

        if header is None or header.type == PacketType.HEARTBEAT:
            return None

        s = self.recv_bytes(header.length, blocking)

        if s is None:
            return None

        return json.loads(s.decode(TCPClient.DATA_ENCODING))

    def recv_bytes(self, n: int, blocking: bool = True) -> Optional[bytes]:
        s = self._socket.recv(n, 0 if blocking else MSG_DONTWAIT)
        logging.debug('[%s:%d] recv: %s', self._address, self._port, s)

        return s

    def heartbeat(self):
        self.send_packet(Packet(header=PacketHeader(PacketType.HEARTBEAT, 0), data=None))
