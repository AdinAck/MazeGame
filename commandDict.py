from typing import Dict

commandDict: Dict[str, int] = {
    'new-player': 0x10,
    'update-coords': 0x20,
    'request-coords': 0x21,
    'remove-player': 0x30,
    'send-grid': 0x40,
    'no-op': 0xFFFF
}
