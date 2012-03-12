import models
import sys, inspect

models_registry = dict()

class ModelNotRegisteredError(TypeError):
	pass

def register_models(*model_classes):
	for model_class in model_classes:
		models_registry[model_class.__class__.__name__] = model_class

def register_models_from_module(module_name):
	predicate = lambda obj: inspect.isclass(obj) and issubclass(obj, models.ModelBase)
	for name, cls in inspect.getmembers(sys.modules[module_name], predicate):
		models_registry[name] = cls

def get_model(name):
	if name not in models_registry:
		raise ModelNotRegisteredError(name)
	return models_registry[name]