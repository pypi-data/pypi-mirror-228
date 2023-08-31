import re


class regex_expressions:
    """Implements all regex lookups and generator functions"""
    def __init__(self):
        self.content_reg = r'(\S*)'  # initial setup
        self.replace_reg = r'\(\\S\*\)'  # for regex loopkups
        self.link = rf'<!--\${self.content_reg}-->'
        # self.extend = rf'<!--@{self.content_reg}-->'
        self.constant = rf'<!--#{self.content_reg}-->'
        self.block = rf'<!--%(?!endblock){self.content_reg}-->((.|\n)*?)<!--%endblock-->'

    def link_gen(self, value):
        return re.sub(self.replace_reg, value, self.link)

    def constant_gen(self, value):
        return re.sub(self.replace_reg, value, self.constant)

    # def extend_gen(self, value):
    #     return re.sub(self.replace_reg, value, self.extend)

    def block_gen(self, value):
        return re.sub(self.replace_reg, value, self.block)
