# Gyver Lamp python class

Working with Gyver firmware https://github.com/AlexGyver/GyverLamp

### Usage

```
from GyverLamp import Lamp, Effect

lamp = Lamp("192.168.0.67")

lamp.enable()
lamp.effect = Effect.FIRE
lamp.brightness = 200

```