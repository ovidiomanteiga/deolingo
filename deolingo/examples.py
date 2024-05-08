
import dataclasses
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path


class ExampleReader:

    def __init__(self):
        self._examples_folder = Path(__file__).parent / "examples"

    def read_examples(self):
        """Returns a list of all examples reading from folders in /examples"""
        folders = [node for node in listdir(self._examples_folder)
                   if isdir(join(self._examples_folder, node))]
        examples_files = []
        for folder in folders:
            folder = self._examples_folder / folder
            examples_files += [folder / file for file in listdir(folder)
                               if isfile(join(folder, file)) and file.endswith(".lp")]
        files = [(self._name(file), open(file)) for file in examples_files]
        examples = [DeolingoExample(name=file[0], contents=file[1].read()) for file in files]
        return examples

    def read_example(self, example):
        """Returns an example from the examples in the /examples folder."""
        if not example.endswith(".lp") or not isfile(join(self._examples_folder, example)):
            return None
        example_file = self._examples_folder / example
        file_name = self._name(example_file)
        file_contents = open(example_file).read()
        example = DeolingoExample(name=file_name, contents=file_contents)
        return example

    @staticmethod
    def _name(file):
        return file.parent.name + "/" + file.name


@dataclasses.dataclass
class DeolingoExample:
    name: str
    contents: str
