import os
import tomllib
import re
from .custom_asserts import NotString, NotFileBlock
from .custom_datatypes import FileBlock
from .regex_expressions import regex_expressions

# Setup configs
with open('config.toml', 'rb') as config_toml:
    config = tomllib.load(config_toml)


class file_object:
    """The File Object is where all file components live.
    Requires a name and a directory to create a file objects.

    Optionals:
    'manual' - Switches file_object creation to manual.

    Returns a file_object.
    """
    def __init__(self, name: str, directory: str, *args, **kwargs):
        assert isinstance(name, str), NotString(name)
        assert isinstance(directory, str), NotString(directory)

        self.regex = regex_expressions()
        self.name = name
        self.dir = directory

        if 'manual' in args:
            self.mode = 'manual'
        else:
            self.mode = 'auto'
            self.auto_build()

    def auto_build(self):
        """Automatically builds the project"""
        file_data = self.stitch_file()
        self.store_blocks(file_data)
        self.build_links()
        self.build_blocks()

    def stitch_file(self) -> str:
        """Uses a generator to read all lines in file.
        Returns the entire file.
        """
        file_lines = []
        for line in self.read_lines():
            file_lines.append(line)
        file_data = '\n'.join(file_lines)
        return file_data

    def read_lines(self):
        """This is a generator function and should be called
        with the stitch_files function.
        """
        with open(self.dir, 'r', encoding='UTF-8') as file:
            for line in file:
                yield line.strip()

    def store_blocks(self, file_data: str) -> FileBlock:
        """Strips all blocks found and ommits '\\n'
        Returns a FileBlock object if manual mode is selected
        else sets self.fileblock to the FileBlock object.
        """
        assert isinstance(file_data, str), NotString(file_data)
        replace_block_temp = 'uHG49rz7qv!6y5@%Bf2G'
        blocks_found = re.findall(self.regex.block, file_data)

        # Strip trailing, leading and lonely '\n'
        blocks = [tuple(
            element.strip() for element in block if element != '\n'
        ) for block in blocks_found]
        ###

        # Deletes all blocks
        file_data = '\n'.join([element for element in ((
            re.sub(self.regex.block, replace_block_temp, file_data)
        ).split('\n')) if element != replace_block_temp])
        ###

        if self.mode == 'auto':
            self.fileblock = FileBlock(file_data, blocks)
        else:
            return FileBlock(file_data, blocks)

    def build_links(self, **kwargs):
        """Import all files linked and add them to the original file.
        Updates self.fileblock.file_data in auto mode.
        Returns the file_data in manual mode. You can optionally skip
        build_links and directly use the fetch_base method.
        """
        if self.mode == 'auto':
            self.fileblock.file_data = self.fetch_base(
                file_data=self.fileblock.file_data,
            )
        if self.mode == 'manual':
            return self.fetch_base(
                file_data=self.fileblock.file_data
            )

    def fetch_base(self, **kwargs):
        """Takes in file_data and recursively searches all links for
        matches. Populates the matches.

        kwarg key-value pairs:
        file_data=file_data: str

        Returns fully populated file_data.
        """
        links_found = re.findall(self.regex.link, kwargs['file_data'])
        if links_found:
            for link in links_found:
                local_file_object = file_object(link,
                                                template_files[link],
                                                'manual')
                local_file_data = local_file_object.stitch_file()
                local_file_object.fileblock = local_file_object.store_blocks(
                    local_file_data
                )
                # Override default fileblock.file_data
                local_file_object.fileblock.file_data = local_file_data
                ###
                returned_file_data = local_file_object.fetch_base(
                    file_data=local_file_object.fileblock.file_data
                )
                sub_link = self.regex.link_gen(link)
                self.fileblock.file_data = re.sub(
                    sub_link,
                    returned_file_data,
                    self.fileblock.file_data
                )
            return self.fileblock.file_data
        else:
            return kwargs['file_data']

    def build_blocks(self, **kwargs):
        """Takes in a FileBlock object.
        Searches for blocks in the fileblock object.
        Replaces blocks with intended values defined in the
        file that inherits.

        kwarg key-value pairs:
        file_data=file_data: str

        Returns the fileblock object in manual mode.
        """
        if self.mode == 'manual':
            assert isinstance(kwargs['fileblock'], FileBlock)
            self.fileblock = kwargs['fileblock']

        blocks_found = re.findall(self.regex.block,
                                  self.fileblock.file_data)
        for block in blocks_found:
            sub_block = self.regex.block_gen(block[0])
            for stored_block in self.fileblock.blocks:
                if stored_block[0] == block[0]:
                    self.fileblock.file_data = re.sub(
                        sub_block,
                        stored_block[1],
                        self.fileblock.file_data
                    )
        if self.mode == 'manual':
            fileblock = self.fileblock
            delattr(self, "fileblock")
            return fileblock


def environment(pwd: object):
    """Takes in a path of base directory.
    Checks whether all the files exist.
    """
    if not os.path.exists(pwd/config['template_folder']):
        raise FileNotFoundError()


def scan_template_folder() -> dict:
    """Scan through all files and sub-dirs in the template
    folder.
    Returns dictionary of all files.
    """
    template_folder_content = {}
    for root, dirs, files in os.walk(config['template_folder']):
        for file in files:
            if template_folder_content.get(file):
                raise RuntimeError(f'The file "{file}" already exists at {os.path.join(root, file)}.')
            template_folder_content[
                file
            ] = os.path.join(root, file)
    return template_folder_content


def main():
    global template_files
    template_files = scan_template_folder()
    build_files = []
    for file_name in template_files:
        build_files.append(file_object(file_name,
                                       template_files[file_name])
                           )
    return build_files
