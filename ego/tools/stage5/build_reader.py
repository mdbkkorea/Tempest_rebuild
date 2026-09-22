"""Rebuild the diagnostic reader using only Python 3 and bundled stage-4 input."""
from pathlib import Path
import struct,hashlib,json
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
u=lambda b,o:struct.unpack_from('<I',b,o)[0]
def record(op,*args): return struct.pack('<7i',op,*(list(args)+[0]*(6-len(args))))
def scene(limit,actions): return struct.pack('<i',limit)+b'\xff'*32+struct.pack('<II',0,len(actions))+b''.join(actions)
def validate(b):
 assert b[:12]==b'E_TOP.zmp\0\0\0'
 assert struct.unpack_from('<II',b,28)==(60,68)
 o=4156;assert u(b,o)==0;o+=4
 count=u(b,o);o+=4;assert count==11;o+=28*count
 assert u(b,o)==0;o+=4
 n=u(b,o);o+=4;offsets=struct.unpack_from('<'+'I'*n,b,o);o+=n*4
 length=u(b,o);o+=4;text=bytes(v^255 for v in b[o:o+length]);o+=length
 assert offsets==tuple([0]+[i+1 for i,v in enumerate(text[:-1]) if v==0])
 strings=text.split(b'\0');assert strings[-1]==b''
 for s in strings[:-1]:s.decode('cp949')
 scenes=u(b,o);o+=4;assert scenes==2
 actions=[]
 for index in range(scenes):
  limit=struct.unpack_from('<i',b,o)[0];o+=36
  nc=u(b,o);o+=4;assert nc==0
  na=u(b,o);o+=4
  rows=[struct.unpack_from('<7i',b,o+i*28) for i in range(na)];o+=na*28;actions.append(rows)
  assert limit==(-1 if index==0 else 1)
 assert o==len(b)
 assert actions[0]==[(9999,1,0,0,0,0,0)]
 seq=[12]+list(range(11))+[13]
 assert len(actions[1])==len(seq)*2
 for i,s in enumerate(seq):
  assert actions[1][2*i]==(1108,s,0,0,0,0,0)
  assert actions[1][2*i+1]==(200,0,0,0,0,0,0)
 return {'bytes':len(b),'text_count':n,'scene_count':scenes,'text_sequence':seq,'sha256':sha(b)}
def build():
 src=(ROOT/'evidence/stage4_working.adv').read_bytes()
 assert sha(src)=='7fbfaef22ee314c2dacee8541ecf6e9d4cca077487377a65de35e6651f509aa3'
 old=bytes(v^255 for v in src[0x11b4:0x2c3f]);assert len(old)==6795
 ui=['클라우제비츠 - 개인 정보\n아래의 진행 버튼으로 글을 읽으세요. 긴 글은 여러 화면으로 나뉩니다.\n목록으로 돌아가기: 화면 왼쪽 위의 기존 돌아가기 영역.', '읽기를 마쳤습니다.\n화면 왼쪽 위의 기존 돌아가기 영역을 누르면 인물 목록으로 돌아갑니다. 다시 들어오면 처음부터 읽을 수 있습니다.']
 payload=old+b''.join(s.encode('cp949')+b'\0' for s in ui)
 offsets=[0]+[i+1 for i,v in enumerate(payload[:-1]) if v==0]
 assert len(offsets)==14
 actions=[]
 for index in [12]+list(range(11))+[13]: actions += [record(1108,index),record(200)]
 b=src[:0x117c]+struct.pack('<I',len(offsets))+struct.pack('<14I',*offsets)+struct.pack('<I',len(payload))+bytes(v^255 for v in payload)+struct.pack('<I',2)+scene(-1,[record(9999,1)])+scene(1,actions)
 result=validate(b)
 # Original header, grid, objects and trbox block are untouched. All twelve original strings remain byte-identical.
 assert b[:0x117c]==src[:0x117c]
 new_text_start=0x117c+4+14*4+4
 assert b[new_text_start:new_text_start+6795]==src[0x11b4:0x2c3f]
 (ROOT/'Adv/_e_s1_01.adv').write_bytes(b)
 result.update({'status':'offline validated; Win98 runtime test pending','source_stage4_sha256':sha(src),'original_text_bytes_preserved':6795,'new_ui_strings':ui,'derivation':'Preserve header/grid/object/trbox blocks and all original strings; append two authored navigation strings; replace prototype scene table with a once-per-entry sequential 1108/200 reader. No DLL, LKC, SPR or ZMP changes.'})
 (ROOT/'provenance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':build()
