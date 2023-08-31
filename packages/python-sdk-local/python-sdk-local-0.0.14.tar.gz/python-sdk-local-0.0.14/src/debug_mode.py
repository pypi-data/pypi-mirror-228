import json
from dotenv import load_dotenv
load_dotenv()
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger


PYTHON_SDK_LOCAL_COMPONENT_ID = 184
PYTHON_SDK_LOCAL_COMPONENT_NAME = 'python_sdk_local/src/debug_mode.py'

obj = {
    'component_id': PYTHON_SDK_LOCAL_COMPONENT_ID,
    'component_name': PYTHON_SDK_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=obj)
class DebugMode:
    def __init__(self):
        self.debug_json = {}
        self._init()

    def _init(self):
        _INIT = "_init()"
        logger.start(_INIT)

        try:
            with open('debug.json', 'r') as file:
                self.debug_json = json.load(file)
        except Exception as e:
            logger.exception("got exception while reading json from file", object={'exception': e})
            logger.end(_INIT)
            return

        logger.end(_INIT)

    def fetch(self, component_id:str, output_id:str, minimum_severity_level:int):

        FETCH_FUNCTION_NAME = "fetch()"
        logger.start(FETCH_FUNCTION_NAME, object={'component_id': component_id, 'output_id': output_id, 'minimum_severity_level': minimum_severity_level})

        if component_id in self.debug_json:
            output_info = self.debug_json[component_id]
            if output_id in output_info:
                result = minimum_severity_level >= output_info[output_id]
                logger.end(FETCH_FUNCTION_NAME, object={'result': result})
                return result
        

        result = False
        logger.end(FETCH_FUNCTION_NAME, object={'result': result})
        return result