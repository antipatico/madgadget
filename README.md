# madgadget

A CLI tool to quickly pull and patch (android) packages.

As of today, madgadget only supports android and linux. If anyone desires to extend its functionality to other OS-es, feel free to open a MR!

Heavily work in progress, will (eventually) update this README further along the way.

## Installing

### Requirements

As of today, the tool uses [apktool](https://github.com/iBotPeaches) behind the scenes. Please download it and put somewhere.

Then, add the following `apktool` SCRIPT in your PATH (remember to `chmod +x`):

```bash
#!/usr/bin/env bash

set -eu
jarpath="/PATH/TO/YOUR/apktool-cli-all.jar"
javaoptions='-Dfile.encoding=utf-8'
java "${javaoptions}" -jar "${jarpath}" "$@"
```

### Install from PyPi

```bash
python3 -m pip install madgadget
```

### Installation from source

```bash
python3 -m pip install flit
python3 -m flit install
```

## Usage

### Pulling split apks from connected device
1. Connect the device and be sure to have a functional adb connection (you can check if `adb shell` works)
2. Pull all apks of target app with:
```bash
madgadget pull com.target
```

### Injecting frida gadget + script in target apk
1. Once you pulled your target, you can inject a script with the following:
```bash
madgaget inject com.target.apk test_script.js
```

**NOTE**: as of today only lief binary injection method is supported, meaning that you have to select a binary having at least one native library.

**NOTE**: with the injection method used today, you have no guarantee you are going to run 'early' enough in your target application.

**NOTE**: if you are trying to patch a split config, you can either target an apk having multiple arch under the `lib/` folder or an architecture-specific apk splitconfig.


## TODOs

* remove apktool and move to Jython and [APKEditor](https://github.com/REAndroid/APKEditor).
* add merge functionality
* add functionality to embed frida gadget without script and custom configuration
* add functionality to specify frida gadget version
* allow different injection methods (now we are based on lief + so patching, but it would be cool to support smali patching too)

## Author

Jacopo antipatico Scannella

## Disclaimer

This tool is heavily inspired by [objection](https://github.com/sensepost/objection), which in turns uses [Frida](https://frida.re). If you want to make donations, donate to those amazing projects.

> If I have seen further, it is by standing on the shoulders of giants - Isaac Newton.
