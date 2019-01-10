# Accesing NFC via Node.JS

Since we'll most likely be using a node.js based player (Volumio), there's good reason  to also implement the NFC reader in Javascript.

This will alllow to migrate the code to a volumio plugin lateron.

## References

- [An npm package for accessing the mfrc522-rpi](https://www.npmjs.com/package/mfrc522-rpi)

## Troubleshooting

Installation of `mfrc522-rpi` fails making wiring-pi? The gcc is likely missing in your distribution => `sudo apt-get install build-essential`