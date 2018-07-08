import unittest
import Config
import Column
import datetime
import pandas as pd


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def Make_test_table(NAs = "NA", DateFormat = "{:%Y-%m-%d %H:%M:%S}", NumberSeparator = "."):
	DateCol = []
	for day in range(1,5):
		if day == 3:
			date = datetime.datetime(2018,1,day*5, 5, 10)
			DateCol.append(DateFormat.format(date))
		else:
			date = datetime.datetime(2018,1,day*5)
			DateCol.append(DateFormat.format(date))
	DateCol.append("NA")
	data = {"NACol" : ["1", NAs, "3", "4", NAs],
			"DateCol" : DateCol,
			"NumCol" : ["100", "100 000", str("10" + NumberSeparator + "1"), str("10" + NumberSeparator + " 000" + NumberSeparator + "1"), "Na"],
			"TextCol" : ["Cat1", "Cat2", "Cat1", "NA", "Cat3"]}
	return pd.DataFrame(data = data)

class test_Column(unittest.TestCase):
	
	def test_NAs(self):
		Conf = Config.Config()
		for NAFormat in Conf.get_NAs():
			Table = Make_test_table(NAs = NAFormat)
			Col = Column.Column(Table["NACol"], Conf)
			self.assertEqual(Col.NAs(), [0, 1, 0, 0, 1])
			self.assertEqual(Col.get_col()[1], "NA")
			self.assertEqual(Col.get_col()[4], "NA")
			self.assertNotEqual(Col.get_col()[0], "NA")

	def test_isDate(self):
		Conf = Config.Config()
		for DateFormat in Conf.get_DateFormats():
			Table = Make_test_table(DateFormat = str("{:" + DateFormat + "}"))
			Col = Column.Column(Table["DateCol"], Conf)
			self.assertEqual(Col.isDate(), True)
			self.assertEqual(Col.DataType, "Date")
			self.assertTrue(DateFormat in Col.DateFormat)
		Conf = Config.Config()
		Table = Make_test_table(DateFormat = str("{:" + DateFormat + "}"))
		Col = Column.Column(Table["NACol"], Conf)
		self.assertNotEqual(Col.isDate(), True)
		Col = Column.Column(Table["NumCol"], Conf)
		self.assertNotEqual(Col.isDate(), True)
		Col = Column.Column(Table["TextCol"], Conf)
		self.assertNotEqual(Col.isDate(), True)

	def test_choose_dateFormat(self):
		Conf = Config.Config()
		for DateFormat in Conf.get_DateFormats():
			Table = Make_test_table(DateFormat = str("{:" + DateFormat + "}"))
			Col = Column.Column(Table["DateCol"], Conf)
			if Col.isDate():
				self.assertEqual(Col.choose_dateFormat(), DateFormat)

	def test_format_date(self):
		Conf = Config.Config()
		for DateFormat in Conf.get_DateFormats():
			Table = Make_test_table(DateFormat = str("{:" + DateFormat + "}"))
			Col = Column.Column(Table["DateCol"], Conf)
			if Col.isDate():
				Col.format_date()
				for i in range(len(Col.Col)):
					self.assertEqual(Col.Col[i], Make_test_table()["DateCol"][i])

	def test_isNumber(self):
		Conf = Config.Config()
		for NumSep in Conf.get_NumberSeparators():
			Table = Make_test_table(NumberSeparator = NumSep)
			Col = Column.Column(Table["NumCol"], Conf)
			isNumber = Col.isNumber()
			self.assertTrue(isNumber)
		Table = Make_test_table()
		Col = Column.Column(Table["TextCol"], Conf)
		isNumber = Col.isNumber()
		self.assertFalse(isNumber)

	def test_format_Number(self):
		Conf = Config.Config()
		for NumSep in Conf.get_NumberSeparators():
			Table = Make_test_table(NumberSeparator = NumSep)
			Col = Column.Column(Table["NumCol"], Conf)
			if Col.isNumber():
				Col.format_number()
				for el in Col.Col:
					if el != "NA":
						self.assertTrue(is_number(el))










if __name__ == '__main__':
	unittest.main()
