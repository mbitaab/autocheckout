import json
from collections import defaultdict
import os
import re
import sys


def create_merch_info(domains, outpath,source_dir):
  
    res = [
        r'"(merchantID|payerID)".+?"([A-Z0-9]{13})"',
        r'"(merchantId|payerId)".+?"([A-Z0-9]{13})"',
        r'"(merchantid|payerid)".+?"([A-Z0-9]{13})"',
        r'merchant-id.+?([A-Z0-9]{13})',
    ]
    domain_red = defaultdict()
    for domain in domains:
        merchant_ids = defaultdict(list)

        # look for merchant id in the source code
        source_fname = domain.replace('https://', 'https___')
        if 'georigia' in source_fname:
            print(source_fname)
        
        source_path = None

        # open the related source path
        for i in range(2):
            source_path = os.path.join(source_dir, source_fname+ str(i) + '.html')
            if os.path.exists(source_path):
               
                f = open(source_path, 'r')
                for line2 in f.readlines():
                    line2 = line2.strip().replace("&quot;", '"').replace('\\', '')
                                
                    for r in res:
                        results = re.findall(r, line2)
                        if results:
                            for mid in set(results):
                                merchant_ids[i].append(mid[1])
            else:
                continue
           
        if merchant_ids:
            tmp = defaultdict()
            tmp['merch_id'] = merchant_ids
            domain_red[domain] = tmp
                                    

    json.dump(domain_red, open(outpath, 'w'), indent=4)


def parse_data(infile, outpath, source_dir):
    
    fin = open(infile, 'r')
    print(infile, '....')
    domains = []
    for line in fin.readlines():
        line = line.strip()
        line_dict = json.loads(line)
        domains.append(line_dict['domain'])
    create_merch_info(domains, outpath, source_dir)

