# Push the button - and make Volumio do something

Buttons are actually quite straight-forward: Once connected to a pin, they either do or don't emit 3.3V which is interpreted by the PI as true or false.

Again, a python script registers functions to be executed, the volumio command line API provides the necessary features.

A service executes the script on startup:
Copy the `VolumioButtons.service` to `/lib/systemd/system/` and make sure it has `644` permissions.

## Links

- [original script from the Junior Jukebox Tutorial](http://www.raspis-world.de/p/raspberry-pi-als-junior-jukebox-der_19.html) (german, uses infinite polling though)
- [Alternatives for running the Python script as service](https://www.raspberrypi.org/forums/viewtopic.php?t=197513)