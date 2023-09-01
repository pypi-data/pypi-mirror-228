import ast
import ConfigParser as configparser


class Visitor(ast.NodeVisitor):
    def __init__(self, options):
        self.errors = []
        self.forbidden_modules = options["forbidden_modules"]

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in self.forbidden_modules:
                self.errors.append((node.lineno, node.col_offset))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module in self.forbidden_modules:
            self.errors.append((node.lineno, node.col_offset))
        elif node.module.split(".")[0] in self.forbidden_modules:
            self.errors.append((node.lineno, node.col_offset))

        self.generic_visit(node)


class OptionManager(object):
    def __init__(self):
        self.config = self.load_config(".flake8")

    def load_config(self, config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path)

        config_values = {}
        if config.has_section(__name__):
            if config.has_option(__name__, "forbidden_modules"):
                config_values["forbidden_modules"] = config.get(
                    __name__, "forbidden_modules"
                )

        return config_values


class Plugin:
    name = __name__
    version = "0.1.0"

    def __init__(self, tree):
        self._tree = tree
        self.options = OptionManager().config

    def run(self):
        visitor = Visitor(self.options)
        visitor.visit(self._tree)

        for line, col in visitor.errors:
            yield line, col, 'IMP100 forbiden import', type(self)
