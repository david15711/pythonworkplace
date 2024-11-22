import time
import asyncio
import websockets
from PIL import ImageGrab
from PIL import ImageStat
from PIL import ImageEnhance

# Analyzing the image and deleting black borders from movies (21:9 or 4:3)
def analyze_borders(debug=False):
    min_size = 3
    im = ImageGrab.grab()
    width, height = im.size
    box = []
    for x in range(0, height):
        # check top
        line = im.crop((0, x, width, x + 1))
        if debug:
            print("TOP", ImageStat.Stat(line).median)
        if ImageStat.Stat(line).median > [1, 1, 1]:
            box.append(x)
            break
        if x >= height / min_size:
            box.append(int(height / min_size))
            break
    for x in range(height, 0, -1):
        # check bottom
        line = im.crop((0, x, width, x + 1))
        if debug:
            print("BOTTOM", ImageStat.Stat(line).median)
        if ImageStat.Stat(line).median > [1, 1, 1]:
            box.append(height - x - 1)
            break
        if x <= height / min_size:
            box.append(int(height / min_size))
            break
    for x in range(0, width):
        # check left
        line = im.crop((x, 0, x + 1, height))
        if debug:
            print("LEFT", ImageStat.Stat(line).median)
        if ImageStat.Stat(line).median > [1, 1, 1]:
            box.append(x)
            break
        if x >= width / min_size:
            box.append(int(width / min_size))
            break
    for x in range(width, 0, -1):
        # check right
        line = im.crop((x, 0, x + 1, height))
        if debug:
            print("RIGHT", ImageStat.Stat(line).median)
        if ImageStat.Stat(line).median > [1, 1, 1]:
            box.append(width - x - 1)
            break
        if x <= width / min_size:
            box.append(int(width / min_size))
            break
    return box


def capture():
    return ImageGrab.grab()


@asyncio.coroutine
def start():
    time1 = time.time()
    websocket = yield from websockets.connect('ws://localhost:8887/')
    for x in range(0, 1000):
        im = capture()
        im = ImageEnhance.Color(im).enhance(1)
        im = ImageEnhance.Contrast(im).enhance(1)
        box = [0, 0, 0, 0]
        if x % 100 == 0:
            box = analyze_borders()
            print(box)
        w, h = im.size
        im = im.crop((box[2], box[0], w - box[3], h - box[1]))
        w, h = im.size
        im1 = im.crop((0, 0, int(w / 2), h))
        im2 = im.crop((int(w / 2), 0, w, h))
        stat1 = ImageStat.Stat(im1)
        stat2 = ImageStat.Stat(im2)
        # print(str(x) + " Median1: " + str(stat1.median))
        # print(str(x) + " Median2: " + str(stat2.median))
        yield from websocket.send(str("C1:(" + str(stat1.median[0]) +
                                      ", " + str(stat1.median[1]) +
                                      ", " + str(stat1.median[2]) + ")"))
        yield from websocket.send(str("C2:(" + str(stat2.median[0]) +
                                      ", " + str(stat2.median[1]) +
                                      ", " + str(stat2.median[2]) + ")"))
    yield from websocket.close()
    duration = time.time() - time1
    print(str(duration))
    print(str(1000 / duration))


asyncio.get_event_loop().run_until_complete(start())