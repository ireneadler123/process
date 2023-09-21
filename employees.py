# Import libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'Theo dõi số nhân viên bán hàng', page_icon = ':trophy:', layout = 'wide')

st.title('Theo dõi số nhân viên bán hàng')

df = pd.read_csv('Vinasoy.csv')
df['Mã NV'] = df['Mã NV'].astype('str')
searchDMS = st.radio('Điền tên DMS vào đây', df['Tên NV'].unique())
df_employees = df[df['Tên NV'] == searchDMS]

# Dataframe of sale
df_employees = df_employees[df_employees['Trạng thái'] == 'Đã duyệt']
df_employees['Month'] =(pd.to_datetime(df_employees['Ngày lấy đơn'], dayfirst = True).dt.month)
df_employees['Month'] = df_employees['Month'].map({
    1: 'Tháng 1/2023',
    2: 'Tháng 2/2023',
    3: 'Tháng 3/2023',
    4: 'Tháng 4/2023',
    5: 'Tháng 5/2023',
    6: 'Tháng 6/2023',
    7: 'Tháng 7/2023',
    8: 'Tháng 8/2023',
    9: 'Tháng 9/2023',
    10: 'Tháng 10/2023',
    11: 'Tháng 11/2023',
    12: 'Tháng 12/2023'
})

employee_sale = df_employees.groupby('Month').agg({'Thành tiền': 'sum'}).reset_index()

# Dataframe of new flavor

df_new1 = df_employees[df_employees['Tên sản phẩm'] == 'Fc.36h']
df_new2 = df_employees[df_employees['Tên sản phẩm'] == 'Fs.36h']
df_new3 = df_employees[df_employees['Tên sản phẩm'] == 'Cf.36h']
df_new4 = df_employees[df_employees['Tên sản phẩm'] == 'Ch.36h']
df_new5 = df_employees[df_employees['Tên sản phẩm'] == 'Cs.36h']
df_new6 = df_employees[df_employees['Tên sản phẩm'] == 'Cp.36h']
df_new7 = df_employees[df_employees['Tên sản phẩm'] == 'Cp.40h']
df_new8 = df_employees[df_employees['Tên sản phẩm'] == 'Ct.36h']
df_new9 = df_employees[df_employees['Tên sản phẩm'] == 'Ct.40h']

df_newFlavor = pd.concat([df_new1,df_new2,df_new3,df_new4,df_new5,df_new6,df_new7,df_new8,df_new9])
df_newFlavor = df_newFlavor[df_newFlavor['Trạng thái'] == 'Đã duyệt']
df_newFlavor['Month'] =(pd.to_datetime(df_newFlavor['Ngày lấy đơn'], dayfirst = True).dt.month)
df_newFlavor['Month'] = df_newFlavor['Month'].map({
    1: 'Tháng 1/2023',
    2: 'Tháng 2/2023',
    3: 'Tháng 3/2023',
    4: 'Tháng 4/2023',
    5: 'Tháng 5/2023',
    6: 'Tháng 6/2023',
    7: 'Tháng 7/2023',
    8: 'Tháng 8/2023',
    9: 'Tháng 9/2023',
    10: 'Tháng 10/2023',
    11: 'Tháng 11/2023',
    12: 'Tháng 12/2023'
})
employee_new = df_newFlavor.groupby(by = ['Month']).agg({'Hàng bán (Thùng)': 'sum'}).reset_index()



col3, col4 = st.columns((2))


# Flavor target

with col3:
    df_target = pd.read_csv('Target_sale.csv')
    df_target['DMS_code'] = df_target['DMS_code'].astype('str')
    df_target = df_target[df_target['Names'] == searchDMS]
    # st.subheader('Chỉ tiêu doanh số bán ra (thùng)')
    # st.table(df_target)

with col4:
    df_flavorTarget = pd.read_csv('Flavor.csv')
    df_flavorTarget['Code'] = df_flavorTarget['Code'].astype('str')
    df_flavorTarget = df_flavorTarget[df_flavorTarget['Name'] == searchDMS]
    # st.subheader('Chỉ tiêu các sản phẩm vị mới (thùng)')
    # st.table(df_flavorTarget)

# Join dataframe

actual = df_target.set_index('Month').join(df_flavorTarget.set_index('Month')).reset_index()

actual = actual.drop(['Code','Name'], axis = 'columns')

total = (actual.set_index('Month').join(employee_sale.set_index('Month'))).reset_index()

result = total.set_index('Month').join(employee_new.set_index('Month')).reset_index()

result = result.rename(columns = {'Month': 'Tháng',
                                  'DMS_code': 'Mã NV',
                                  'Names': 'Tên NV',
                                  'Target': 'Chỉ tiêu doanh số (VNĐ)',
                                  'New': 'Chỉ tiêu vị mới (thùng)',
                                  'Thành tiền': 'Thực hiện doanh số (VNĐ)',
                                  'Hàng bán (Thùng)': 'Bán ra vị mới (Thùng)'})

# months = st.sidebar.radio('Chọn tháng: ', result['Tháng'])
# result = result[result['Tháng'] == months]
result['% DS'] = round(result['Thực hiện doanh số (VNĐ)'] / result['Chỉ tiêu doanh số (VNĐ)'] * 100 * 0.7, 2)
result['% Vị mới'] = round(result['Bán ra vị mới (Thùng)'] / result['Chỉ tiêu vị mới (thùng)'] * 100 * 0.2, 2)
result['Tổng hoành thành'] = result['% DS'] + result['% Vị mới']

st.header('Hoàn thành kênh MT Đông Nam Bộ 1')
st.warning('Lưu ý: Nếu % vị mới > 24 thì sẽ tính bằng 24')
st.table(result)
