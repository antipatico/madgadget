# madgadget

A CLI tool to quickly pull and patch (Android) multiarch packages.

As of today, madgadget only supports Android (target) and Linux (host). If anyone desires to extend its functionality to other OS-es, feel free to open a MR!

Heavily work in progress.

## Usage

```
$ madgadget -h
usage: madgadget [-h] [--version] {pull,inject} ...

Embed frida gadgets into android multiarch applications

positional arguments:
  {pull,inject}  Desired action
    pull         Pull a (split) package from a connected device
    inject       Inject frida-gadget inside a locally-stored package

options:
  -h, --help     show this help message and exit
  --version      show program's version number and exit

Author: Jacopo (antipatico) Scannella
```

```
$ madgadget pull -h
usage: madgadget pull [-h] [-o OUTPUT] package_name

positional arguments:
  package_name          The name of the package you want to pull (E.G. com.android.settings)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory path
```

```
$ madgadget inject -h
usage: madgadget inject [-h] [-o OUTPUT] [-A] apk script

positional arguments:
  apk                   Android apk you want to inject frida gadget to
  script                Frida script you want to inject, javascript only

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file
  -A, --apktool         Use Apktool instead of APKEditor (Default: False)
```

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

**NOTE**: if you are trying to patch a multi-arch apk, you can either target an apk having multiple arch under the `lib/` folder or an architecture-specific apk splitconfig.



## Installation

### Requirements

* **[APKEditor](https://github.com/REAndroid/APKEditor)** (default) or **[Apktool](https://github.com/iBotPeaches)**
* **[zipalign]()** (optional, if using Apktool)

As of today, `madgadget` uses [APKEditor](https://github.com/REAndroid/APKEditor) behind the scenes. Please download it and put somewhere.

Then, add the following `apkeditor` script in your **PATH** (remember to `chmod +x`):

```bash
#!/usr/bin/env bash

set -eu
jarpath="/PATH/TO/YOUR/APKEditor.jar"
javaoptions='-Dfile.encoding=utf-8'
java "${javaoptions}" -jar "${jarpath}" "$@"
```

As an alternative, you can decide to use [Apktool](https://github.com/iBotPeaches). Provide a similar `apktool` script in your **PATH** to the one described above for APKEditor.
In the future, I plan to use Jython to overcome this usability issue.

### Install from PyPi

```bash
python3 -m pip install madgadget
```

### Installation from source

```bash
python3 -m pip install flit
python3 -m flit install
```

## TODOs

* embed jar and move to Jython
* add merge functionality
* add functionality to embed frida gadget without script and custom configuration
* add functionality to specify frida gadget version
* allow different injection methods (now we are based on lief + so patching, but it would be cool to support smali patching too)
* allow to specify lief target
* change strategy to select so target by building dag

## Author

Jacopo antipatico Scannella

## Disclaimer

This tool is heavily inspired by [objection](https://github.com/sensepost/objection), which in turns uses [Frida](https://frida.re). If you want to make donations, donate to those amazing projects.

> If I have seen further, it is by standing on the shoulders of giants - Isaac Newton.
