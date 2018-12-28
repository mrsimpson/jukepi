# jukepi
Scripts for a Pi-Based jukebox

## Hardware

### Illuminated buttons

Is there anything more attractive than buttons that can be hit with force by a child? Yes: Illuminated buttons that can be hit with force.
I found [those](https://www.amazon.de/gp/product/B0771K36FT/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) - but they didn't have a specification nor a plan how to connect them.
Via (very painful) trial and error, I found the following connectivity to be working:
```

    3.3V    GND     <- outside the black "inner box"
 
 ________________   <- the black "inner box"
|                |
|                |
|  target   GND  |
|   pin          |
|________________|
```