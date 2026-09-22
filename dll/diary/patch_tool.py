#!/usr/bin/env python3
"""Hash-guarded Tempest Diary patch / rollback. Never modifies input files."""
from pathlib import Path
import argparse, hashlib, json

def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('mode',choices=['apply','undo']);ap.add_argument('input',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
 root=Path(__file__).resolve().parent;m=json.loads((root/'patch_manifest.json').read_text());b=a.input.read_bytes()
 if a.output.exists():raise ValueError('Output already exists; choose a new filename.')
 if a.mode=='apply':
  if sha(b)=='804ecba6e573f9444e02b12ff8feaead6a77b09e1c07ecac3a3c6872eaccab81':
   b=bytearray(b);b[0x4a5c1]=0x64;b=bytes(b) # Remove the exact earlier Adventure diagnostic patch.
  if sha(b)!=m['original_sha256']:raise ValueError('Input is neither the supported original DLL nor the exact prior diagnostic DLL.')
  out=bytearray(b)
  for e in m['edits']:
   o=int(e['offset'],16);old=bytes.fromhex(e['old']);new=bytes.fromhex(e['new'])
   if bytes(out[o:o+len(old)])!=old:raise ValueError('Original bytes mismatch at '+e['offset'])
   out[o:o+len(old)]=new
  raw=int(m['helper_raw_offset'],16);helper=bytes.fromhex((root/'helper.hex').read_text())
  if len(helper)!=m['helper_bytes']:raise ValueError('Helper size mismatch')
  out.extend(b'\0'*(raw-len(out)));out.extend(helper);out.extend(b'\0'*(m['patched_bytes']-len(out)))
  expected=m['patched_sha256']
 else:
  if sha(b)!=m['patched_sha256']:raise ValueError('Input is not this exact Diary-patched DLL.')
  out=bytearray(b[:m['original_bytes']])
  for e in reversed(m['edits']):
   o=int(e['offset'],16);old=bytes.fromhex(e['old']);new=bytes.fromhex(e['new'])
   if bytes(out[o:o+len(new)])!=new:raise ValueError('Patched bytes mismatch at '+e['offset'])
   out[o:o+len(new)]=old
  expected=m['original_sha256']
 if sha(out)!=expected:raise ValueError('Output hash mismatch; no file written.')
 with a.output.open('xb') as f:f.write(out)
 print(str(a.output)+'\nSHA-256: '+expected)
if __name__=='__main__':
 try:main()
 except (OSError,ValueError,KeyError) as e:raise SystemExit('Error: '+str(e))
