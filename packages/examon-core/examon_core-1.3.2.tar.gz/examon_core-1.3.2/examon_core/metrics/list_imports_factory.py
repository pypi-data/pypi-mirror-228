import ast


class ListImportsFactory:
    @staticmethod
    def build(code):
        modules = set()

        def visit_import(node):
            for name in node.names:
                modules.add(name.name.split(".")[0])

        def visit_import_from(node):
            if node.module is not None and node.level == 0:
                modules.add(node.module.split(".")[0])

        node_iter = ast.NodeVisitor()
        node_iter.visit_Import = visit_import
        node_iter.visit_ImportFrom = visit_import_from

        node_iter.visit(ast.parse(code))
        return list(modules)
