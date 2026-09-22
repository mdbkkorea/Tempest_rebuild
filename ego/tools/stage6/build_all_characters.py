from pathlib import Path
import struct,hashlib,json
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def rec(op,*a):return struct.pack('<7i',op,*(list(a)+[0]*(6-len(a))))
def scene(limit,actions):return struct.pack('<i',limit)+b'\xff'*32+struct.pack('<II',0,len(actions))+b''.join(actions)
def page(base,text):
 raw=text.encode('cp949')+b'\0'
 # baseline map/header/grid; zero actors, objects and trboxes; one string.
 b=base[:4156]+struct.pack('<5I',0,0,0,1,0)+struct.pack('<I',len(raw))+bytes(v^255 for v in raw)
 return b+struct.pack('<I',2)+scene(-1,[rec(9999,1)])+scene(1,[rec(1108,0),rec(200)])
def validate(b):
 assert b[:12].split(b'\0')[0]==b'E_TOP.zmp'
 assert struct.unpack_from('<II',b,28)==(60,68)
 o=4156
 for stride in [0,28,20]:
  n=struct.unpack_from('<I',b,o)[0];o+=4
  if stride==0:assert n==0
  o+=n*stride
 n=struct.unpack_from('<I',b,o)[0];o+=4
 offsets=struct.unpack_from('<'+'I'*n,b,o);o+=4*n
 ln=struct.unpack_from('<I',b,o)[0];o+=4
 raw=bytes(v^255 for v in b[o:o+ln]);o+=ln
 assert offsets==tuple([0]+[i+1 for i,v in enumerate(raw[:-1]) if v==0])
 for s in raw.split(b'\0')[:-1]:s.decode('cp949')
 ns=struct.unpack_from('<I',b,o)[0];o+=4
 for index in range(ns):
  o+=36
  for block in range(2):
   nr=struct.unpack_from('<I',b,o)[0];o+=4
   for _ in range(nr):
    row=struct.unpack_from('<7i',b,o);o+=28
    if block==1:
     assert row[0] in (1108,200,9999)
     if row[0]==1108:assert 0<=row[1]<n
     if row[0]==9999:assert 0<=row[1]<ns
 assert o==len(b)
base=(P/'evidence/stage3_blank.adv').read_bytes()
assert sha(base)=='5740821c4f1323858ec8c9d6d51b2f77a70c2d098ebf1d3ddf11057476adc927'
link=(P/'evidence/original_ego.lkc').read_bytes();modified=bytearray(link);rows=[]
for num in range(1,11):
 node=num*2;r=link[node*112:(node+1)*112];name=r[:12].split(b'\0')[0].decode()
 assert name==f'_e_s1_{num:02}' and struct.unpack_from('<i',r,72)[0]==num-1
 conditions=list(struct.unpack_from('<8i',r,76))
 modified[node*112+76:node*112+108]=b'\xff'*32
 if num==1:b=(P/'evidence/stage5_clausewitz.adv').read_bytes();status='Recovered 11 passages; reconstructed reader; runtime untested'
 else:
  text=f'개인 정보 {num:02}\n이 인물의 원본 소개 글은 아직 복원되지 않았습니다.\n진행 버튼으로 닫은 뒤 화면 왼쪽 위의 기존 돌아가기 영역을 누르면 인물 목록으로 돌아갑니다.'
  b=page(base,text);status='Navigation diagnostic only; biography not recovered; runtime untested'
 validate(b);(P/'Adv'/f'{name}.adv').write_bytes(b)
 ret=link[(node+1)*112:(node+2)*112];x0,y0,x1,y1=struct.unpack_from('<4i',ret,48)
 rect=[x0-40,y0-32,x1-40,y1-32]
 rows.append({'route':name,'menu_frame_zero_based':num-1,'status':status,'original_conditions':conditions,'return_rectangle_640x480':rect,'return_point_640x480':[(rect[0]+rect[2])//2,(rect[1]+rect[3])//2],'bytes':len(b),'sha256':sha(b)})
allowed={node*112+76+i for node in range(2,21,2) for i in range(32)}
diff=[i for i,(a,b) in enumerate(zip(link,modified)) if a!=b];assert set(diff)<=allowed and len(diff)==24
(P/'Link/_ego.lkc').write_bytes(modified)
(P/'manifest.json').write_text(json.dumps({'runtime_status':'All stage6 changes untested in Win98; stage5 reader also still untested. Stage4 load and return user-confirmed.','pages':rows,'original_link_sha256':sha(link),'diagnostic_link_sha256':sha(modified),'link_changed_byte_offsets':diff,'link_derivation':'Only six Personal Information story-state condition DWORDs changed to -1. All route names, positions, sprites, return nodes and other categories unchanged. Does not modify save flags.'},indent=2)+'\n')
print('Validated ten pages; condition-only link patch:',len(diff),'bytes.')
