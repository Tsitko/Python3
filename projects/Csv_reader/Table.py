import Config
import Column
import pandas as pd
pd.options.mode.chained_assignment = None

class Table(object):
	def __init__(self, path):
		Conf = Config.Config()
		self.Separators = Conf.get_CsvSeparators()
		self.path = path
		self.Table = self.read_Table()
		self.col_names = self.Table.columns
		self.errors = list()
		self.Conf = Conf
		self.DataReady = False

	def check_rows(self, Table):
		counter = 0
		for row in Table:
			counter += 1
			if counter > 1 : return True
		return False

	def read_Table(self):
		Table = None
		for Sep in self.Separators:
			try:
				with open(self.path) as CsvFile:
					Table = pd.read_csv(CsvFile, sep = Sep)
					if self.check_rows(Table): break
			except: pass
		return Table


	def get_Table(self):
		if self.check_rows(self.Table):
			return self.Table
		else:
			self.errors.append("Wrong csv format. Separators should be like " + str(self.Separators))
			return self.errors


	def get_col_names(self):
		return self.col_names

	def get_column(self, colname):
		if colname in self.get_col_names():
			return self.Table[colname]
		else:
			self.errors.append("No column with name " + colname)

	def get_errors(self):
		return self.errors

	def format_data(self):
		cols = self.get_col_names()
		for col in cols:
			Col = Column.Column(self.Table[col], self.Conf)
			if Col.isDate():
				Col.format_date()
				self.Table[col] = Col.Col
			elif Col.isNumber():
				Col.format_number()
				self.Table[col] = Col.Col
			else:
				self.Table[col] = Col.Col

	def save_csv(self, path):
		if self.DataReady == False:
			self.format_data()
			self.DataReady = True
		self.Table.to_csv(path, na_rep = "NA", index = False)





if __name__ == '__main__':
	Tab = Table("t.csv")
	Tab.save_csv("t_1.csv")