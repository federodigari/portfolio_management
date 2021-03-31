#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 17:20:51 2021

@author: zhuo
"""
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from functools import reduce
import re

df1 = pd.read_csv('amundi-msci-wrld-ae-c.csv')
df2 = pd.read_csv('ishares-global-corporate-bond-$.csv')
df3 = pd.read_csv('db-x-trackers-ii-global-sovereign-5.csv')
df4 = pd.read_csv('spdr-gold-trust.csv')
df5 = pd.read_csv('usdollar.csv')

#concat and discard irrelevant columns and rename
df_list = [df1, df2, df3, df4, df5]
df_final = reduce(lambda left,right: pd.merge(left,right,on='Date', how='outer'), df_list)
df_final.drop(['Open_x', 'High_x', 'Low_x', 'Change %_x','Open_y', 'High_y', 'Low_y', 'Vol._x', 'Change %_y','Open_x', 'High_x', 'Low_x', 'Vol._y', 'Change %_x','Open_y', 'High_y', 'Low_y', 'Vol._x', 'Change %_y','Open','High', 'Low', 'Vol._y', 'Change %'],axis=1,inplace=True)
df_final.columns = ['Date','ST','CB','PB','GO','CA']

#convert date to sortable values and sort
date=df_final['Date'].str[8:12]+df_final['Date'].str[0:3].replace("Dec","12").replace("Nov","11").replace("Oct","10").replace("Sep","09").replace("Aug","08").replace("Jul","07").replace("Jun","06").replace("May","05").replace("Apr","04").replace("Mar","03").replace("Feb","02").replace("Jan","01")+df_final['Date'].str[4:6]
df_final['Date'] = date.values
df_final.sort_values(by='Date',inplace=True)


#fill in NaN by the previous trading day
df_main=df_final.fillna(method='ffill',axis=0)
#index with Date
df_main = df_main.set_index('Date', drop=False).drop('20200101') #########¿Should we remove first row?

print(df_main)
df_main.to_csv("prices.csv")



#INVESTMENT PORTFOLIO


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
	#Price of the asset to buy. List len 5
	price_in = list()
	for i in df_main:
		if i =='Date':
			pass
		elif i == 'CA':
			price_in.append(1)
		else:
			price_in.append(df_main.loc[date_in, i])

	print(price_in)	

	#Initial amount in each asset
	amount_in = list()
	print(asset[1], type(asset[1]))
	for i in asset:
		amount_in.append((i/100) * money_in)

	#Shares bought
	shares_1off = list()
	for price, amount in zip(price_in, amount_in):
		shares_1off.append(amount / price)

	print(shares_1off)	

	#OUTPUT 

	#Obtain price to sell
	price_sell = list()
	for i in df_main:
		if i =='Date':
			pass
		elif i == 'CA':
			price_sell.append(1)
		else:
			price_sell.append(df_main.loc[date_out, i])

	#Money obtain after sell in each asset
	amount_fin = list()
	n = 0
	for share, price in zip(shares_1off, price_sell):
		if asset[n] == 0:
			amount_fin.append(0)
			n = n+1
		else:
			amount_fin.append ((share * price) / (asset[n]/100) * (asset[n]/100))
			n = n+1


	#REBALANCE
	rebalance_dif = list() #Difference in % in portfolio allocation
	for ini, fin in zip(amount_in, amount_fin): 
		rebalance_dif.append(ini/sum(amount_in) - fin/sum(amount_fin))

	amount_reb = list()
	for percentage, amount_fin in zip(rebalance_dif, amount_fin):
		if percentage > 0:
			amount_reb.append()




	return shares_1off



#2. Dollar Cost Averaging (DCA)

def DCA(money_in, date_out):

	#---------------------------------------------------------------
	#ST
	#---------------------------------------------------------------	


	#Obtain first day of month
	m1_list = list()
	d1_list = list()
	
	for date in df_main['Date']:
		if re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(2) not in m1_list:
			if re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(3) == '01':
				m1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(2))
				d1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(0))
			elif re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(3) == '02':
				m1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(2))
				d1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(0))
			elif re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(3) == '03':
				m1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(2))
				d1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(0))
			elif re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(3) == '04':
				m1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(2))
				d1_list.append(re.search(r"(\d{1,4})(\d{1,2})(\d{1,2})", date).group(0))
	print(d1_list, len(d1_list))
	print(m1_list, len(m1_list))

	#Price the first day of the month
	#12 lists (months) with 5 elements (assets)
	price_in = list()
	for date_in in d1_list:
		price_in_i = list()
		price_in.append(price_in_i) #append list for each month
		for header in df_main:
			if header =='Date':
				continue
			if header == 'CA':
				price_in_i.append(1)
			else:
				price_in_i.append(df_main.loc[date_in, header])
			
	#print("price in", price_in, len(price_in))

	#INPUT
	n_month_ST = len(m1_list)
	money_month = money_in/n_month_ST #money per month to buy
	asset = [50, 20, 20, 0, 10]
	asset_month = [i / n_month_ST for i in asset] #list with 5 elements

	#12 lists equals with 5 elements (€)
	amount_in = list()
	for month in d1_list:
		amount_in_i = list()
		amount_in.append(amount_in_i)
		for i in asset_month:
			amount_in_i.append((i/100) * money_month)
	
	'''
	print('Asset', asset)
	print('Asset month', asset_month)
	print('Money month', money_month)
	print('Amount in ', amount_in, len(amount_in))
	'''


	#Shares bought for each month. List of assets for each month 
	#12 lists with 5 assets each one	
	shares_dca = list()
	for price_month, amount_month in zip(price_in, amount_in):
		shares_dca_i = list()
		for price_asset, amount_asset in zip(price_month, amount_month):
			shares_dca_i.append(amount_asset / price_asset)
		shares_dca.append(shares_dca_i)
	#print("Shares", shares_dca, len(shares_dca))


	#OUTPUT 

	#Obtain price to sell
	#1 list of 5 elements (assets) for a date
	price_sell = list()
	for i in df_main:
		if i =='Date':
			pass
		elif i == 'CA':
			price_sell.append(1)
		else:
			price_sell.append(df_main.loc[date_out, i])


	#Obtain final amount, 12 lists with 5 elements
	#NOTE: for each month the buy price its different to the sell price
	#so the final amount if date_buy = date_sell only is the same in the first month
	amount_fin = list()
	for share_month in shares_dca:
		n = 0
		amount_fin_i = list()
		for share_asset, price in zip(share_month, price_sell):

			if share_asset == 0:
				amount_fin_i.append(0)
				n = n+1
			else:
				amount_fin_i.append((share_asset * price) / (asset_month[n]/100) * (asset_month[n]/100))
				n = n+1
		amount_fin.append(amount_fin_i)

	print("INITIAL 0", amount_in[0], len(amount_in))
	print("FINAL 0", amount_fin[0], len(amount_fin))
	print("INITIAL 1", amount_in[1], len(amount_in))
	print("FINAL 1", amount_fin[1], len(amount_fin))

	#REBALANCE
	

	return shares_dca




money = 100
date_in = '20200102'
date_out = '20200102'
#one_off(money, date_in, date_out)

DCA(money, date_out)

#reb(date_out)
	
