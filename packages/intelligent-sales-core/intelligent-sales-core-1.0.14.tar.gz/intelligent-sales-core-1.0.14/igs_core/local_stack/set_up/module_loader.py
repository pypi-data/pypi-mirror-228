import importlib
import os
import sys


def load_module_from_non_standard_filename(module_name, file_path):
    sys.path.insert(0, os.path.dirname(os.path.abspath(file_path)))
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
