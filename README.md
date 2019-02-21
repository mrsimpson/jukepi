# NFC Jukebox - not only for kids

Every parent of an audiobook-addict little one comes to the point: There is not a single good portable audio system which can be operated by children which can play the already bought CDs (or converted-to MP3s) - and we'll not even talk about the sound. As a friend of mine noted: There is no product category on Amazon rated as bad as children's audio players.

But there is one exception: The [Toniebox](https://tonies.com/toniebox/). It is awesome, no doubt about that. World class with respect to build quality, usability - and business model. The latter majorly benefits the company, not the consumer: 15€/audiobook is a lot. And it feels unneccessary when already having signed a spotify subscription.

So I was looking for a do-it-yourself alternative. Though there are awesome projects, none matched my needs perfectly. So as a software engineer, of course (I thought) I could create an own version.

## Requirements

Primary consumer of the system will be my four year old son who loves audio books - but also listens to real music (current favourite: [Jukebox the ghost](https://www.youtube.com/watch?v=dZ_Jp2w9XSg) :) )
It shall be operated similar to the Toniebox for him (but using self-programmable NFC tags), without the need to connect a mobile phone. Big buttons rule the small hands' world.

But having it at home, I'd like to use it myself as well, so it also has to satisfy my needs: Take it to the garden in summer and stream something from my NAS or spotify. It should be operatable using my mobile (for easy browsing).
Finally, programming new audiobooks should be possible without further programming skills - my wife should be able to do it.

## The final solution 

I combine

- A Raspberry PI 3 B
- Some soldered components for the PI (no fear, it's really easy to do)
- A passive DIY loudspeaker
- Volumio + plugins

## Hardware

The following section describes the hardware I chose, followed by how to wire it.
Major objectives were to have a *portable* (in the sense it can be operated without power cord), *musical quality* (in the sense of "I can not only play audiobooks, but also rock music") and *low budget* (in the sense of "get the cheapest component for the job, not the one which is most comfortable to implement") audio system.

*Remark: There are many tutorials out there utilizing the same hardware I did, but wiring it up differently or installing additional drivers. Don't do this unless you've got very good reason and know what you're doing. I'll document everything from wiring to software, each step further down below.*

### Amplifier and DAC

My main objective was to use an amp which does not need a separate power supply. I selected the super-cheap-and-tiny [Adafruit MAX98357](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp). It does not only amplify the sound to a level which is more than reasonable for children's audio books and uses the digital I2S-interface. Finally, it's mono implicitly mixed down - which is a feature imho (since I wanted only one driver in the case).

The [wiring is well documented](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-wiring)

### NFC reader

The [RC522 NFC reader](https://www.amazon.com/s?k=rc522+rfid+reader&i=electronics) is a very low budget (6€) board. Soldering is comparatively easy (you only have to solder the pins). I works well through 10mm wood.
The reader is connected using the digital SPI bus, so as far as I can tell you can also replace it with any other SPI based USB NFC reader.

### Illuminated buttons

Is there anything more attractive than buttons that can be hit with force by a child? Yes: Illuminated buttons - that can be hit with all force available to turn up the volume.
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

### Wiring

The first step of course is to wire up things. Here's a hopefully complete list of how to connect the components

```
                             Pin 1 Pin2
> Power 3.3V             +  3V3 [P] [A] +5V                  > Amp Vin
                 SDA1 / GPIO  2 [ ] [ ] +5V
> Power          SCL1 / GPIO  3 [P] [P] GND                  > Power GND
> Btn 3.3V out          GPIO  4 [B] [ ] GPIO 14 / TXD0
                            GND [ ] [ ] GPIO 15 / RXD0
> Btn Prev              GPIO 17 [B] [A] GPIO 18              > Amp BCLK
                        GPIO 27 [ ] [ ] GND
> Btn Play              GPIO 22 [B] [B] GPIO 23              > Btn Next
> NFC 3.3V                 +3V3 [N] [ ] GPIO 24
> NFC MOSI       MOSI / GPIO 10 [N] [A] GND                  > Amp GND
> NFC MISO       MISO / GPIO  9 [N] [N] GPIO 25              > NFC RST
> NFC SCK        SCLK / GPIO 11 [N] [N] GPIO  8 / CE0#       > NFC SDA
> NFC GND                   GND [N] [ ] GPIO  7 / CE1#
                ID_SD / GPIO  0 [ ] [ ] GPIO  1 / ID_SC
> Btn Vol +             GPIO  5 [B] [ ] GND
> Btn Vol -             GPIO  6 [B] [ ] GPIO 12
                        GPIO 13 [ ] [ ] GND
> Amp LRCLK      MISO / GPIO 19 [A] [ ] GPIO 16 / CE2#
                        GPIO 26 [ ] [ ] GPIO 20 / MOSI
                            GND [ ] [A] GPIO 21 / SCLK       > Amp DIN
                            Pin 39 Pin 40
```
[Kudos to the pinout ascii-art](http://weyprecht.de/2015/11/30/raspberry-pi-ascii-art/)

Legend

- `A`: Amp
- `N`: NFC Reader
- `B`: Pushbuttons (illuminated)
- `P`: Powerbutton (illuminated)

## Software

### Foundation: Volumio

[Volumio](https://volumio.org) is an incredible project which has all the features we needed to start from:

- Open Source (GPL v3)
- Active community, [hosted on Github](https://github.com/volumio/volumio2)
- Incredibly [well documented](http://docs.volumio.org/) with web based APIs (websocket and Rest)
- A really nice UI for desktop as well as for mobile
- A plugin infrastructure which allows to program extensions without modifying the core.

### Install Volumio

This is the easiest part - unless you start doing more that necessary. Just install it, don't do more than that. It is [well documented](https://volumio.org/get-started)

### Configure Volumio

Once Volumio has been extracted onto the disk, it will launch a wireless network. Select "I have an I2S DAC" and choose your DAC from the list.

After a reboot, you should hear the start sound (unless configured differently). You may load an MP3 to your `INTERNAL` storage (see the Volumio docs on how to do that) or play it from USB to make sure the wiring of the AMP is correct.

Next, we'll install plugins granting us access to the peripherals we wired up earlier-on.
For this, I implemented plugins which are not (yet) official or which I tuned for my needs.

In order to be able to install those unoffical plugins, you need to log-in using a terminal (SSH). Don't be afraid if you're not used to using a command line, it doesn't hurt.
And again, there is a nice documentation in Volumio [how to get SSH access](https://volumio.github.io/docs/User_Manual/SSH.html) and [how to install unoffical plugins](https://volumio.github.io/docs/Plugin_System/Plugin_System_Overview#page_How_to_install_an_unoffical_plugin)

#### Clone my repository

I'll go and install the plugins all from my repository. I know those work well (Volumio version 2.555 by the time of writing), so this is where we're going to pull them from.

from your home directory on the PI:

`git clone 
https://github.com/mrsimpson/volumio-plugins`

### Pushbuttons

There is a wonderful, but now unmaintained plugin for configuring pushbuttons in Volumio. I maintained the official version and adapted it for children's operations (longer debounce-time for the buttons) in my repository..

We need to set up our system once to allow for compilation of local binaries:

```bash
sudo apt-get update
sudo apt-get install build-essential
```

and then install the actual plugin

```bash
cd ~/volumio-plugins/plugins/system_controller/gpio-buttons/
npm i
volumio plugin install
```

Before we can map all the buttons, we need to make sure they emit a `high` signal. There are various ways to achieve this (from wiring the buttons differently to adding external resistors). I'll go for the software solution and configure the internal resistors at boot time. Also for this, [there are various (even better)](https://www.raspberrypi.org/documentation/configuration/pin-configuration.md) ways to achieve this, but editing the `/boot/config.txt` is most achievable to me (and probably the most dirty).

`sudo nano /boot/config.txt`

Add `gpio=5,6,17,22,23=ip,pu`, explicitly making those pin inputs which can be detected

and reboot `sudo reboot`

### Optional: Illumination

In case you also bought those strange flipper buttons which make all little boys' eyes laugh but you cry: The way we wired things, the buttons LEDs should not be shining by now. You'll need to given them 3.3V:

`sudo nano /boot/config.txt`

Add `gpio=4,op,dh`, which will light-them-up once the system has booted

and reboot `sudo reboot`

### NFC reader integration

Enable the SPI bus
`sudo nano /boot/config.txt`

Add `dtparam=spi=on`

Afterwards, install the plugin. Be patient, this may take a while! If it takes more than ten minutes, abort (`Ctrl+C`) and retry.

```bash
cd ~/volumio-plugins/plugins/user_interface/raspi_nfc_spi/
npm i
volumio plugin install
```

Unfortunately, we're not done yet. Until [PR #1702](https://github.com/volumio/Volumio2/pull/1702) has been included into volumio, we'll not be able to keep the NFC tag on the reader while playing - the playlist would keep starting again and again.
Thus, we need to install a custom version of volumio for the time being:

` volumio pull https://github.com/mrsimpson/volumio2`

### Poweroff

We'll not have an explicit power off. This can be frustrating as children often just push any button to see what happens. Instead, we'll have an idle-power-off-timer. This will shut the system down if nothing is played for a configurable duration.

```
cd volumio-plugins/plugins/system_controller/auto_off/

volumio plugin install
```

In case you desperately need the explicit power off, feel free to configure the GPIO button in the buttons-plugin.

### Startup

Last not least, we also want to power-on the complete system by pushing a button. As of the recent raspbian distributions, there is an "onboard-mechanism" for that. Once more, we need to head into the `/boot/config`

Add `dtoverlay=gpio-shutdown`

For further details, see the discussions about the [overlay for the startup](https://raspberrypi.stackexchange.com/questions/77905/raspberry-pi-3-model-b-dtoverlay-gpio-shutdown)

### Troubleshooting

#### where can I get the log

- Observe what volumio complains about (technically): `tail -f /var/log/volumio.log`

#### Plugin cannot be installed

- If it appears to be already installed, use `volumio plugin refresh` to replace it

#### Startup performance

- `systemd-analyze critical-chain`

## Appendix

### `/boot/config.txt`

```
### own settings
gpio=5,6,17,22,23=ip,pu
gpio=4=op,dh
dtparam=spi=on
dtoverlay=gpio-shutdown

#### Volumio i2s setting below: do not alter ####
dtoverlay=hifiberry-dac
```

## References / Links

- [Junior Jukebox](http://www.raspis-world.de/p/raspberry-pi-als-junior-jukebox-der_19.html) (german)