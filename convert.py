#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Convert the configurations from your Jetbrains IDE to VSCode.

    Requirements:
        - workspace.xml:
            Copy your workspace.xml from your Jetbrains IDE into this folder.
        - launch.json: (Optional)
            Copy launch.json from your Jetbrains IDE into this folder.

    Warning!
    Warning! It's overwriting all existing configurations in launch.json file.
    Warning! But the good news is that is only overwrites the configurations.
    Warning!
"""

import sys
import json
import xml.dom.minidom
from pathlib import Path


__author__ = "github.com/topscoder"
__license__ = "UNLICENSE"


class Convert():
    def __init__(self, source: str = "workspace.xml", destination: str = "launch.json"):
        self.source = Path(source)
        self.destination = Path(destination)
        # If only a directory was set as destination, add launch.json as default filename
        if self.destination.suffix != ".json":
            self.destination = self.destination / "launch.json"
        
        self.now()

    def now(self):
        workspace_parsed = self.parse_workspace_xml()
        contents = {}

        with open(self.destination, 'w+') as target:
            # Warning! It's overwriting all existing configurations.
            try:
                contents = json.load(target)
            except Exception:
                pass
            contents['configurations'] = workspace_parsed
            target.write(json.dumps(contents, indent=2))

            target.close()

        print(f'> OK written to {self.destination}')
        print(f'> Copy {self.destination.name} to your VSCode project / workspace '
              'and have fun!')

    def parse_workspace_xml(self) -> list:
        doc = xml.dom.minidom.parse(str(self.source))
        configuration_nodes = doc.getElementsByTagName('configuration')
        nodes = []

        for node in configuration_nodes:
            if node.getAttribute('type') != 'PythonConfigurationType':
                continue

            if node.getAttribute('name') == '':
                continue

            if node.getAttribute('type') == '':
                continue

            vscode_node = VSCodeConfigurationElement(
                node.getAttribute('name'),
                node.getAttribute('type'),
                'launch',
                '',
                'integratedTerminal'
            )

            if node.getElementsByTagName('module'):
                module_name = node.getElementsByTagName('module')[0] \
                                    .getAttribute('name')
                vscode_node.presentation['group'] = module_name

            node_options = node.getElementsByTagName('option')
            for option in node_options:
                if option.getAttribute('name') == 'SCRIPT_NAME':
                    vscode_node.program = option.getAttribute('value')
                    continue

                if option.getAttribute('name') == 'PARAMETERS':
                    vscode_node.args = option.getAttribute('value').split(' ')

            nodes.append(vscode_node.as_dict())

        return nodes


class VSCodeConfigurationElement():
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

        self.runtimeExecutable = 'python3'
        self.args = {}
        self.presentation = {
            'hidden': False,
            'group': 'Default'
        }

        self.comment = ('Automatically converted from '
                        'Jetbrains IDE workspace.xml '
                        'to VSCode launch.json')

    def as_dict(self):
        return {
            'type': self.conf_type,
            'name': self.__name,
            'request': self.__request,
            'runtimeExecutable': self.runtimeExecutable,
            'program': self.program,
            'console': self.console,
            'args': self.args,
            'presentation': self.presentation
        }

    def as_json(self):
        return json.dumps(self.as_dict())

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'conf_type':
            self.__dict__[name] = value.replace(
                'PythonConfigurationType',
                'python'
            )

        if '$PROJECT_DIR$' in value:
            self.__dict__[name] = value.replace(
                '$PROJECT_DIR$',
                '${workspaceFolder}')


if __name__ == '__main__':    
    try:
        Convert(source=sys.argv[1], destination=sys.argv[2])
    except IndexError:
        Convert()