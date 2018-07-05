# Reading csv in different formats

## Summary

Class Table which is reading csv as pandas DataFrame and transforms it into most popular scv format.  
For example, it transforms this:  

ColumnNumberOne/ColumnNumberTwo/ColumnNumberThree  
01 12 2017/Some Text1/10  
15 12 2017/Some Text2/100 000  
20 12 2017/Some Text1/10,02  
21 12 2017/Some Text2/100 000,001

Into this:  

ColumnNumberOne,ColumnNumberTwo,ColumnNumberThree  
2017-12-01,Some Text1,10  
2017-12-15,Some Text2,100000  
2017-12-20,Some Text1,10.02  
2017-12-21,Some Text2,100000.001

So by using that class you can always be shure about data types and formats of your columns

## Requiered libraries:  
_regex_ - to check date and numeric formats  
_json_ - needed for config file where you can add more date formats, csv separators, etc. which will be checked while forming the final csv
from the initial one  
_pandas and numpy_ - because that project is a part of my machineLearning framework, which I will place here right after it will be done  

## How to use

```python

import Table from Table

Csv = Table.load_Table('initial_csv.csv')
Csv.save_csv('final_csv.csv')

```
