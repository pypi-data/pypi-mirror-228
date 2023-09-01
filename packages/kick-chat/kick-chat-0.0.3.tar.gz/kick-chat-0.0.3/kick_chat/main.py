#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from kick_chat.client import Client


def main(argv=None) -> int:
    if argv is None or len(argv) != 2:
        print(f"Usage: {argv[0]} <channel_name>")
        return 1
    client = Client(username=argv[1])
    client.listen()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
