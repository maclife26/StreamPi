
Prerequisitos
-------------

### Instalar dependencias

Se asume que se tiene Rasbian Jessie en Raspberry Pi. 

[Python 3](https://www.python.org/)

    sudo apt install python3
    
PIP para instalar paquetes Python:

    sudo apt-get install python3-pip

[Tornado Web server](http://www.tornadoweb.org/)

    sudo pip3 install tornado

[Python Imaging Library](https://pypi.python.org/pypi/PIL)

    sudo apt install python3-pil

[Pygame](https://www.pygame.org/) (usado para capturar imagenes de una web cam)

    sudo apt install python3-pygame
    
[git](https://git-scm.com/) (para clonar el repositorio)

    sudo apt install git

### Conectar WebCam

La WebCam debe ser compatible con Video4Linux2 y debe aparecer como /dev/video0 en el sistema de ficheros.

    sudo modprobe bcm2835-v4l2
    
Para cargar este módulo de manera permanente añadir la siguiente línea --> `bcm2835-v4l2` en el siguiente patch --> `/etc/modules`.

Instalación
------------

Clonar el repositorio y cambiar de directorio:

    git clone https://github.com/maclife26/StreamPi.git
    cd StreamPi

Ejecutar el siguiente comando dentro de la carpeta:

    python3 main.py

El Stream puede ser visto en: http://TU_HOST:8888/ (donde TU_HOST es tu dirección IP o localhost si es en la misma Rasp).


Autocomenzar
---------

Para levantar el servidor automáticamente cada vez que se reinicie la Rasp, ejecutar:

    crontab -e

... y luego añadir la siguiente línea en crontab:

    @reboot sleep 5 && /home/pi/project/StreamPi/start.sh

Remplazar la ruta dependiendo donde tengas tu carpeta con el script.

Logrotate
---------

Cuando se levanta el servidor usando el comando `start.sh` se escribirá en `server.log`. 
Para evitar que crezca de manera infinita en la siguiente ruta `/etc/logrotate.d/StreamPi.save` escribir la siguiente función

```
/home/pi/project/StreamPi/server.log {
   weekly
   rotate 4
   compress
   missingok
   copytruncate
}
```
Remplazar la ruta dependiendo donde tengas tu carpeta con el script.


