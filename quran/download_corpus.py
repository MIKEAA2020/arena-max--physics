#!/usr/bin/env python3
"""Optional download of the four corpora used by q.py (internet required).
The corpora remain third-party material with their source attribution/rights;
this script does not make them part of the generated-work license.
"""
from pathlib import Path
import json,urllib.request
ROOT=Path(__file__).resolve().parent
for edition in ['quran-simple','en.sahih','en.arberry','en.pickthall']:
    url=f'https://api.alquran.cloud/v1/quran/{edition}'
    req=urllib.request.Request(url,headers={'User-Agent':'Arena research corpus retrieval'})
    with urllib.request.urlopen(req,timeout=90) as r:data=r.read()
    obj=json.loads(data)
    if obj.get('code')!=200 or len(obj.get('data',{}).get('surahs',[]))!=114:
        raise RuntimeError('Unexpected corpus response for '+edition)
    dst=ROOT/(edition+'.json');tmp=dst.with_suffix('.tmp');tmp.write_bytes(data);tmp.replace(dst)
    print(edition,'downloaded',len(data),'bytes')
