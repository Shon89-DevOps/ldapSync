import Operation
import numpy as np
from ldap3 import ALL_ATTRIBUTES,SUBTREE,BASE

total_entries = 0

source = Operation.Bind_Oper('192.168.0.88',11389,5,'cn=Directory manager','dirmanager')
target = Operation.Bind_Oper('192.168.0.209',41389,5,'cn=Directory manager','dirmanager')
s_conn = Operation.Search_Oper(source,"c=kr","(objectclass=*)",SUBTREE,ALL_ATTRIBUTES)

for s_entry in s_conn.response:
    entry_dn = s_entry['dn']
    entry_dn_s = Operation.sp_empty(entry_dn)
    t_conn = Operation.Search_Oper(target, entry_dn_s,"(objectclass=*)",BASE, ALL_ATTRIBUTES)
    if t_conn.result.get('result') == 32:
        t_add = Operation.Add_Oper(target,entry_dn_s,s_entry['attributes'])
        if t_add.result.get('result') == 0:
            print(entry_dn_s,": ADD Success")
        else:
            print(entry_dn_s,": ADD Fail")
    elif t_conn.result.get('result') == 0:
        attr_list = list(s_entry['attributes'].items())
        for t_entry in t_conn.response:
            np_result = np.array_equal(sorted(s_entry['attributes'].items()), sorted(t_entry['attributes'].items()))

            if np_result is False:
                cp_entry = Operation.Compare_Entry(list(sorted(s_entry['attributes'].items())),
                                    sorted(t_entry['attributes'].items()),t_conn,entry_dn_s)
