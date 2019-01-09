# How to activate Mifare RC522

We use the SPI as device, so we need to activate it in the kernel:

In `/boot/config.txt`: `dtparam=spi=on`

Validate using `lsmod | grep spi` => find `spidev` and `spi_bcm2835`

For the driver, we need python and a compiler for the current platform:

```bash
sudo apt-get install python2.7-dev build-essential
```

and the actual driver:
`git clone https://github.com/lthiery/SPI-Py.git`, `sudo python setup.py install`

Finally, a library simplifies programming to it:
`git clone https://github.com/pimylifeup/MFRC522-python.git`

## Links

- [original script from the Junior Jukebox Tutorial](http://www.raspis-world.de/p/raspberry-pi-als-junior-jukebox-der_19.html) (german-
- [Simplified library and bootstrapping code](https://pimylifeup.com/raspberry-pi-rfid-rc522/)
