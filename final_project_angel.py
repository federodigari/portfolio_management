#INVESTMENT PORTFOLIO
import pandas as pd 
import numpy as np 
import re

ST = pd.read_csv('C:\\Users\\sanch\\Desktop\\Master\\2nd Semester\\Programming for DS\\Final Project\\assignment_PDS\\amundi-msci-wrld-ae-c.csv')
PB = pd.read_csv('C:\\Users\\sanch\\Desktop\\Master\\2nd Semester\\Programming for DS\\Final Project\\assignment_PDS\\db-x-trackers-ii-global-sovereign-5.csv')
CB = pd.read_csv('C:\\Users\\sanch\\Desktop\\Master\\2nd Semester\\Programming for DS\\Final Project\\assignment_PDS\\ishares-global-corporate-bond-$.csv')
GO = pd.read_csv('C:\\Users\\sanch\\Desktop\\Master\\2nd Semester\\Programming for DS\\Final Project\\assignment_PDS\\spdr-gold-trust.csv')
CA = pd.read_csv('C:\\Users\\sanch\\Desktop\\Master\\2nd Semester\\Programming for DS\\Final Project\\assignment_PDS\\usdollar.csv')

ST = pd.DataFrame(ST).set_index('Date', drop=False)
PB = pd.DataFrame(PB).set_index('Date', drop=False)
CB = pd.DataFrame(CB).set_index('Date', drop=False)
GO = pd.DataFrame(GO).set_index('Date', drop=False)
CA = pd.DataFrame(CA).set_index('Date', drop=False)

print(ST)
print('aaaaaa')
print(CB)
'''
print(ST[ST['date_in'] == 'Dec 31, 2020']['Price'])
date_ine = 'Dec 31, 2020'
print(ST.loc[date_ine,'Price'])
'''

'''
b = 'Jan 13, 2020'
a = re.search(r"(.*)(\s)(.*)(,)(.*)", b).group(3)  #1= month, 3=day
print(type(a))
print(a)
if re.search(r"(.*)(\s)(.*)(,)(.*)", b).group(3) == '13':
	print("bien")

print(ST[ST['date_in'] == 'Jan 13, 2020']['Price'])
'''

#TRADING METHODOLOGY
#1. One off (1-OFF)  


def one_off(money_in, date_in, date_out):
	asset = [50, 20, 20, 0, 10]
	'''
	ST_1off = list()
	PB_1off = list()
	CB_1off = list()
	GO_1off = list()
	CA_1off = list()
	'''
	price_ST = ST.loc[date_in,'Price']
	price_PB = PB.loc[date_in,'Price']
	price_CB = CB.loc[date_in,'Price']
	price_GO = GO.loc[date_in,'Price']
	price_CA = 1

	ST_shares_1off = (asset[0]/100 * money_in) / price_ST
	PB_shares_1off = asset[1]/100 * money_in / price_PB
	CB_shares_1off = asset[2]/100 * money_in / price_CB
	GO_shares_1off = asset[3]/100 * money_in / price_GO
	CA_shares_1off = asset[4]/100 * money_in / price_CA

	shares_1off = [ST_shares_1off, PB_shares_1off, CB_shares_1off, GO_shares_1off, CA_shares_1off]
	print("share", shares_1off)

	#OUTPUT 
	price_ST_sell = ST.loc[date_out,'Price']
	price_PB_sell = PB.loc[date_out,'Price']
	price_CB_sell = CB.loc[date_out,'Price']
	price_GO_sell = GO.loc[date_out,'Price']
	price_CA_sell = 1

	price_sell = [price_ST_sell, price_PB_sell, price_CB_sell, price_GO_sell, price_CA_sell]

	print("Precio", price_ST, price_ST_sell)

	money_final = list()
	n = 0
	
	
	for share, price in zip(shares_1off, price_sell):
		if asset[n] == 0:
			money_final.append(0)
			n = n+1
		else:
			money_final.append ((share * price) / (asset[n]/100) * (asset[n]/100))
			n = n+1


	#print("in", shares_1off[0] * price_sell[0] / (asset[0]/100))

	print("money", money_final)

	return shares_1off



#2. Dollar Cost Averaging (DCA)

def DCA(money_in):

	#---------------------------------------------------------------
	#ST
	#---------------------------------------------------------------	
	m1_list_ST_dca = list()
	d1_list_ST_dca = list()

	for date in ST['Date']:
		if re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1) not in m1_list_ST_dca:
			if re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '01':
				m1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))
			elif re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '02':
				m1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))
			elif re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '03':
				m1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))
			elif re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '04':
				m1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d1_list_ST_dca.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))
	#print(d_list_ST)
	n_month_ST = len(m1_list_ST_dca)
	money_month = money_in/n_month_ST
	asset = [50, 20, 20, 0, 10]
	asset_month = [i / n_month_ST for i in asset]

	#Price the first day of the month
	price_ST = list()
	for date in d1_list_ST_dca:
		price_ST.append(ST.loc[date,'Price'])
	print(price_ST)

	#Shares bought
	ST_shares_dca = list()
	for price in price_ST:
		ST_shares_dca.append(asset_month[0]/100 * money_in * price)
	print(ST_shares_dca)

	for shares in ST_shares_dca:
		pass

	#---------------------------------------------------------------
	#ST
	#---------------------------------------------------------------	

	#---------------------------------------------------------------
	#ST
	#---------------------------------------------------------------	
	#---------------------------------------------------------------
	#ST
	#---------------------------------------------------------------	
	#---------------------------------------------------------------
	#ST
	#---------------------------------------------------------------			
	return ST_shares_dca

def reb(date_out):
	#Obtain day 15th to rebalance
	m15_list_ST_1off = list()
	d15_list_ST_1off = list()
	for date in ST['Date']:
		if re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1) not in m15_list_ST_1off:
			if re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '15':
				m15_list_ST_1off.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d15_list_ST_1off.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))
			elif re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '16':
				m15_list_ST_1off.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d15_list_ST_1off.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))
			elif re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(3) == '17':
				m15_list_ST_1off.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(1))
				d15_list_ST_1off.append(re.search(r"(.*)(\s)(.*)(,)(.*)", date).group(0))

	#print(d15_list_ST_1off, len(d15_list_ST_1off))
	
	#Save in a list the returning shares in 1OFF
	shares_1off = one_off(money, date_in, date_out)
	print(shares_1off)
	asset = [50, 20, 20, 0, 10]
	price_ST_sell = ST.loc[date_out,'Price']

	money_final = list()
	for i in shares_1off:
		money_final.append (i / (asset[0]/100) / price_ST_sell)
	print(money_final)

money = 100
date_in = 'Jan 08, 2020'
date_out = 'Jan 08, 2020'
one_off(money, date_in, date_out)

#DCA(money)

#reb(date_out)
	

	