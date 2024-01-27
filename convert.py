#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convert the configurations from your Jetbrains IDE to VSCode.

    Requirements:
        - workspace.xml:
            Copy your workspace.xml's from your Jetbrains IDE (e.g. .run folder) into this folder.
        - launch.json: (Optional)
            Copy launch.json from your Jetbrains IDE into this folder.

    Warning!
    Warning! It's overwriting all existing run configurations in launch.json file.
    Warning! But the good news is that is only overwrites the configurations.
    Warning!
"""
import sys
import json
import xml.dom.minidom
from pathlib import Path


__author__ = "github.com/topscoder"
__license__ = "UNLICENSE"


class Convert:
    def __init__(self, source: str = None, destination: str = "launch.json"):
        if source is not None:
            self.source = Path(source)

            if self.source.suffix != ".xml":
                # source is not an XML file
                if self.source.name != ".idea" and self.source.is_dir():
                    # source is not the .idea directory
                    # now we assume, that we are in the base directory of the project and append .idea
                    print(f"{bcolors.WARNING}Auto-adding '.idea' to path")
                    self.source = self.source / ".idea"

            if self.source.exists() is not True:
                print(
                    f"{bcolors.FAIL}"
                    f"Source {self.source} doesn't exist or is not accessible!"
                    f"{bcolors.ENDC}"
                )
                sys.exit(1)

        else:
            self.source = Path()

        self.destination = Path(destination)
        # If only a directory was set as destination, add launch.json as default filename
        if self.destination.suffix != ".json":
            if self.destination.is_dir():
                self.destination = self.destination / "launch.json"
            else:
                print(
                    f"{bcolors.FAIL}"
                    f"Destination {self.destination} doesn't exist or is not accessible!"
                    f"{bcolors.ENDC}"
                )
                sys.exit(1)

        self.now()

    def now(self):
        workspace_parsed = self.process_source()
        contents = {}

        with open(self.destination, "w+") as target:
            # Warning! It's overwriting all existing configurations.
            try:
                contents = json.load(target)
            except Exception:
                pass
            contents["configurations"] = workspace_parsed
            target.write(json.dumps(contents, indent=2))

            target.close()

        print("")
        print(f"> {bcolors.WHITE}OK written to {bcolors.CYAN}{self.destination}{bcolors.ENDC}")
        print(
            f"> {bcolors.WHITE}Copy {bcolors.CYAN}{self.destination.name}{bcolors.WHITE} "
            f"to your VSCode project / workspace and have fun!{bcolors.ENDC}"
        )

    def process_source(self):
        nodes_configuration = []

        if self.source.suffix == ".xml":
            print(
                f"{bcolors.WHITE}Reading from {bcolors.BOLD}file{bcolors.ENDC} {bcolors.WHITE}{self.source.absolute()}{bcolors.ENDC}"
            )
            nodes = self.parse_workspace_xml(self.source)
            if nodes:
                nodes_configuration.append(nodes)
        else:
            print(
                f"{bcolors.WHITE}Reading from {bcolors.BOLD}directory{bcolors.ENDC} {bcolors.WHITE}{self.source.absolute()}{bcolors.ENDC}"
            )
            for workspace_xml in self.source.rglob("*.xml"):
                nodes = self.parse_workspace_xml(workspace_xml)
                if nodes:
                    nodes_configuration.append(nodes)

        return nodes_configuration

    def parse_workspace_xml(self, filename: str):
        print(f"> {filename.name}", end="")
        doc = xml.dom.minidom.parse(str(filename))
        configuration_nodes = doc.getElementsByTagName("configuration")
        if len(configuration_nodes) > 0:
            print(f" --> {bcolors.GREEN}found {len(configuration_nodes)} entries{bcolors.ENDC}")
        else:
            print(f" --> no configuration")

        nodes = []
        for node in configuration_nodes:
            if node.getAttribute("type") != "PythonConfigurationType":
                continue

            if node.getAttribute("name") == "":
                continue

            if node.getAttribute("type") == "":
                continue

            vscode_node = VSCodeConfigurationElement(
                node.getAttribute("name"),
                node.getAttribute("type"),
                "launch",
                "",
                "integratedTerminal",
            )

            if node.getAttribute("folderName") == "":
                if node.getElementsByTagName("module"):
                    module_name = node.getElementsByTagName("module")[0].getAttribute("name")
            else:
                module_name = node.getAttribute("folderName")

            vscode_node.presentation["group"] = module_name

            node_options = node.getElementsByTagName("option")
            for option in node_options:
                if option.getAttribute("name") == "SCRIPT_NAME":
                    vscode_node.program = option.getAttribute("value")
                    continue

                if option.getAttribute("name") == "PARAMETERS":
                    vscode_node.args = (
                        option.getAttribute("value")
                        .replace("$PROJECT_DIR$", "${workspaceFolder}")
                        .split(" ")
                    )

                if option.getAttribute("name") == "WORKING_DIRECTORY":
                    vscode_node.cwd = option.getAttribute("value")

            nodes.append(vscode_node.as_dict())

        return nodes


class VSCodeConfigurationElement:
    """This object contains one configuration element.

    Example:
    {
        "name": "Python: Current file",
        "type": "python",
        "request": "launch",
        "runtimeExecutable": "python3",
        "program": "${file}",
        "console": "integratedTerminal",
        "args": ["--foobar"]
    }
    """

    __name: str
    conf_type: str
    __request: str
    program: str
    console: str
    cwd: str
    runtimeExecutable: str
    args: dict
    presentation: dict
    comment: str

    def __init__(self, el_name, conf_type, request, program, console):
        self.__name = el_name
        self.conf_type = conf_type
        self.__request = request
        self.program = program
        self.console = console
        self.cwd = "${workspaceFolder}"
        # self.runtimeExecutable = 'python3'
        self.args = {}
        self.presentation = {"hidden": False, "group": "Default"}

        self.comment = (
            "Automatically converted from " "Jetbrains IDE workspace.xml " "to VSCode launch.json"
        )

    def as_dict(self):
        return {
            "type": self.conf_type,
            "name": self.__name,
            "request": self.__request,
            # 'runtimeExecutable': self.runtimeExecutable,
            "program": self.program,
            "console": self.console,
            "args": self.args,
            "presentation": self.presentation,
            "cwd": self.cwd,
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "conf_type":
            self.__dict__[name] = value.replace("PythonConfigurationType", "python")

        if "$PROJECT_DIR$" in value:
            self.__dict__[name] = value.replace("$PROJECT_DIR$", "${workspaceFolder}")


class bcolors:
    WHITE = "\033[37m"
    PINK = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


if __name__ == "__main__":
    try:
        Convert(source=sys.argv[1], destination=sys.argv[2])
    except IndexError:
        Convert()
