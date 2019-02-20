# NFC Jukebox - not only for kids

Every parent of an audiobook-addict little one comes to the point: There is not a single good portable audio system which can be operated by children which can play the already bought CDs (or converted-to MP3s) - and we'll not even talk about the sound. As a friend of mine noted: There is no product category on Amazon rated as bad as children's audio players.

But there is one exception: The [Toniebox](https://tonies.com/toniebox/). It is awesome, no doubt about that. World class with respect to build quality, usability - and business model. The latter majorly benefits the company, not the consumer: 15€/audiobook is a lot. And it feels unneccessary when already having signed a spotify subscription.

So I was looking for a do-it-yourself alternative. Though there are awesome projects, none matched my needs perfectly. So as a software engineer, of course (I thought) I could create an own version.

## Requirements

Primary consumer of the system will be my four year old son who loves audio books - but also listens to real music (current favourite: [Jukebox the ghost](https://www.youtube.com/watch?v=dZ_Jp2w9XSg) :) )
It shall be operated similar to the Toniebox for him (but using self-programmable NFC tags), without the need to connect a mobile phone. Big buttons rule the small hands' world.

But having it at home, I'd like to use it myself as well, so it also has to satisfy my needs: Take it to the garden in summer and stream something from my NAS or spotify. It should be operatable using my mobile (for easy browsing).
Finally, programming new audiobooks should be possible without further programming skills - my wife should be able to do it.

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

### Wiring

The first step of course is to wire up things. Here's a hopefully complete list of how to connect the components

```
                             Pin 1 Pin2
> Power 3.3V             +  3V3 [P] [A] +5V                  > Amp Vin
                 SDA1 / GPIO  2 [ ] [ ] +5V
> Power          SCL1 / GPIO  3 [P] [P] GND                  > Power GND
> Btn 3.3V out          GPIO  4 [B] [ ] GPIO 14 / TXD0
                            GND [ ] [ ] GPIO 15 / RXD0
> Btn Play              GPIO 17 [B] [A] GPIO 18              > Amp BCLK
                        GPIO 27 [ ] [ ] GND
> Btn Prev              GPIO 22 [B] [B] GPIO 23              > Btn Next
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

`A`: Amp
`N`: NFC Reader
`B`: Pushbutton
`P`: Powerbutton (lighted)


## References / Links

- [Junior Jukebox](http://www.raspis-world.de/p/raspberry-pi-als-junior-jukebox-der_19.html) (german)