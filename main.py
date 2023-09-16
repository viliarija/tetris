from objects import *
import threading

canvas = Canvas()

canvas.load()
threading.Thread(target=canvas.update).start()

while True:
    canvas.tick()
