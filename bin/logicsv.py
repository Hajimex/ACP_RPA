# coding:utf-8
import sys
import argparse
import csv
import pandas as pd
import codecs
import math

def Read_File(f):
	file_path = "data/" + f

	with codecs.open(file_path, "r", "Shift-JIS", "ignore") as file:
		df = pd.read_table(file, delimiter=",")
		df.to_csv("data/utf-8_" + f, encoding='utf-8',index=False) 
		df = pd.read_csv("data/utf-8_" + f, encoding="utf-8")

	return df

def Shipping_Method(df,yupacket_products):
	#もしSKUが特定のものだったら、ゆうパケット、それ以外だったらゆうパック
	for yupacket_product in yupacket_products:
		for index, row in df.iterrows():
			if df.at[index,'Lineitem sku']==yupacket_product:
				df.at[index,'Shipping Method']=u"ゆうパケット"
			else:
				df.at[index,'Shipping Method']=u"ゆうパック"
	return df

def Validate_Address(df):
	# 1.Tax 1~5 Name Tax 1~5 Valueを置き換えて、コピペする
	print(df[:10])
	df = df.rename(columns={
		"Tax 1 Name": "Shipping_Province", 
		"Tax 1 Value": "Shipping_Province_T", 
		"Tax 2 Name": "Shipping_Province_Is_Correct", 
		"Tax 2 Value": "Shipping_City", 
		"Tax 3 Name": "Shipping_City_T", 
		"Tax 3 Value": "Shipping_City_Is_Correct", 
		"Tax 4 Name": "Shipping_Street", 
		"Tax 4 Value": "Shipping_Street_T", 
		"Tax 5 Name": "Shipping_Street_Is_Correct", 
		"Tax 5 Value": "Shipping_Address2",
		"Barcode": "Shipping_Zip"
	})
	df['Shipping_Province'] = df['Shipping Province']
	df['Shipping_City'] = df['Shipping City']
	df['Shipping_Street'] = df['Shipping Street']
	df['Shipping_Address2'] = df['Shipping Address2']

	# 2. ZIP CODEを調べて、正しい値をゲットする
	KEN_ALL = pd.read_csv("src/KEN_ALL.CSV",encoding="utf-8")
	df["Shipping_Zip"]=df["Shipping Zip"].str.replace("-","").astype(int)

	df["Shipping_Province_T"]=df.Shipping_Zip.map(KEN_ALL.prefecture)

	df = pd.merge(df,KEN_ALL,on="Shipping_Zip",how='left')

	df["Shipping_Province_T"]=df["prefecture"]
	df["Shipping_City_T"]=df["city"]
	df["Shipping_Street_T"]=df["street"]

	df['Shipping_Province_Is_Correct'] = (df['Shipping_Province_T'] == df['Shipping_Province'])
	df['Shipping_City_Is_Correct'] = (df['Shipping_City'] == df['Shipping_City_T'])
	
	for index, row in df.iterrows():
		# 町名と前方一致
		Shipping_Street_Series = df['Shipping_Street'].str.startswith(df.at[index,'Shipping_Street_T'])
		# 市区町村に含まれるか
		if type(df.at[index,'Shipping_Street_T']) is float and math.isnan(df.at[index,'Shipping_Street_T']):
			df.at[index,'Shipping_Street_T'] = ""
		Shipping_City_Series = df['Shipping_City'].str.contains(df.at[index,'Shipping_Street_T'])
		if Shipping_Street_Series[index] == False and Shipping_City_Series[index] == False:
			df.at[index,'Shipping_Street_Is_Correct'] = False
		else:
			df.at[index,'Shipping_Street_Is_Correct'] = True
		df['Shipping_Street_Is_Correct'].astype(bool)

	return df

def If_Test(df,test_names,test_products):
	#もし注文者名に特定文字が含まれているか、商品SKUがテスト商品のSKUだったら住所欄をテストにする
	for test_name in test_names:
		# print(df['Billing Name'].str.contains(test_name))
		df.loc[df['Billing Name'].str.contains(test_name), 'Shipping_Province'] = u"テスト"
	for test_product in test_products:
		# print(df['Lineitem sku']==test_product)
		df.loc[df['Lineitem sku']==test_product, 'Shipping_Province'] = u"テスト"

	return df

def Output(df):
	df.to_csv("output.sjis.csv", encoding="shift_jis", index=False)
	return df

def main(f,test_names,test_products,yupacket_products):
	df = Read_File(f)
	df = Shipping_Method(df,yupacket_products)
	df = Validate_Address(df)
	df = If_Test(df,test_names,test_products)
	df = Output(df)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='enter the value')
	parser.add_argument('--file', help='file name')    # 必須の引数を追加
	# parser.add_argument('arg2', help='foooo')

	test_names = [u"テスト"] #配列にするs
	test_products = ["SFwtest","SFwtests"] #配列にする
	yupacket_products = ["SFwo002s"] #配列にする
	args = parser.parse_args()
	print("args.file",args.file)

	main(args.file,test_names,test_products,yupacket_products)