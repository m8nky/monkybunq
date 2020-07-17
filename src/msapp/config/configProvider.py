import logging
import simplejson as json
import os.path
from functools import lru_cache


logging.basicConfig(level=logging.DEBUG)
class ConfigProvider:
    _MAIN_CONFIG_FILE = '/config/config.json'
    _EXTRA_CONFIG = {}

    def __init__(self):
        self._l = logging.getLogger(__name__)
        self._config = self._loadConfig(ConfigProvider._MAIN_CONFIG_FILE)

    @staticmethod
    @lru_cache(maxsize=None)
    def _loadConfig(configFile: str) -> [dict, list]:
        _l = logging.getLogger(__name__)
        data = {}
        try:
            fp = open(configFile, 'r', encoding='utf-8')
            data = json.load(fp)
            fp.close()
        except Exception:
            _l.error(f"Failed to load config data from '{configFile}'")
        # Replace nested config
        def _injectNestedConfig(obj: dict):
            if 'configProvider' in obj:
                assert type(obj['configProvider']) is str and os.path.isfile(obj['configProvider']), f"'configProvider' must be a filename."
                nestedData = ConfigProvider._loadConfig(obj['configProvider'])
                if type(nestedData) is dict:
                    obj.update(nestedData)
                else:
                    obj['config'] = nestedData
                del obj['configProvider']
            for k, v in obj.items():
                if isinstance(v, dict):
                    _injectNestedConfig(v)
        if type(data) is dict:
            _injectNestedConfig(data)
        _l.debug(f"Config loaded: {data}")
        return data

    def getConfig(self, context: str):
        if context in ConfigProvider._EXTRA_CONFIG:
            return ConfigProvider._EXTRA_CONFIG[context]
        if context in self._config:
            return self._config[context]
        return None

    @staticmethod
    def injectExtraConfig(key: str, value):
        ConfigProvider._EXTRA_CONFIG[key] = value
