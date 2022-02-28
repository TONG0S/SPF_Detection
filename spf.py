#encoding=utf-8
import dns.resolver
import re,json
rdtype='TXT'
all=dict()
temp=['include',"ip4","ip6"]
domain_list=list(set(open('domain.txt','r',encoding='utf-8').readlines()))
for i in domain_list:
    domain = i.strip()
    all[domain] = dict()
    for t in temp:
        all[domain][t]=list()

    try:
        A= dns.resolver.resolve(domain, rdtype)
        for info in A:
            judge=re.findall("(spf)",str(info),re.I)
            if len(judge)>=1:
                include=re.findall("include:(.*?) ",str(info))
                ip4=re.findall("ip4:(.*?) ",str(info))
                ip6=re.findall("ip6:(.*?) ",str(info))
                if len(include)>=1:
                    all[domain]["include"].append(include)
                if len(ip4) >= 1:
                    all[domain]["ip4"].append(ip4)
                if len(ip6) >= 1:
                    all[domain]["ip6"].append(ip4)
                all[domain]["spf_info"]=str(info)
    except Exception  as e:
        pass
    if len(all[domain]["include"])==0 and len(all[domain]["ip4"])==0  and len(all[domain]["ip6"])==0:
        try:
            if  len(all[domain]["spf_info"]) == 0:
                pass
        except:
            del  all[domain]
print("以下域名存在SPF:")
for i  in all.keys():
    print("\t\t{}".format(i))
with open('SPF_Resuite.json','w',encoding='utf-8') as f:
    json.dump(all,f)
