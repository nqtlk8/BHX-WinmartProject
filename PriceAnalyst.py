# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:26:05 2023

@author: admin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Import Data BHX

data_BHX_01 = pd.read_excel('Gia_BHX_2022-12-01.xlsx')
data_BHX_15 = pd.read_excel('Gia_BHX_2022-12-15.xlsx')

data_BHX_15= data_BHX_15.rename(columns = {'Gia':'Giá'})
data_BHX_15.info()

    #Xóa columns không cần thiết
data_BHX_01 = data_BHX_01.drop(['Sku','Barcode','LinkSku','DateUpdate'], axis = 1)
data_BHX_15 = data_BHX_15.drop(['Sku','Barcode','LinkSku','DateUpdate'], axis = 1)


    # Merge dữ liệu BHX lại với nhau
data_BHX = data_BHX_01.merge(data_BHX_15,on = ['Tên sản phẩm','LinkCategory'], how = 'outer')
data_BHX.info()
data_BHX = data_BHX.rename(columns = {'Giá_x':'Giá_01','Giá_y':'Giá_15'})

    # Tạo cột Category

data_BHX['Category'] = data_BHX['LinkCategory'].apply(lambda x: x.split(".com/")[-1])
data_BHX = data_BHX.drop(columns = 'LinkCategory')


    #Import data Winmart
data_Winmart_01 = pd.read_excel('Gia_Winmart_2022-12-01.xlsx')
data_Winmart_15 = pd.read_excel('Gia_Winmart_2022-12-15.xlsx')

data_Winmart_01.info()

    # Xóa các column không cần thiết
data_Winmart_01 = data_Winmart_01.drop(['Url'], axis = 1)
data_Winmart_15 = data_Winmart_15.drop(['Url'], axis = 1)

    # Merge dữ liệu BHX lại với nhau
data_Winmart = data_Winmart_01.merge(data_Winmart_15,on = ['Tên sản phẩm','Category_link','Sell unit'], how = 'outer')
data_Winmart = data_Winmart.rename(columns = {'Giá_x':'Giá_01','Giá_y':'Giá_15'})

    # Tạo cột Category
data_Winmart['Category'] = data_Winmart['Category_link'].apply(lambda x: x.split(".vn/")[-1])
data_Winmart = data_Winmart.drop(columns = 'Category_link')

    # Nhóm các sản phẩm có cùng công năng lại với nhau
replacementsBHX = {
    'dau-goi': 'Chăm sóc tóc',
    'ca-phe-tra': 'Nước uống',
    'mi':'Thực phẩm',
    'nuoc-giat-bot-giat-nuoc-tay':'Nước tẩy rửa',
    'dau-goi-dau-xa-duong-toc':'Chăm sóc tóc',
    'ca-phe-lon':'Nước uống',
    'nuoc-giat':'Nước tẩy rửa',
    'mi-pho-chao-an-lien':'Thực phẩm',
    'ca-phe-hoa-tan':'Nước uống',
    'nuoc-rua-chen':'Nước tẩy rửa',
    'mi-nui-bun-kho':'Thực phẩm',
    'ca-phe-phin':'Nước uống',
    'nuoc-giat-cho-tre':'Nước tẩy rửa',
    'nuoc-giat-xa-cho-be':'Nước tẩy rửa',
    'mi-chay':'Thực phẩm'
}
new_category_BHX = []
list_loi_BHX = []
for x in data_BHX['Category']:
    if x in replacementsBHX.keys():
        new_category_BHX.append(replacementsBHX[x])
    else:
        list_loi_BHX.append(x)
        
    # Kiểm tra len của new_category_BHX và data_BHX 
print(len(new_category_BHX) == len(data_BHX['Category']))

    # Kiểm tra một vài giá trị của new_category có được chuyển đổi đúng không
patterns = [1,2,5,123,555]
for idx in patterns:
    print(new_category_BHX[idx],data_BHX['Category'][idx])

    # Thêm cột Newcategory vào data_BHX
data_BHX['NewCategory'] = new_category_BHX

    # Kiểm tra tổng quan lần cuối, drop cột Category, rename cột NewCategory thành Category
data_BHX = data_BHX.drop(columns = ['Category'])
data_BHX = data_BHX.rename(columns = {'NewCategory':'Category'})

