# jetbrains-vscode

**Convert your Jetbrains Run/Debug Configrations to VSCode Run and Debug configurations.**
---

Imagine you are a [Jetbrains IDE](https://www.jetbrains.com/products/) user (IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, etc.)
and you configured your IDE to your liking. You invested a lot of time in creating [Run/Debug Configurations](https://www.jetbrains.com/help/idea/services-tool-window.html).

Now you want to be able to use another IDE such as [VSCode](https://code.visualstudio.com). Maybe as a full switch. Maybe just to feel the freedom to use whatever IDE you want. Well, you had to recreate all your run-configurations. 🤷‍♂️

## Installation instructions

Download this repository – or at least `convert.py` – to your computer.
Find your Jetbrains IDE workspace config file (`workspace.xml`) and copy it over or copy the absolute path to `workspace.yml` or copy the absolute path to `workspace.yml`.

**(Optional)** You can drop your [VSCode launch configuration](https://code.visualstudio.com/Docs/editor/debugging) (`launch.json`) over here also. All your existing Run and Debug configurations in VSCode will be replaced with all configurations from your Jetbrains IDE workspace.xml. All other settings are untouched.

```
.
├── convert.py      # The converter you will love.
├── launch.json     # (optional) Your VSCode launch configuration file.
├── workspace.xml   # Your Jetbrains IDE configuration file.
```

`convert.py` takes 2 optional command line arguments: `<source>` and `<destination>`:
    
* `<source>`: The absolute or relative path to `workspace.xml`  
* `<destination>`: The absolute or relative path to `launch.json` (output) or output directory for `launch.json`.

If none of the command line arguments are used, they fallback to `*.xml` and `launch.json`, in current directory. `*.xml` means, that each XML file in the current directory is checked (based on changes from [@dmilkie] (https://github.com/dmilkie)).

## Usage

### Usage with `workspace.xml` and `launch.json` in the same directory

```shell
$ python3 convert.py

Reading from directory <absolute path to current directory>
> workspace.xml --> found 2 entries
> launcher manifest.xml --> no configuration

> OK written to launch.json
> Copy launch.json to your VSCode project / workspace and have fun!
```

### Usage with `workspace.xml` and `launch.json` in any directory

#### Example 1 - absolute Path with output to `launch.json`
Define the output path to `launch.json`. The output directory has to exist! It will **NOT** be created from the script.

```shell
$ python3 convert.py /read/my/project/.idea/workspace.xml /output/to/launch.json

Reading from file /read/my/project/.idea/workspace.xml
> workspace.xml --> found 2 entries

> OK written to /output/to/launch.json
> Copy launch.json to your VSCode project / workspace and have fun!
```

#### Example 2 - absolute Path with output to `launching_launcher.json`
While defining the path for `launch.json`, you can use any name as the output file.

```shell
$ python3 convert.py /read/my/project/.idea/workspace.xml /output/to/launching_launcher.json

Reading from file /read/my/project/.idea/workspace.xml
> workspace.xml --> found 2 entries

> OK written to /output/to/launching_launcher.json
> Copy launching_launcher.json to your VSCode project / workspace and have fun!
```

#### Example 3 - absolute Path with output to a path
You don't have to explicitly write `launch.json` to the output. You can just use the path and file will be automatically set to `launch.json`.
```shell
$ python3 convert.py /read/my/project/.idea/workspace.xml /output/to/my/vscode_project

Reading from file /read/my/project/.idea/workspace.xml
> workspace.xml --> found 2 entries

> OK written to /output/to/my/vscode_project/launch.json
> Copy launch.json to your VSCode project / workspace and have fun!
```

#### Example 4 - dynamic resolve of source
You don't have to provide the absolute path to the `workspace.xml`. It's enough to reference the project directory. The script will automatically append `.idea` and then work on each XML file within the directory.
```shell
$ python3 convert.py /read/my/project /output/to/my/vscode_project

Reading from directory /read/my/project/.idea
> dataSources.local.xml --> no configuration
> dataSources.xml --> no configuration
> kubernetes-settings.xml --> no configuration
> misc.xml --> no configuration
> modules.xml --> no configuration
> vcs.xml --> no configuration
> workspace.xml --> found 2 entries
> profiles_settings.xml --> no configuration

> OK written to /output/to/my/vscode_project/launch.json
> Copy launch.json to your VSCode project / workspace and have fun!
```