import json

class Config(object):
	def __init__(self, path = "Config.json"):
		Config_file = open(path, "r")
		Config_json = json.loads(Config_file.read())
		Config_file.close()
		self.NAs = Config_json["NAs"]
		self.NaNs = Config_json["NaNs"]
		self.DateFormats = Config_json["DateFormats"]
		self.CsvSeparators = Config_json["CsvSeparators"]
		self.NumberSeparators = Config_json["NumberSeparators"]
	
	def get_NAs(self):
		return self.NAs

	def get_NaNs(self):
		return self.NaNs

	def get_DateFormats(self):
		return self.DateFormats

	def get_CsvSeparators(self):
		return self.CsvSeparators

	def get_NumberSeparators(self):
		return self.NumberSeparators
