# pip install pymysql
# pip install cryptography
import pymysql
import streamlit as st
# Streamlit

def mysql_test(hostname,user,dbpassword,dbname,method):
    query_params = st.experimental_get_query_params()
    usernames = query_params['usernames']
    names = query_params['names']
    password = query_params['password']
    role = query_params['role']
    view = query_params['view']
    conn = pymysql.connect(host=hostname, user=user,password=dbpassword, db=dbname, charset='utf8')

    cur = conn.cursor()
    sql = 'select * from noah.inform where username =%s and name =%s and password =%s'
    vals = (usernames, names, password)
    cur.execute(sql, vals)
    rows = cur.fetchall()

    if len(rows) == 1:
        method
        return role, view
        conn.close()
    else:
        st.write('CONNECTION ERROR')
        conn.close()