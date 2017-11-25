___VERSION___ = 1.0

from log import Log

import json

from description_config import DescriptionConfig

___LETTERS___ = ["a","A","b","B","c","C","d","D","e","E","f","F","g","G","h","H","i","I","j","J","l","L","m","M","n","N","o","O","p","P","q","Q","r","R",
					"s","S","t","T","u","U","v","V","w","W","x","X","y","Y","z","Z"]

class DataProcessor(object):
	def __init__(self):
		pass

	@Log()
	def form_message(self, parsed_data):
		cl = "class " + parsed_data["Class"]["Name"] + "(object):\n" 
		init = "	def __init__(self):\n"
		
		## Initialization
		if parsed_data["Class"]["Initialization"] != [{}]:
			for i in range(len(parsed_data["Class"]["Initialization"]["Attributes"])):
				init += "		self._"
				val = parsed_data["Class"]["Initialization"]["Values"][i]
				if type(val) is int or type (val) is float:
					val = str(val)
				else:
					val = "\"" + str(val) + "\""
				init += parsed_data["Class"]["Initialization"]["Attributes"][i] + " = " + val
				init += "\n"
			init += "\n"
		else: 
			if parsed_data["Class"]["Attributes"] != []:
				for i in range(len(parsed_data["Class"]["Attributes"])):
					init += "		self._"
					init += parsed_data["Class"]["Attributes"][i] + " = None\n"
		if init == "	def __init__(self):\n":
			init += "		pass\n\n"
		else:
			init += "\n"
		
		## Methods
		methods = []
		if parsed_data["Class"]["Methods"] != [{}]:
			for meth in parsed_data["Class"]["Methods"]:
				method_msg = "	def " + meth["Method"] + "(self"
				if meth["Attributes"] != []:
					for i in range(len(meth["Attributes"])):
						method_msg += ", " + meth["Attributes"][i]
					method_msg += "):"
				else:
					method_msg += "):"
				method_msg += "\n		pass\n\n"
				methods.append({"Method" : method_msg})

		## Getters and setters
		if parsed_data["Class"]["Attributes"] != []:
			for i in range(len(parsed_data["Class"]["Attributes"])):
				methods.append({"Method" : "	def set_" + parsed_data["Class"]["Attributes"][i] +
					"(self, " + parsed_data["Class"]["Attributes"][i] + "):\n		" + 
					"self._"+parsed_data["Class"]["Attributes"][i] + " = " + parsed_data["Class"]["Attributes"][i] + "\n\n"})
				methods.append({"Method" : "	def get_" + parsed_data["Class"]["Attributes"][i] + "(self):\n		" + 
					"return " + "self._"+parsed_data["Class"]["Attributes"][i] + "\n\n"})


		message = {"Class" : cl, "Init" : init, "Methods" : methods}
		return json.dumps(message).encode('utf-8')



	@Log()
	def parse_client_message(self, client_message):
		data = json.loads(client_message)
		description_text = data["Description text"]
		description_config = data["Description config"]
		return description_text, description_config

	@Log()
	def make_lines(self, string):
		strings=[]
		line = ""
		for ch in string:
			if ch != "\n":
				line += ch
			else:
				strings.append(line)
				line = ""
		return strings


	@Log()
	def clean_strings(self, description_text):
		string = description_text
		strings=[]
		good_strings=[]
		line=""
		flag=0
		for ch in string:
			if ch in ___LETTERS___ or ch == "*":
				flag = 1
			if ch != "\n" and flag == 1:
				if ch not in ["?", "!", ".", "-","'","\"",":"]:
					line += ch
			else:
				strings.append(line)
				line = ""
				flag=0
		strings.append(line)
		for line in strings:
			if (line[0:2] != "**") and (line != ""):
				good_strings.append(line)
		result_string = ""
		for line in good_strings:
			result_string += line + "\n"
		return result_string

	@Log()
	def check_attr(self, attr, attributes, line):
		result = 1
		for a in attributes:
			if a in line:
				if (attr != a) and (attr in a):
					result = 0
		return result
		
	@Log()
	def parse_methods(self, line, attributes, description_config):
		result = [{}]
		attribute_keywords = description_config.get_attribute_keywords()
		method_keywords = description_config.get_method_keywords()
		initialization_keywords = description_config.get_initialization_keywords()
		is_method_line = 1
		for keyword in attribute_keywords:
			if keyword in line:
				is_method_line = 0
		for keyword in initialization_keywords["Attribute keywords"]:
			if keyword in line:
				is_method_line = 0
		if is_method_line == 1:
			for keyword in method_keywords:
				if keyword in line:
					split = line.split(keyword)
					if len(split) == 1: 
						method_line = split
					else:
						method_line = split[1]
					if ", " in method_line:
						method_lines = method_line.split(", ")
						for subline in method_lines:
							if " and " in subline:
								for a in subline.split(" and "):
									meth_attr = []
									for attr in attributes:
										if attr in a:
											if self.check_attr(attr, attributes, a) == 1:
												meth_attr.append(attr)
									if meth_attr != []:
										result.append({"Method" : a, "Attributes" : meth_attr})
									else:
										result.append({"Method" : a, "Attributes" : []})
							else:
								meth_attr = []
								for attr in attributes:
									if attr in subline:
										if self.check_attr(attr, attributes, subline) == 1:
											meth_attr.append(attr)
								if meth_attr != []:
									result.append({"Method" : subline, "Attributes" : meth_attr})
								else:
									result.append({"Method" : subline, "Attributes" : []})
					else:
						if " and " in method_line:
							for subline in method_line.split(" and "):
								meth_attr = []
								for attr in attributes:
									if attr in subline:
										if self.check_attr(attr, attributes, subline) == 1:
											meth_attr.append(attr)
								if meth_attr != []:
									result.append({"Method" : subline, "Attributes" : meth_attr})
								else:
									result.append({"Method" : subline, "Attributes" : []})
						else:
							meth_attr = []
							for attr in attributes:
								if attr in method_line:
									if self.check_attr(attr, attributes, method_line) == 1:
										meth_attr.append(attr)
							if meth_attr != []:
								result.append({"Method" : method_line, "Attributes" : meth_attr})
							else:
								result.append({"Method" : method_line, "Attributes" : []})
		if result != [{}]:
			result.remove({})
		return result

	@Log()
	def make_val(self,value):
		val=""
		try:
			val = float(value)
			if val == int(val):
				val = int(val)
		except Exception:
			pass
		if val == "":
			val = value
		return val

	@Log()
	def parse_initialization(self, line, attributes, description_config):
		result = [{}]
		init_attr = []
		init_vals = [] 
		attribute_keywords = description_config.get_attribute_keywords()
		method_keywords = description_config.get_method_keywords()
		initialization_keywords = description_config.get_initialization_keywords()
		is_initialization_line = 1
		for keyword in attribute_keywords:
			if keyword in line:
				is_initialization_line = 0
		for keyword in method_keywords:
			if keyword in line:
				is_initialization_line = 0
		if is_initialization_line == 1:
			for keyword in initialization_keywords["Attribute keywords"]:
				if keyword in line:
					split = line.split(keyword)
					if len(split) == 1:
						initialization_line = split
					else:
						initialization_line = split[1]
					if ", " in initialization_line:
						attributes_line = initialization_line.split(", ")
						for subline in attributes_line:
							if " and " in subline:
								for a in subline:
									for kw in initialization_keywords["Attribute values keywords"]:
										if kw in a:
											at_val = a.split(kw)
											if len(at_val) > 1:
												init_attr.append(at_val[0])
												init_vals.append(self.make_val(at_val[1]))
							else:
								for kw in initialization_keywords["Attribute values keywords"]:
									if kw in subline:
										at_val = subline.split(kw)
										if len(at_val) > 1:
											init_attr.append(at_val[0])
											init_vals.append(self.make_val(at_val[1]))
					else:
						if " and " in initialization_line:
							attributes_line = initialization_line.split(" and ")
							for subline in attributes_line:
								for kw in initialization_keywords["Attribute values keywords"]:
									if kw in subline:
										at_val = subline.split(kw)
										if len(at_val) > 1:
											init_attr.append(at_val[0])
											init_vals.append(self.make_val(at_val[1]))
						else:
							for kw in initialization_keywords["Attribute values keywords"]:
									if kw in initialization_line:
										at_val = initialization_line.split(kw)
										if len(at_val) > 1:
											init_attr.append(at_val[0])
											init_vals.append(self.make_val(at_val[1]))
					result = init_attr, init_vals
		return result

	@Log()
	def parse_attributes(self, line, description_config):
		result = []
		attributes_line = ""
		attribute_keywords = description_config.get_attribute_keywords()
		method_keywords = description_config.get_method_keywords()
		initialization_keywords = description_config.get_initialization_keywords()
		is_attribute_line = 1
		for keyword in method_keywords:
			if keyword in line:
				is_attribute_line = 0
		for keyword in initialization_keywords["Attribute keywords"]:
			if keyword in line:
				is_attribute_line = 0
		if is_attribute_line == 1:
			for keyword in attribute_keywords:
				if keyword in line:
					split = line.split(keyword)
					if len(split) == 1: 
						attributes_line = split
					else:
						attributes_line = split[1]
			if attributes_line != "":
				if ", " in attributes_line:
					attributes_lines = attributes_line.split(", ")
					for subline in attributes_lines:
						if " and " in subline:
							for a in subline.split(" and "):
								result.append(a)
						else:
							result.append(subline)
				else:
					if " and " in attributes_line:
						for subline in attributes_line.split(" and "):
							result.append(subline)
					else:
						result.append(attributes_line)
		return result

	@Log()
	def make_name(self, line):
		name = ""
		if " " in line:
			for word in line.split(" "):
				if name == "":
					name = word
				else:
					name = name + "_" + word
		else:
			name = line
		return name

	@Log()
	def parse_class(self, line):
		return line.split(" ", 1)[0]


	@Log()
	def make_parsed_data(self, client_message):
		description_text, description_config = self.parse_client_message(client_message)
		description_config = DescriptionConfig(description_config)
		clean_description_text = self.clean_strings(description_text)
		lines = self.make_lines(clean_description_text)
		class_name = self.parse_class(lines[0])
		attributes = []
		methods = [{}]
		initialization = [{}]
		for line in lines:
			atr = self.parse_attributes(line, description_config)
			if atr != []:
				for a in atr:
					attributes.append(a)
		renamed_attributes = []
		if attributes != []:
			for name in attributes:
				renamed_attributes.append(self.make_name(name))

		for line in lines:
			meth = self.parse_methods(line, attributes, description_config)
			if meth != [{}]:
				for m in meth:
					m["Method"] = self.make_name(m["Method"])
					ren_atr=[]
					for a in m["Attributes"]:
						ren_atr.append(self.make_name(a))
					m["Attributes"] = ren_atr
					methods.append(m)
		if methods != {}:
			methods.remove({})
		attr = []
		vals = []
		for line in lines:
			init = self.parse_initialization(line, attributes, description_config)
			if init != [{}]:
				at, vl = init
				for a in at:
					attr.append(self.make_name(a))
				for v in vl:
					vals.append(v)
		if attr != [] and vals != []:
			initialization = {"Attributes" : attr, "Values" : vals}
		parsed_data = {"Class" : {"Name" : class_name, "Initialization" : initialization, "Methods" : methods, "Attributes" : renamed_attributes}}
		return parsed_data