import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
from logger_local.MessageSeverity import MessageSeverity
sys.path.append(os.getcwd())
from python_sdk_local.sdk.src.LoggerOutputEnum import LoggerOutputEnum

PYTHON_SDK_LOCAL_COMPONENT_ID = 202
PYTHON_SDK_LOCAL_COMPONENT_NAME = 'python_sdk_local/src/debug_mode.py'
LOGGER_CONFIGURATION_JSON = '.logger.json'
LOGGER_MINIMUM_SEVERITY = os.getenv('LOGGER_MINIMUM_SEVERITY')    


obj = {
    'component_id': PYTHON_SDK_LOCAL_COMPONENT_ID,
    'component_name': PYTHON_SDK_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=obj)
class DebugMode:
    def __init__(self):
        self.logger_json = {}
        self.debug_everything = False
        self._init()

    def _init(self):
        INIT_METHOD_NAME = "_init()"
        logger.start(INIT_METHOD_NAME)

        global LOGGER_MINIMUM_SEVERITY
        if not LOGGER_MINIMUM_SEVERITY:
            LOGGER_MINIMUM_SEVERITY = 0
        else:
            if hasattr(MessageSeverity, LOGGER_MINIMUM_SEVERITY):
                LOGGER_MINIMUM_SEVERITY = MessageSeverity[LOGGER_MINIMUM_SEVERITY].value
            elif LOGGER_MINIMUM_SEVERITY.isdigit():
                LOGGER_MINIMUM_SEVERITY = int(LOGGER_MINIMUM_SEVERITY)
            else:
                raise Exception("LOGGER_MINIMUM_SEVERITY must be a valid LoggerOutputEnum or a number or None")

        try:
            with open(LOGGER_CONFIGURATION_JSON, 'r') as file:
                self.logger_json = json.load(file)
        except FileNotFoundError:
            self.debug_everything = True
            logger.info("could not find .logger.json file, debugging everything")
        except Exception as exception:
            logger.exception("encounteredthe following error", object={'exception': exception})
            logger.end(INIT_METHOD_NAME)
            raise
        logger.end(INIT_METHOD_NAME)

    def is_logger_output(self, component_id:str, logger_output: LoggerOutputEnum, severity_level:int)->bool:
        IS_LOGGER_OUTPUT_METHOD_NAME = "is_logger_output()"
        logger.start(IS_LOGGER_OUTPUT_METHOD_NAME, object={'component_id': component_id, 'logger_output': str(logger_output), 'severity_level': severity_level})


        #Debug everything that has a severity level higher than the minimum required
        if self.debug_everything:
            result = severity_level >= LOGGER_MINIMUM_SEVERITY
            logger.end(IS_LOGGER_OUTPUT_METHOD_NAME, object={'result': result})
            return result
        
        severity_level = max(severity_level, LOGGER_MINIMUM_SEVERITY)
        if component_id in self.logger_json:
            output_info = self.logger_json[component_id]
            if logger_output in output_info:
                result = severity_level >= output_info[logger_output]
                logger.end(IS_LOGGER_OUTPUT_METHOD_NAME, object={'result': result})
                return result

        # In case the component do not exist in the logger configuration file or the 
        # logger_output was not specif
        result = True
        logger.end(IS_LOGGER_OUTPUT_METHOD_NAME, object={'result': result})
        return result