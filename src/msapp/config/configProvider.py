import logging
import simplejson as json
import os.path
from functools import lru_cache


class ConfigProvider:
    _MAIN_CONFIG_FILE = '/config/config.json'
    _l = logging.getLogger(__name__)

    def __init__(self):
        self._config = self._loadConfig(ConfigProvider._MAIN_CONFIG_FILE)

    @staticmethod
    @lru_cache(maxsize=None)
    def _loadConfig(configFile: str) -> [dict, list]:
        data = {}
        try:
            fp = open(configFile, 'r', encoding='utf-8')
            data = json.load(fp)
            fp.close()
        except Exception:
            ConfigProvider._l.error(f"Failed to load config data from '{configFile}'")
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
        ConfigProvider._l.debug(f"Config loaded: {data}")
        return data

    def getConfig(self, context: str = None):
        if context is None:
            return self._config
        if context in self._config:
            return self._config[context]
        return None
