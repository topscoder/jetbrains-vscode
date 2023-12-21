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
from pathlib import Path
from os import getcwd
import json
import xml.dom.minidom


__author__ = "github.com/topscoder"
__license__ = "UNLICENSE"


class Convert():
    def __init__(self):
        self.now()

    def now(self):
        workspace_parsed = self.parse_workspace_xml()
        contents = {}

        with open('launch.json', 'w+') as target:
            # Warning! It's overwriting all existing configurations.
            try:
                contents = json.load(target)
            except Exception:
                pass
            contents['configurations'] = workspace_parsed
            target.write(json.dumps(contents, indent=2))

            target.close()

        print('> OK written to launch.json.')
        print('> Copy launch.json to your VSCode project / workspace '
              'and have fun!')

    def parse_workspace_xml(self) -> list:
        cwd = Path(getcwd())
        nodes = []
        xml_files = cwd.rglob("*.xml")
        for workspace_xml in cwd.rglob("*.xml"):
            print(f'> reading {str(workspace_xml)}')
            doc = xml.dom.minidom.parse(str(workspace_xml))
            configuration_nodes = doc.getElementsByTagName('configuration')

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
                        vscode_node.args = option.getAttribute('value').replace('$PROJECT_DIR$','${workspaceFolder}').split(' ')

                    if option.getAttribute('name') == 'WORKING_DIRECTORY':
                        vscode_node.cwd = option.getAttribute('value')

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
        self.cwd = '${workspaceFolder}'
        # self.runtimeExecutable = 'python3'
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
            # 'runtimeExecutable': self.runtimeExecutable,
            'program': self.program,
            'console': self.console,
            'args': self.args,
            'presentation': self.presentation,
            'cwd': self.cwd
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
    Convert()
