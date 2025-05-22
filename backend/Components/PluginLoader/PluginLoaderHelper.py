import importlib.util
import os
import traceback
from types import ModuleType
from typing import Any, Optional, Callable, Dict

PLUGIN_DIR = "plugins"
os.makedirs(PLUGIN_DIR, exist_ok=True)

_loaded_plugins: Dict[str, ModuleType] = {}

def load_plugin(plugin_name: str) -> Optional[ModuleType]:
    plugin_path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")
    if not os.path.isfile(plugin_path):
        return None

    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            _loaded_plugins[plugin_name] = module
            return module
        except Exception as e:
            print(f"Failed to load plugin '{plugin_name}': {e}\n{traceback.format_exc()}")
    return None

def list_plugins() -> list:
    return [f[:-3] for f in os.listdir(PLUGIN_DIR) if f.endswith(".py")]

def is_plugin_loaded(plugin_name: str) -> bool:
    return plugin_name in _loaded_plugins

def get_loaded_plugins() -> list:
    return list(_loaded_plugins.keys())

def unload_plugin(plugin_name: str) -> bool:
    if plugin_name in _loaded_plugins:
        del _loaded_plugins[plugin_name]
        return True
    return False

def execute_plugin_function(plugin_name: str, function_name: str, *args, **kwargs) -> Any:
    plugin = _loaded_plugins.get(plugin_name)
    if plugin and hasattr(plugin, function_name):
        func: Callable = getattr(plugin, function_name)
        if callable(func):
            return func(*args, **kwargs)
    raise ValueError(f"Function '{function_name}' not found in plugin '{plugin_name}'")