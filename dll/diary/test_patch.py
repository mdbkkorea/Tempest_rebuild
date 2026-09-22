from pathlib import Path
import sys,struct,json,itertools

from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE
from unicorn.x86_const import *
O=Path(__file__).resolve().parent;binary=(O/'dllmain_diary.dll').read_bytes();m=json.loads((O/'patch_manifest.json').read_text());p=struct.unpack_from('<I',binary,60)[0];opt=p+24;sh=opt+struct.unpack_from('<H',binary,p+20)[0]
u=lambda o:struct.unpack_from('<I',binary,o)[0]
sections=[struct.unpack_from('<IIII',binary,sh+i*40+8) for i in range(struct.unpack_from('<H',binary,p+6)[0])]
frames=json.loads((O/'sprite_geometry.json').read_text())['frames']
regs=[UC_X86_REG_EAX,UC_X86_REG_ECX,UC_X86_REG_EDX,UC_X86_REG_EBX,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_EFLAGS]
def run(base,alternate,management,fail_at=None):
 uc=Uc(UC_ARCH_X86,UC_MODE_32);uc.mem_map(base,u(opt+56));uc.mem_write(base,binary[:4096])
 for vs,va,rs,raw in sections:uc.mem_write(base+va,binary[raw:raw+rs])
 def read(a):return struct.unpack('<I',uc.mem_read(a,4))[0]
 def write(a,v):uc.mem_write(a,struct.pack('<I',v&0xffffffff))
 rr,sz=u(opt+136),u(opt+140);cur=base+rr
 while cur<base+rr+sz:
  page=read(cur);size=read(cur+4)
  if not size:break
  for j in range(cur+8,cur+size,2):
   v=struct.unpack('<H',uc.mem_read(j,2))[0]
   if v>>12==3:a=base+page+(v&4095);write(a,read(a)+base-0x10000000)
   else:assert v>>12==0
  cur+=size
 uc.mem_map(0,4096);write(0,0x12345678)
 uc.mem_map(0x2000000,0x100000);stack=0x20f0000
 uc.mem_map(0x3000000,0x100000);parent=0x3000000;table=0x3010000;handle=7
 write(base+0x47235c,parent);write(base+0xdc0f0+handle*4,table);write(base+0x49a2c4,0x4f8 if management else 0x4fa);write(base+0x49a2c8,20)
 for f in frames:
  a=table+36*f['index'];write(a+8,f['width']);write(a+12,f['height']);write(a+16,f['origin_x']);write(a+20,f['origin_y'])
 for r,v in zip(regs,[0x1111,0x2222,0x3333,0 if alternate else 0xffffffff,stack,0xffffffff,0,handle,0x246]):uc.reg_write(r,v)
 write(stack+0x3c,handle);write(stack+0x34,99);write(base+0x48dd44,99)
 allocations=[];calls=[];before=[];after=[];freed=[];route=[]
 def hook(uc,a,size,data):
  if a==base+0xa2283:
   s=uc.reg_read(UC_X86_REG_ESP);assert read(s+4)==0x74
   number=len(allocations);ptr=0 if number==fail_at else 0x3020000+0x100*number;allocations.append(ptr)
   if ptr:uc.mem_write(ptr,b'\xcc'*0x74)
   uc.reg_write(UC_X86_REG_EAX,ptr);uc.reg_write(UC_X86_REG_ECX,0xcafecafe);uc.reg_write(UC_X86_REG_EDX,0xbeefbeef);uc.reg_write(UC_X86_REG_ESP,s+4);uc.reg_write(UC_X86_REG_EIP,read(s))
  if a in [base+0x1110,base+0xa2278,base+0xa1b70,base+0xa1b80]:
   s=uc.reg_read(UC_X86_REG_ESP)
   if a==base+0xa2278:freed.append(read(s+4))
   if a==base+0xa1b70:route.append(('state',read(s+4)))
   if a==base+0xa1b80:route.append(('resource',bytes(uc.mem_read(read(s+4),5)).decode('ascii')))
   uc.reg_write(UC_X86_REG_ESP,s+4);uc.reg_write(UC_X86_REG_EIP,read(s))
  if a==base+0x46360:
   s=uc.reg_read(UC_X86_REG_ESP);args=[read(s+4+i*4) for i in range(12)];calls.append((uc.reg_read(UC_X86_REG_ECX),args))
  if a==base+0x4a806:before.extend(uc.reg_read(r) for r in regs)
  if a==base+0x4a80c:after.extend(uc.reg_read(r) for r in regs);uc.emu_stop()
 uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(base+0x4a580,base+0x4a80c,count=20000)
 after=[uc.reg_read(r) for r in regs];assert uc.reg_read(UC_X86_REG_EIP)==base+0x4a80c;assert after==before,(before,after);assert read(0)==0x12345678;assert read(stack+0x34)==0xffffffff;assert read(base+0x48dd44)==0
 controls={}
 for ptr,args in calls:
  id=args[1];assert read(ptr+4)==id;assert read(ptr+12)==parent;assert read(ptr)==base+0xb07b0;assert read(ptr+0x3c)==handle
  assert [read(ptr+x) for x in (0x40,0x44,0x48)]==args[7:10];assert read(ptr+0x70)==args[10]
  rect=[read(ptr+x) for x in (0x4c,0x50,0x54,0x58)];controls[id]=dict(rect=rect,frames=args[7:10],highlight=args[10],anchor=args[2:4])
 expected=([105] if alternate else [100,101])+([103] if management else [])+[104,102]
 if fail_at is not None:expected.pop(fail_at)
 assert set(controls)==set(expected),(controls,expected)
 assert read(parent+0x28)==len(expected)
 # Check ownership chain, so parent teardown sees the new control.
 ptr=read(parent+0x30);chain=[]
 while ptr:chain.append(read(ptr+4));ptr=read(ptr+0x20);assert len(chain)<=6
 assert set(chain)==set(expected)
 for a,b in itertools.combinations(controls.values(),2):
  l,t,r,z=a['rect'];ll,tt,rr,zz=b['rect'];assert min(r,rr)<=max(l,ll) or min(z,zz)<=max(t,tt)
 for id,c in controls.items():
  assert 0<=c['rect'][0]<c['rect'][2]<=640 and 0<=c['rect'][1]<c['rect'][3]<=480
 if 102 in controls:assert controls[102]['frames']==([13,12,12] if alternate else [5,4,4])
 if 102 in controls:
  ptr=next(ptr for ptr,args in calls if args[1]==102)
  write(base+0x472354,base+0x4a170);uc.reg_write(UC_X86_REG_ECX,ptr);uc.reg_write(UC_X86_REG_ESP,stack);write(stack,0x2000000)
  uc.emu_start(base+0x45ec0,base+0x45ed3,count=1000);assert read(base+0x48dd44)==102
  uc.reg_write(UC_X86_REG_ESP,stack);uc.emu_start(base+0x4a99d,base+0x4aacd,count=1000)
  assert route==[('state',4),('resource','_ego\0')],route
 uc.reg_write(UC_X86_REG_ECX,parent);uc.reg_write(UC_X86_REG_ESP,stack);write(stack,0x2000000)
 uc.emu_start(base+0x41300,0x2000000,count=10000)
 assert set(freed)==set(ptr for ptr,args in calls) and len(freed)==len(calls)
 assert read(parent+0x28)==0 and read(parent+0x2c)==0 and read(parent+0x30)==0
 assert read(0)==0x12345678
 return dict(callback_and_ego_dispatch_verified=102 in controls,all_controls_freed_once=True,base=hex(base),alternate=alternate,management=management,allocation_failure_index=fail_at,controls=controls,registers_flags_stack_preserved=True,seh_chain_preserved=True,parent_chain_valid=True,hit_rectangles_nonoverlapping=True)
results=[]
for base,alt,manage in itertools.product([0x10000000,0x18000000],[False,True],[False,True]):
 n=(3 if alt else 4)+int(manage)
 for failure in [None]+list(range(n)):results.append(run(base,alt,manage,failure))
(O/'emulation_validation.json').write_text(json.dumps(dict(status='passed',cases=len(results),method='Unicorn executes patched constructor blocks and original actual control/base constructors; heap allocation/free and state-setting endpoints are stubbed; original callback, EGO dispatch, and recursive destruction code also execute. PE relocations applied at both bases. Not a full Windows/game test.',results=results),indent=2)+'\n')
print('PASS',len(results),'constructor cases')
