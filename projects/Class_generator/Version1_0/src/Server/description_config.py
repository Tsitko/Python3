import json

___CONFIGPATH___ = "description_config.json"

class DescriptionConfig(object):
	def __init__(self, data):
		self._attribute_keywords = data["Attribute keywords"]
		self._method_keywords = data["Method keywords"]
		self._initialization_keywords = data["Initialization keywords"]

	def set_attribute_keywords(self,keywords):
		self._attribute_keywords = keywords

	def set_method_keywords(self,keywords):
		self._method_keywords = keywords

	def set_initialization_keywords(self,keywords):
		self._initialization_keywords = keywords

	def get_attribute_keywords(self):
		return self._attribute_keywords

	def get_method_keywords(self):
		return self._method_keywords

	def get_initialization_keywords(self):
		return self._initialization_keywords
