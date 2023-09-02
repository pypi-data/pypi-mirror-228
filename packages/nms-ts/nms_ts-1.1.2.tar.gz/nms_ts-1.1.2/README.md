NMS Lore Translator
===
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/E1E0DESP9)
![Publish to PyPi](https://github.com/da-code-a/nms-translator/actions/workflows/publish.yml/badge.svg)

With the Echoes update, No Man's Sky introduced some dialogue written in binary. I created this tool so that I could easily grab the screen, extract the binary text, and then convert it to UTF-8 characters. It will then append each new bit of lore to a file in your home folder.

Caveats
---

This was only tested on Ubuntu 23.04 with a screen resolution of 1920x1080 and the game running in full screen. It should, theoretically, work on any OS with the Tesseract OCR library installed, but it has not at all been tested and I take no responsibilites for this.

Installation
---

You can either clone this repository and then run `poetry build && pip3 install --user dist/nms_ts-<version>-py3-none-any.whl` or you can install from PyPi with just `pip3 install --user nms-ts`

Usage
---

The script runs and copies everything it sees on the screen within the resolution as soon as you call it. This could cause issues if your terminal pops up over the game as it will try to read binary from that as well and then fail because it's not proper binary. I would suggest, instead, binding to a hotkey:

```
nms --xend=<your X resolution> --yend=<your Y resolution>
```
Then, when you hit your hotkey, it will run the script without launching a terminal, therefore introducing no confusion for the script. Doing it like that will make it capture your entire display and attempt to extract from there. However, you can also specify just a small portion of your screen (to get a more exact area to translate and minimize possible errors) by specifying more exact `xstart`, `ystart`, `xend` and `yend` values.


Changelog
---

* v1.1.2
  * Actually fixed the damn thing
* v1.1.1
  * Fixed capture and translate
* v1.1.0
  * Added option to set boundary box
  * Made it so that values actually get passed to grab function
  * Now filters out characters that are not proper binary digits
* v1.0.0
  * Initial release