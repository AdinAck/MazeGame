import os
import threading
from render import Renderer

from client import Client

# Configurable constants

c = Client()
r = Renderer(c)

r.main()
