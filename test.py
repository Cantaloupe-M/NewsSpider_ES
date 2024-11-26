import requests

cookies = {
    'Qs_lvt_382223': '1723109578%2C1723196264',
    'Qs_pv_382223': '1410631857528691700%2C1661359657171768300',
    '_ntes_nnid': '2195eb0651290af5f618fdcc191147c8,1726213025331',
    '_ntes_nuid': '2195eb0651290af5f618fdcc191147c8',
    'NTES_PASSPORT': '5Dr.lATybR2Tr88BTVDpgH9hyrJoPQu8yaLcYlKRJVSCWh3VWELSHaN4QBTR7_6jwTQRPQGnS_kbDB_sBmnPkU5qBQE8ycyLu2BmuucdcXKenrwwKSAZoM0Ys21WjndxnhjgTlgk9P2ILGpJ6vhKt4iNWfV1ExR_MZb53QJHz00NNHcQ35E1vSm3.eZUmHij5ylX6Ff0zUUCa',
    'timing_user_id': 'time_QGUmInbGEr',
    '_ntes_origin_from': '',
    's_n_f_l_n3': '607610fcf3a134c11730686596436',
    'pver_n_f_l_n3': 'a',
    'UserProvince': '%u5168%u56FD',
    'ne_analysis_trace_id': '1730702033169',
    '_antanalysis_s_id': '1730702443230',
    'NTES_PC_IP': '%E4%B8%9C%E4%BA%AC%7C%E6%97%A5%E6%9C%AC',
    'vinfo_n_f_l_n3': '607610fcf3a134c1.1.1.1730099509816.1730099825553.1730702693887',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,eo;q=0.7',
    # 'cookie': 'Qs_lvt_382223=1723109578%2C1723196264; Qs_pv_382223=1410631857528691700%2C1661359657171768300; _ntes_nnid=2195eb0651290af5f618fdcc191147c8,1726213025331; _ntes_nuid=2195eb0651290af5f618fdcc191147c8; NTES_PASSPORT=5Dr.lATybR2Tr88BTVDpgH9hyrJoPQu8yaLcYlKRJVSCWh3VWELSHaN4QBTR7_6jwTQRPQGnS_kbDB_sBmnPkU5qBQE8ycyLu2BmuucdcXKenrwwKSAZoM0Ys21WjndxnhjgTlgk9P2ILGpJ6vhKt4iNWfV1ExR_MZb53QJHz00NNHcQ35E1vSm3.eZUmHij5ylX6Ff0zUUCa; timing_user_id=time_QGUmInbGEr; _ntes_origin_from=; s_n_f_l_n3=607610fcf3a134c11730686596436; pver_n_f_l_n3=a; UserProvince=%u5168%u56FD; ne_analysis_trace_id=1730702033169; _antanalysis_s_id=1730702443230; NTES_PC_IP=%E4%B8%9C%E4%BA%AC%7C%E6%97%A5%E6%9C%AC; vinfo_n_f_l_n3=607610fcf3a134c1.1.1.1730099509816.1730099825553.1730702693887',
    'referer': 'https://news.163.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

params = {
    'callback': 'data_callback',
}

response = requests.get('https://news.163.com/special/cm_yaowen20200213_05/', params=params, cookies=cookies, headers=headers)
print(response.text)