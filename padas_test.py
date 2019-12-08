import pandas as pd

def excel_read():
	df = pd.read_excel("11.xlsx", header=[0], usecols='A')
	#data = df.head()
	print(df.shape[0])

	a = []
	i = 0
	for v in df.iloc[:,0]:
		a.append(v)

	#print(type(df))
	#print(df.iloc[:,0])

	print(a)

def main():
	#df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
	#df.to_excel('22.xlsx')
	excel_read()


if __name__ == '__main__':
	main()