#!/usr/bin/env python3
import json,lzma,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;O=Path(sys.argv[1]) if len(sys.argv)>1 else H
f=[{"id":lzma.FILTER_LZMA1,"lc":4,"lp":0,"pb":0,"dict_size":16*1024*1024}]
L,W,B=lzma.decompress((H/"payload.wrt.lzma").read_bytes(),format=lzma.FORMAT_RAW,filters=f).decode("utf-8").split("\x00",2)
ws=W.split("\n");ts=[a+b for a in L.split("\n") for b in map(chr,range(33,127))]
m={ts[i]:ws[i] for i in range(len(ws))}
r=re.compile("|".join(map(re.escape,m))).sub(lambda x:m[x.group(0)],B).encode("utf-8")
i=r.index(b"\n");p=i+1;mf=json.loads(r[:i].decode("utf-8"))
for rel,ln in mf:
 d=O/rel;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(r[p:p+ln]);p+=ln
print(f"[OK] {len(mf)} fichiers extraits dans {O}")
