import pandas as pd
import sys
import calendar

"""
Imports a python file that initializes 3 arrays, they are used to identify the text of the items in the xls file:
utilities: contains the billing companies (as specified in the xls file) for water, energy, internet, rent...
restaurants: contains restaurants names, as specified in the xls file.
supermarkets: same for supermarkets, to summarize groceries expenses.
"""
from category_lists import restaurants, supermarkets, utilities

filename = 'Movimientos_EVO.xls'
n_months = 12

class Expense:
	power = 0
	water = 0
	rent = 0
	internet = 0
	trash = 0
	groceries = 0
	restaurants = 0
	other = 0
	total = 0

def checkItemCategory(msg, categories):
	index = 0
	for i in categories:
		if i in msg:
			return True, index
		index += 1
	return False, None

def formatFloat(num):
	return str(round(num, 2))


def main():
	# Check parameters
	if len(sys.argv) < 2:
		print("ERROR: Invalid argument.\nYou must specify the year you want the summary for.\n\ti.e. 'python3 evoneitor.py 2020'")
		exit()

	# Read the year we want the report for from the command line parameters
	year = int(sys.argv[1])

	# Read excel file
	rows = pd.read_excel(filename)

	# Prepare array to store data classified by month and expense type
	expense_list = [Expense() for i in range(n_months)]

	# Process file
	for index, row in rows.iterrows():
		item = row['Concepto']
		amount = row['Importe']
		y = row['Fecha Contable'].year
		m = row['Fecha Contable'].month
	# Process only the data for the given year
		if y == year and amount < 0:
	# Check items
			found = False
			found, category_index = checkItemCategory(item, restaurants)
			if found:
				expense_list[m-1].restaurants -= amount
			else:
				found, category_index = checkItemCategory(item, supermarkets)
				if found:
					expense_list[m-1].groceries -= amount
				else:
					found, category_index = checkItemCategory(item, utilities)
					if found:
						if category_index == 0:
							expense_list[m-1].power -= amount
						elif category_index in range(1,3): # Note: ranges may vary depending on the utilities array order
							expense_list[m-1].water -= amount
						elif category_index in range(3,6):
							expense_list[m-1].rent -= amount
						elif category_index == 6:
							expense_list[m-1].internet -= amount
						elif category_index == 7:
							expense_list[m-1].trash -= amount
						else:
							print("ERROR: could not find the category (index: " + str(category_index) + ")")
			if not found:
				expense_list[m-1].other -= amount
			
			expense_list[m-1].total -= amount

	cnt = 1
	for i in range(12):
		total = 0
		print("MONTH: " + calendar.month_name[cnt])
		print("  power:       " + formatFloat(expense_list[i].power))
		print("  water:       " + formatFloat(expense_list[i].water))
		print("  rent:        " + formatFloat(expense_list[i].rent))
		print("  internet:    " + formatFloat(expense_list[i].internet))
		print("  trash:       " + formatFloat(expense_list[i].trash))
		print("  groceries:   " + formatFloat(expense_list[i].groceries))
		print("  restaurants: " + formatFloat(expense_list[i].restaurants))
		print("  other:       " + formatFloat(expense_list[i].other))
		print("TOTAL:         " + formatFloat(expense_list[i].total))
		print("*********************************")
		cnt+=1

if __name__ == "__main__":
	main()