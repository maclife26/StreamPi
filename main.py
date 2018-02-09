#!/usr/bin/env python3

import argparse
import os
import io

import tornado.ioloop
import tornado.web
import tornado.websocket

from PIL import Image

import pygame.camera
import pygame.image

parser = argparse.ArgumentParser(description='Comenzar el StreamPi.')

parser.add_argument('--port', default=8888, type=int, help='Puerto del servidor Web (default: 8888)')
parser.add_argument('--camera', default=0, type=int, help='Camara index, primera camera es 0 (default: 0)')
parser.add_argument('--width', default=460, type=int, help='Ancho (default: 640)')
parser.add_argument('--height', default=360, type=int, help='Alto (default: 480)')
parser.add_argument('--quality', default=70, type=int, help='JPEG Calidad 1 (peor) a 100 (mejor) (default: 70)')
parser.add_argument('--stopdelay', default=7, type=int, help='Delay en segundos (default: 7)')

args = parser.parse_args()

class Camera:

    def __init__(self, index, width, height, quality, stopdelay):
        print("Iniciando camara...")
        pygame.camera.init()
        camera_name = pygame.camera.list_cameras()[index]
        self._cam = pygame.camera.Camera(camera_name, (width, height))
        print("Camara iniciada")
        self.is_started = False
        self.stop_requested = False
        self.quality = quality
        self.stopdelay = stopdelay

    def request_start(self):
        if self.stop_requested:
            print("Camara continua en uso")
            self.stop_requested = False
        if not self.is_started:
            self._start()

    def request_stop(self):
        if self.is_started and not self.stop_requested:
            self.stop_requested = True
            print("Parando camara en: " + str(self.stopdelay) + " segundos...")
            tornado.ioloop.IOLoop.current().call_later(self.stopdelay, self._stop)

    def _start(self):
        print("Iniciando camara...")
        self._cam.start()
        print("Camara iniciada")
        self.is_started = True

    def _stop(self):
        if self.stop_requested:
            print("Deteniendo camara ahora...")
            self._cam.stop()
            print("Camara detenida")
            self.is_started = False
            self.stop_requested = False

    def get_jpeg_image_bytes(self):
        img = self._cam.get_image()
        imgstr = pygame.image.tostring(img, "RGB", False)
        pimg = Image.frombytes("RGB", img.get_size(), imgstr)
        with io.BytesIO() as bytesIO:
            pimg.save(bytesIO, "JPEG", quality=self.quality, optimize=True)
            return bytesIO.getvalue()


camera = Camera(args.camera, args.width, args.height, args.quality, args.stopdelay)


class ImageWebSocket(tornado.websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        # Permite el acceso desde cualquier origen
        return True

    def open(self):
        ImageWebSocket.clients.add(self)
        print("WebSocket abierto desde: " + self.request.remote_ip)
        camera.request_start()

    def on_message(self, message):
        jpeg_bytes = camera.get_jpeg_image_bytes()
        self.write_message(jpeg_bytes, binary=True)

    def on_close(self):
        ImageWebSocket.clients.remove(self)
        print("WebSocket cerrado desde: " + self.request.remote_ip)
        if len(ImageWebSocket.clients) == 0:
            camera.request_stop()


script_path = os.path.dirname(os.path.realpath(__file__))
static_path = script_path + '/static/'

app = tornado.web.Application([
        (r"/websocket", ImageWebSocket),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path, 'default_filename': 'index.html'}),
    ])
app.listen(args.port)

print("Comenzando servidor: http://localhost:" + str(args.port) + "/")

tornado.ioloop.IOLoop.current().start()