replacementsWinmart = {
    'mi-thuc-pham-an-lien--c34':'Thực phẩm',
    'mi--c01145': 'Thực phẩm',
    'cham-soc-toc--c0145': 'Chăm sóc tóc',
    'nuoc-giat--c01140': 'Nước tẩy rửa',
    'mien-hu-tiu-banh-canh--c01148':'Thực phẩm',
    'ca-phe--c01162':'Nước uống',
    'nuoc-rua-chen--c01142':'Nước tẩy rửa',
    'pho-bun--c01147':'Thực phẩm'
}
new_category_Winmart = []
list_loi_Winmart = []
for x in data_Winmart['Category']:
    if x in replacementsWinmart.keys():
        new_category_Winmart.append(replacementsWinmart[x])
    else:
        list_loi_Winmart.append(x)

    # Kiểm tra len của new_category_Winmart và data_Winmart
print(len(new_category_Winmart) == len(data_Winmart['Category']))

    # Kiểm tra một vài giá trị của new_category_Winmart có được chuyển đổi đúng không
for idx in patterns:
    print(new_category_Winmart[idx],data_Winmart['Category'][idx])

    # Thêm cột Newcategory vào data_Winmart
data_Winmart['NewCategory'] = new_category_Winmart

    # Kiểm tra tổng quan lần cuối, drop cột Category, rename cột NewCategory thành Category
data_Winmart = data_Winmart.drop(columns = ['Category'])
data_Winmart = data_Winmart.rename(columns = {'NewCategory':'Category'})

    # Kiểm tra duplicate
data_BHX.duplicated().sum()
data_BHX = data_BHX.drop_duplicates()

data_Winmart.duplicated().sum()
data_Winmart = data_Winmart.drop_duplicates()

    ### So sánh danh mục sản phẩm 2 thương hiệu
data_BHX['Category'].value_counts()
data_Winmart['Category'].value_counts()
    # Tạo danh mục công năng của các sản phẩm
Danhmuc = data_BHX['Category'].value_counts().keys().tolist()
    # Tạo biểu đồ cột so sánh số lượng sản phẩm của từng danh mục của 2 thương hiệu
So_Luong_SP_BHX = [631, 630,551 , 511]
So_Luong_SP_Winmart = [59, 158, 159, 343]

barWidth = 0.25
fig = plt.subplots(figsize =(7, 5))

br1 = np.arange(len(So_Luong_SP_BHX))
br2 = [x + barWidth for x in br1]

plt.bar(br1, So_Luong_SP_BHX, color ='r', width = barWidth,
         label ='BHX')
plt.bar(br2, So_Luong_SP_Winmart, color ='g', width = barWidth,
         label ='Winmart')

plt.xlabel('Category', fontweight ='bold', fontsize = 15)
plt.ylabel('Số lượng', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(So_Luong_SP_BHX))],
        Danhmuc)
 
plt.legend()
plt.show()

### So sánh giá của 2 thương hiệu
# Xóa các sản phẩm không có giá để so sánh
data_price_BHX = data_BHX.dropna()
data_price_Winmart = data_Winmart.dropna()
# Chuyển đổi column Giá_01 va Giá_15 sang Int

data_price_BHX['Giá_01'] = data_price_BHX['Giá_01'].str.replace('₫', '')
data_price_BHX['Giá_01'] = data_price_BHX['Giá_01'].str.replace('.', '').astype(int)

data_price_BHX['Giá_15'] = data_price_BHX['Giá_15'].str.replace('₫', '')
data_price_BHX['Giá_15'] = data_price_BHX['Giá_15'].str.replace('.', '').astype(int)

data_price_Winmart['Giá_01'] = data_price_Winmart['Giá_01'].str.replace('₫', '')
data_price_Winmart['Giá_01'] = data_price_Winmart['Giá_01'].str.replace('.', '').astype(int)

data_price_Winmart['Giá_15'] = data_price_Winmart['Giá_15'].str.replace('₫', '')
data_price_Winmart['Giá_15'] = data_price_Winmart['Giá_15'].str.replace('.', '').astype(int)

# Tạo column chenh_lech_gia

data_price_BHX['Chenh_Lech_Gia'] = data_price_BHX['Giá_15'] - data_price_BHX['Giá_01']
data_price_Winmart['Chenh_Lech_Gia'] = data_price_Winmart['Giá_15'] - data_price_Winmart['Giá_01']
# Tạo biểu đồ scater thể hiện mức độ chênh lệch giá của từng danh mục sản phẩm của 2 thương hiệu
fig, ax = plt.subplots()
ax.scatter(data_price_BHX['Category'], data_price_BHX['Chenh_Lech_Gia'])

fig, ax = plt.subplots()
ax.scatter(data_price_Winmart['Category'], data_price_Winmart['Chenh_Lech_Gia'])

