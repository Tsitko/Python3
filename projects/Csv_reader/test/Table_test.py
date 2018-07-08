import unittest
import Table
import Config

__TESTSCVPATH__ = "test_csv.csv"

def Make_test_csv(sep=",", row1 = ["col1", "col2"], row2 = ["row1col1", "row1col2"]):
	with open(__TESTSCVPATH__, "w") as test_csv:
		test_csv.write(row1[0] + sep + row1[1] + "\n" + row2[0] + sep + row2[1])

class test_Table(unittest.TestCase):
	def test_Table_check_rows(self):
		Conf = Config.Config()
		for sep in Conf.get_CsvSeparators():
			Make_test_csv(sep)
			Tab = Table.Table(__TESTSCVPATH__)
			self.assertEqual(Tab.check_rows(Tab.get_Table()), True)
		Make_test_csv("-:-:-")
		Tab = Table.Table(__TESTSCVPATH__)
		self.assertEqual(Tab.check_rows(Tab.get_Table()), False)
		Make_test_csv("-::-")
		Tab = Table.Table(__TESTSCVPATH__)
		self.assertEqual(Tab.check_rows(Tab.get_Table()), False)

	def test_Table_read_Table(self):
		Make_test_csv()
		Tab = Table.Table(__TESTSCVPATH__)
		data = Tab.read_Table()
		self.assertEqual(data["col1"][0], "row1col1")
		self.assertEqual(data["col2"][0], "row1col2")
		Make_test_csv("-:-:-")
		Tab = Table.Table(__TESTSCVPATH__)
		self.assertEqual(Tab.get_Table(), Tab.get_errors())

if __name__ == '__main__':
	unittest.main()



