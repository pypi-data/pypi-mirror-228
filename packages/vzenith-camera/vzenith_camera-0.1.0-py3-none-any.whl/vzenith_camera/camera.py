import json
import time
from threading import Thread
from typing import Optional

from .emitter import Emitter
from .socket import TCPClient
from .types import PlateResult

ENABLE_WATCHER_IVSRESULT = True


class SmartCamera(Emitter):
    client: TCPClient

    _name: str

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, name: str):
        super().__init__()

        self._name = name
        self.client = TCPClient()

    def connect(self, address: str, port: int = 8131):
        self.client.connect(address, port)

    def cmd_getsn(self) -> Optional[str]:
        self.client.send_request({'cmd': 'getsn'})

        data = self.client.recv_response()
        print(data)
        if 'state_code' not in data or data['state_code'] != 200 or 'value' not in data:
            return None

        return data['value']

    def cmd_ivsresult(self, enable: bool = False, result_format: str = 'json', image: bool = True,
                      image_type: int = 0) -> bool:

        cmd = {
            'cmd': 'ivsresult',
            'enable': enable,
            'format': result_format,
            'image': image,
            'image_type': image_type
        }

        self.client.send_request(cmd)
        data = self.client.recv_response()

        if enable:
            if data['state_code'] != 200:
                return False

            thread = Thread(target=_ivsresult_watcher, args=(self,))
            thread.start()

        return data['state_code'] == 200


def _ivsresult_watcher(camera: SmartCamera):
    count = 0

    while ENABLE_WATCHER_IVSRESULT:
        if count > 3:
            camera.client.heartbeat()
            count = 0

        count += 1

        try:
            header = camera.client.recv_packet_header(blocking=False)
            if header and header.length > 0:
                data = camera.client.recv_bytes(header.length)

                if data is not None:
                    res = json.loads(data[0:data.index(0x00) - 1].decode('gb2312'))['PlateResult']
                    result = PlateResult(
                        license=res['license'],
                    )

                    camera.emit('ivsresult', result)
        except BlockingIOError:
            ...

        time.sleep(1)
