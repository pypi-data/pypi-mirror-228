import json
from dotenv import load_dotenv
load_dotenv()
import os
import sys
sys.path.append(os.getcwd())

import python_sdk_local.sdk.src.debug_mode as debug_mode 
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger


PYTHON_SDK_LOCAL_COMPONENT_ID = 184
PYTHON_SDK_LOCAL_COMPONENT_NAME = 'python_sdk_local/tests/debug_mode_test.py'

obj = {
    'component_id': PYTHON_SDK_LOCAL_COMPONENT_ID,
    'component_name': PYTHON_SDK_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=obj)

with open('python_sdk_local/.logger.json.example1', 'r') as file:
    EXAMPLE_DATA_1 = json.load(file)

with open('python_sdk_local/.logger.json.example2', 'r') as file:
    EXAMPLE_DATA_2 = json.load(file)

def add_debug_file(data):

    ADD_DEBUG_FILE_FUNCTION_NAME = 'add_debug_file()'
    logger.start(ADD_DEBUG_FILE_FUNCTION_NAME)

    with open(debug_mode.LOGGER_CONFIGURATION_JSON, 'w') as file:
        json.dump(data, file)

    logger.end(ADD_DEBUG_FILE_FUNCTION_NAME)


def remove_debug_file():
    REMOVE_DEBUG_FILE_FUNCTION_NAME = 'remove_debug_file()'
    logger.start(REMOVE_DEBUG_FILE_FUNCTION_NAME)

    os.remove(debug_mode.LOGGER_CONFIGURATION_JSON)

    logger.end(REMOVE_DEBUG_FILE_FUNCTION_NAME)


def test_debug_mode_init():

    #set env variable
    TEST_DEBUG_MODE_INIT_FUNCTION_NAME = 'test_debug_mode_init()'
    logger.start(TEST_DEBUG_MODE_INIT_FUNCTION_NAME)

    add_debug_file(EXAMPLE_DATA_1)

    debug = debug_mode.DebugMode()

    remove_debug_file()

    result = debug.debug_json == EXAMPLE_DATA_1
    logger.end(TEST_DEBUG_MODE_INIT_FUNCTION_NAME, object={'result': result})

    assert result


def test_fetch_debug_info_1():

    TEST_FETCH_DEBUG_INFO_1_FUNCTION_NAME = 'test_fetch_debug_info_1()'
    logger.start(TEST_FETCH_DEBUG_INFO_1_FUNCTION_NAME)

    add_debug_file(EXAMPLE_DATA_1)

    debug = debug_mode.DebugMode()

    remove_debug_file()

    result = debug.fetch('1', 'console', 501) == True
    logger.end(TEST_FETCH_DEBUG_INFO_1_FUNCTION_NAME,
               object={'result': result})

    assert result


def test_fetch_debug_mode_2():

    TEST_FETCH_DEBUG_MODE_2_FUNCTION_NAME = 'test_fetch_debug_mode_2()'
    logger.start(TEST_FETCH_DEBUG_MODE_2_FUNCTION_NAME)

    add_debug_file(EXAMPLE_DATA_2)

    debug = debug_mode.DebugMode()

    remove_debug_file()

    result1 = debug.fetch('2', 'logzio', 502) == True
    result2 = debug.fetch('2', 'MySQL', 503) == True
    result3 = debug.fetch('2', 'console', 499) == False
    result4 = debug.fetch('2', 'console', 501) == True
  
    result = result1 and result2 and result3
    logger.end(TEST_FETCH_DEBUG_MODE_2_FUNCTION_NAME,
               object={'result': result})
    assert result

def test_minimum_sevirity():
    
    TEST_MINIMUM_SEVIRITY_FUNCTION_NAME = 'test_minimum_sevirity()'
    logger.start(TEST_MINIMUM_SEVIRITY_FUNCTION_NAME)

    add_debug_file(EXAMPLE_DATA_2)

    debug = debug_mode.DebugMode()
    print(debug.debug_json)

    remove_debug_file()

    debug_mode.LOGGER_MINIMUM_SEVERITY = 501
    result1 = debug.fetch('2', 'logzio', 502) == True

    debug_mode.LOGGER_MINIMUM_SEVERITY = 503
    result2 = debug.fetch('2', 'logzio', 502) == False

    debug_mode.LOGGER_MINIMUM_SEVERITY = 0

    result = result1 and result2
    logger.end(TEST_MINIMUM_SEVIRITY_FUNCTION_NAME, object={'result': result})
    assert result
    


