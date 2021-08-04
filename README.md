# jetbrains-vscode

**Convert your Jetbrains Run/Debug Configrations to VSCode Run and Debug configurations.**
---

Imagine you are a [Jetbrains IDE](https://www.jetbrains.com/products/) user (IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, etc.)
and you configured your IDE to your liking. You invested a lot of time in creating [Run/Debug Configurations](https://www.jetbrains.com/help/idea/services-tool-window.html).

Now you want to be able to use another IDE such as [VSCode](https://code.visualstudio.com). Maybe as a full switch. Maybe just to feel the freedom to use whatever IDE you want. Well, you had to recreate all your run-configurations. 🤷‍♂️

## Installation instructions

Download this repository – or at least `convert.py` – to your computer.
Find your Jetbrains IDE workspace config file (`workspace.xml`) and copy it over.

**(Optional)** You can drop your [VSCode launch configuration](https://code.visualstudio.com/Docs/editor/debugging) (`launch.json`) over here also. All your existing Run and Debug configurations in VSCode will be replaced with all configurations from your Jetbrains IDE workspace.xml. All other settings are untouched.

```
.
├── convert.py      # The converter you will love.
├── launch.json     # (optional) Your VSCode launch configuration file.
├── workspace.xml   # Your Jetbrains IDE configuration file.
```

## Usage

```shell
$ python3 convert.py

> OK written to launch.json.
> Copy launch.json to your VSCode project / workspace and have fun!
```