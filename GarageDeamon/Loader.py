'''

Module that allows to load all the actors and sensors

:author: Stefan-Gabriel CHITIC
'''

import os
from GarageDeamon.Common import SensorBase, ActorBase


class MainLoader(object):

    def __init__(self, base='GarageDeamon.Sensors', base_class=SensorBase):
        self.base = base
        self.baseClass = base_class
        self.pluginNames = None
        self.plugins = {}
        self.reload_plugins()

    def get_plugin_names(self):
        return self.pluginNames

    def get_modules(self):
        return self.plugins

    def get_module(self, name):
        if not self.plugins.get(name, None):
            raise ImportError('No module %s loaded' % name)
        return self.plugins[name]

    def reload_plugins(self):
        self.pluginNames = self._get_plugins()
        self.plugins.clear()
        for module in self.pluginNames:
            mod_name = '%s.%s' % (self.base, module)
            module_tmp = __import__(mod_name, globals(), locals(), [module])
            cls = MainLoader.get_subclass(module_tmp, self.baseClass)
            self.plugins[module] = cls()

    @staticmethod
    def get_subclass(module, base_class):
        good_results = []
        for name in dir(module):
            obj = getattr(module, name)
            if name == base_class.__name__:
                continue
            try:
                if issubclass(obj, base_class):
                    print name
                    good_results.append(obj)
            except TypeError:  # If 'obj' is not a class
                pass
        if good_results:
            return good_results[-1]
        return None

    @staticmethod
    def convert_to_module_name(name):
        return name.replace('.py', '')

    def _get_plugins(self):
        full_path = os.path.abspath(__file__).split('/')[:-2]
        full_path = '/'.join(full_path)
        full_path = "%s/%s/" % (full_path, self.base.replace('.', '/'))
        modules = []
        for _, _, modules_tmp in os.walk(full_path):
            for module in modules_tmp:
                if not module.endswith('.py'):
                    continue
                if module != '__init__.py' and 'Test' not in module:
                    modules.append(MainLoader.convert_to_module_name(module))
        return modules


SensorLoader = MainLoader()
ActorLoader = MainLoader(base='GarageDeamon.Actors', base_class=ActorBase)
