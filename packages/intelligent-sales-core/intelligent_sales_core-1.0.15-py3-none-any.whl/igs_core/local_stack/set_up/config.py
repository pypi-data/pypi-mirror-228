import os
from pathlib import Path

PROJECT_NAME = "intelligentsales"
ENVIRONMENT_TAG = "lokoelstack"

_CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
TESTS_PATH = Path(_CURRENT_FOLDER).absolute().parent.parent


UNIT_TESTS_PATH = f"{TESTS_PATH}/unit"
TESTS_FIXTURES_PATH = f"{TESTS_PATH}/fixtures"
OUTPUTS_PATH = f"{TESTS_PATH}/outputs"
TESTS_FIXTURES_RAW_PATH = f'{TESTS_FIXTURES_PATH}/raw_data'
INTEGRATION_TESTS_PATH = f"{TESTS_PATH}/integration"

# TODO: Refactor config  system entirely, please
