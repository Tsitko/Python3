import re
import Config
import numpy as np
from datetime import datetime

def rem(string,i):
	l = len(string)
	return str(string[0:i]+string[i+1:l])


def Matching(pattern, string, Match = "Date"):
	if Match == "Date":
		if re.fullmatch(pattern, string[0:10]) is not None:
			return True
		else: return False
	if Match == "Number":
		if re.fullmatch(pattern, string) is not None:
			return True
		else: return False

def make_pattern(DateFormat):
	DateFormat = DateFormat[0:8]
	pattern = DateFormat.replace("%d", "([1-9]||[0-3][0-9])")
	pattern = pattern.replace("%m", "([1-9]||[0][1-9]||[1][0-2])")
	pattern = pattern.replace("%y", "[0-9][0-9]")
	pattern = pattern.replace("%Y", "[0-9][0-9][0-9][0-9]")
	return pattern

class Column(object):

	def __init__(self, Col, Conf):
		self.DataType = None
		self.DateFormat = list()
		self.Col = Col
		self.Conf = Conf
		self.NA = self.NAs()

	def get_col(self):
		return self.Col

	def NAs(self):
		NAs = [0]*len(self.Col)
		for NaFormat in self.Conf.get_NAs():
			for i in range(0,len(self.Col)):
				if self.Col[i] == NaFormat:
					NAs[i] = 1
					self.Col[i] = "NA"
		return NAs


	def isDate(self):
		for i in range(0,len(self.NA)):
			if self.NA[i] != 1:
				break
		checking_date = str(self.Col[i])
		if len(checking_date) <=9:
			return False
		for DateFormat in self.Conf.get_DateFormats():
			pattern = make_pattern(DateFormat)
			if Matching(pattern, checking_date):
				self.DataType = "Date"
				self.DateFormat.append(DateFormat)
		if self.DataType == "Date" and len(self.DateFormat) > 1:
			return True
		else: 
			return False

	def choose_dateFormat(self):
		sum_Dates = [0]*len(self.DateFormat)
		i=0
		for DateFormat in self.DateFormat:
			pattern = make_pattern(DateFormat)
			count = 0
			for el in self.Col:
				if Matching(pattern, el):
					count += 1
			sum_Dates[i] = count
			i += 1
		index_max = np.argmax(sum_Dates)
		return self.DateFormat[index_max]

	def format_date(self):
		format_full = self.choose_dateFormat()
		for i in range(0,len(self.Col)):
			try:
				date = datetime.strptime(self.Col[i], format_full)
				self.Col[i] = str(date)
			except:
				try:
					date = datetime.strptime(self.Col[i], format_full[0:8])
					self.Col[i] = str(date)
				except: self.Col[i] = "NA"

	def isNumber(self):
		pattern = str()
		for delimiter in self.Conf.get_NumberSeparators():
			if len(pattern) != 0:
				pattern += "||"
			pattern += str("(([0-9]+"+delimiter+"* *)*[0-9]+)")
		count = 0
		for i in range(0,len(self.NA)):
			if self.NA[i]==0:
				if Matching(pattern, str(self.Col[i]), Match = "Number"):
					count +=1
		if count == len(self.NA) - sum(self.NA):
			return True
		else:
			return False

	def format_number(self):
		for i in range(0, len(self.Col)):
			if self.NA[i] == 0:
				num = str(self.Col[i])
				for delim in self.Conf.get_NumberSeparators():
					num = num.replace(delim, ".")
				num = num.replace(' ', '')
				delimFound = 0
				for j in range((len(num)-1),-1,-1):
					if num[j] == '.':
						if delimFound == 0:
							delimFound = 1
						else:
							num = rem(num,j)
				self.Col[i] = num
