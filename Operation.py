from ldap3 import Server, Connection, ALL , NTLM,core,SUBTREE,ALL_ATTRIBUTES,BASE,MODIFY_REPLACE
import sys
import numpy as np

def Bind_Oper(host,port,timeout,id,pw):
    server = Server(host,port,connect_timeout=timeout)
    connect = Connection(server,id,pw)

    if not connect.bind():
        print("invaild account / password ")
        sys.exit(1)
    else:
        print("ldap://"+host+":"+str(port),"   : Connection Success")
    return connect


def Search_Oper(conn,base,filter,scope,attr):
    conn.search(
        search_base = base,
        search_filter = filter,
        search_scope = scope,
        attributes = attr)
    return conn


def Add_Oper(conn,dn,attr):
    conn.add(dn,attributes=attr)
    return conn.result

def Mod_Oper(conn,dn,attr,c_attr):
    conn.modify(dn,{
        attr:[(MODIFY_REPLACE,[c_attr])]})
    print(dn,": Modify_Replace Success")

def Compare_Entry(s,t,conn,dn):
    i = 0
    while i < len(s):
        # ss=len(s[i][0])
        target = s[i][0]
        print(t)
        print(target)
        if target in t:
            print("있어")
        # np_result=np.array_equal(s[i],t[i])
        # print(np_result)
        # if np_result is False:
        #     print(s[i]," : ",t[i])
        #     Mod_Oper(conn,dn,s[i][0],s[i][1][0])
        i = i + 1

def sp_empty(data):                        # 공백제거, 가끔 콤마사이가 띄어져있어 제대로 작동하지않아서 추가함.
    i = 0
    entry_dn_split =""
    temp = data.split(",")
    while i < len(temp):
        if i is len(temp) - 1:
            entry_dn_split += temp[i].strip()
        else:
            entry_dn_split += temp[i].strip() + ","
        i = i + 1
    return entry_dn_split


