#!/usr/bin/python3
"""Convert snippet from Kate/KDevelop to VSCode and vice versa """
import argparse
import json
import os.path
import re
import xml.etree.ElementTree as ET
from enum import Enum
from pathlib import Path
from typing import TypedDict

from snippetconverter.languages import (
    get_language_identifier_for_vscode,
    induce_language_from_file_name,
)


class IDE(Enum):
    """Type of IDE"""

    UNKNOWN = 1
    KATE = 2
    VSCODE = 3


def usage():
    """Tells user how to use this module"""
    print(
        "--input $HOME/.local/share/ktexteditor_snippets/CMake.xm --output $HOME/.config/Code/User/snippets/cmake.json"
    )


def induce_ide_from_file(filename):
    """Induce which IDE was used to create the file based on its name"""
    if "ktexteditor" in filename or "kdevelop" in filename:
        return IDE.KATE
    if "Code/User" in filename:
        return IDE.VSCODE
    return IDE.UNKNOWN


class Variable(TypedDict):
    """@brief This describe a variable in a snipppet.
    @member name the name of the variables without specific extras like ( { $ etc e.g. foobar
    @member original text the original full text e.g. ${foobar}
    """

    name: str
    originaltext: int


class Snippet:
    # pylint: disable=R0903
    """@brief This describe a snippet
    @member name the name of the snippet (this is what tyou gonna type in the IDE to match the snippet)
    @member content the content of the snippet
    @member variables the list of variables contained in this snippet. They will have to be formatted in the output IDE format when creating a new snippet file!
    """

    def __init__(self, name, content, variables):
        self.name = name
        self.content = content
        self.variables = variables

    def to_vs_code(self, language):
        """
        @brief print the snippet into Visual Studio Code format
        @param language the language (c++, python, javascript, brainfuck... )relevant for this snippet
        """
        contentlist = self.content.split("\n")
        # See https://code.visualstudio.com/docs/editor/userdefinedsnippets
        for content in enumerate(contentlist):
            for variable in self.variables:
                if variable["original_text"] in content[1]:
                    content[1].replace(
                        variable["original_text"], str("{" + variable["name"] + "}")
                    )

        return dict(
            {
                "scope": get_language_identifier_for_vscode(language),
                "prefix": self.name,
                "body": contentlist,
                "description": "",
            }
        )


def get_variable_lists_from_kate_snippet(content):
    """@brief this extract all the variables that exist inside a Kate Snipppet
    @param content this is the content (array of lines) of the snippet
    """
    variables = []
    for line in content:
        for original_text in re.findall(r"\$\{[\w|\s]+\}", line):
            name = re.sub(r"\$\{", "", original_text)
            name = re.sub(r"\}", "", name)
            name = re.sub(r" ", "_", name)
            if name not in [var["name"] for var in variables]:
                variable = Variable({"name": name, "original_text": original_text})
                variables.append(variable)
    return variables


def convert_from_kate_to_vscode(katensippet: Path, vscodesnippet: Path):
    """
    @brief Convert a snippet from a Kate/KDevelop snippet format to a visual studio code
    @param katensippet. URL of the Kate snippet file
    @param vscodesnippet. URL of the Visual Studio Code snippet file
    """
    snippets = []

    # First we parse the Kate xml snippet to get a list of snippet that written in the file
    tree = ET.parse(katensippet.absolute())
    root = tree.getroot()
    for items in root.findall("item"):
        match = items.find("match")
        fillin = items.find("fillin")
        variables = get_variable_lists_from_kate_snippet(fillin.text.split("\n"))
        snippets.append(Snippet(match.text, fillin.text, variables))
    # Second we induce which language it is
    language = induce_language_from_file_name(str(katensippet.absolute()))

    outputsnippets = {}
    for snippet in snippets:
        outputsnippets[snippet.name] = snippet.to_vs_code(language)

    with open(vscodesnippet.absolute(), "w", encoding="utf-8") as vscode_snippetfile:
        vscode_snippetfile.write(json.dumps(outputsnippets, indent=4, sort_keys=True))


def convert_vscode_to_kate(vscodesnippet, katesnippet):
    # pylint: disable=W0613
    """@brief Convert a Visual Studio Code snippet to a Kate Snippet
    @param vscodesnippet URL to the visual studio snippet file
    @param katesnippet URL to the Kate/KDevelop snippet file"""
    raise NotImplementedError(
        "Conversion from Visual Studio to Kate is not yet implemented"
    )


def main():
    """module main"""
    argument_parser = argparse.ArgumentParser(
        description="Kate to VSCode snippet converter"
    )
    argument_parser.add_argument(
        "-i", "--input", help="input snippet file", required=True
    )
    argument_parser.add_argument(
        "-o", "--output", help="output snippet file", required=True
    )
    args = argument_parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(str(f"Input file: {args.input} does not exist"))

    ide_in = induce_ide_from_file(args.input)
    ide_out = induce_ide_from_file(args.output)
    if ide_in == IDE.UNKNOWN:
        raise RuntimeError(
            str(f"Could not find which IDE the input file {args.input} comes from.")
        )
    if ide_out == IDE.UNKNOWN:
        raise RuntimeError(
            str(f"Could not find which IDE the output file {args.output} comes from.")
        )

    if ide_in == IDE.KATE and ide_out == IDE.VSCODE:
        convert_from_kate_to_vscode(Path(args.input), Path(args.output))
    if ide_in == IDE.VSCODE and ide_out == IDE.KATE:
        convert_vscode_to_kate(Path(args.input), Path(args.output))
