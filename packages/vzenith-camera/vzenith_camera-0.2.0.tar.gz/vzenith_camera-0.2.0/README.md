# vzenith-camera

![license](https://img.shields.io/github/license/he-yaowen/vzenith-camera)
![status](https://img.shields.io/pypi/status/vzenith-camera)
![version](https://img.shields.io/pypi/v/vzenith-camera)
![build](https://img.shields.io/github/actions/workflow/status/he-yaowen/vzenith-camera/ubuntu-jammy.yml)
![codecov](https://img.shields.io/codecov/c/github/he-yaowen/vzenith-camera)
![python](https://img.shields.io/pypi/pyversions/vzenith-camera)
![downloads](https://img.shields.io/pypi/dm/vzenith-camera)

A Python library for [VisionZenith][1] Smart Camera SDK in TCP protocol.

## Installation

`vzenith-camera` is published on [PyPI][2], so you can install this module with:

```
pip install vzenith-camera
```

## Quickstart

Following is an example to monitor recognized license from a camera.

```python
from vzenith_camera import SmartCamera
from vzenith_camera.types import Event, PlateResult

camera = SmartCamera('camera-name')
camera.connect('CAMERA_ADDRESS', 8131)

# Get serial number.
print(f'Serial Number: {camera.cmd_getsn()}')


# The callback function of reorganization result.
def ivsresult_callback(event: Event, result: PlateResult):
    print(f'Got license "{result.license}" on camera "{event.target.name}".')


# Register the 'ivsresult' event.
camera.on('ivsresult', ivsresult_callback)

# Send command 'ivsresult' to camera.
camera.cmd_ivsresult(enable=True, result_format='json', image_type=False)
```

## License

Copyright (C) 2023 HE Yaowen <he.yaowen@hotmail.com>

The BSD-3-Clause License, see [LICENSE](./LICENSE).

[1]: https://www.vzenith.com

[2]: https://pypi.org/
