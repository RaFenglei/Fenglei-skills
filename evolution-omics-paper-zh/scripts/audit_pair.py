"""Check two distinct DOCX containers and their explicit common source identity.
Usage: python audit_pair.py translation.docx report.docx
Structural check only; does not certify content completeness or rendering.
"""
import sys,zipfile,hashlib,json
from pathlib import Path
from xml.etree import ElementTree as E
def inspect(path):
 p=Path(path)
 with zipfile.ZipFile(p) as z:
  for required in ['[Content_Types].xml','word/document.xml','docProps/core.xml']:
   if required not in z.namelist():raise ValueError('Not a complete DOCX: '+str(p))
  body=E.fromstring(z.read('word/document.xml'));core=E.fromstring(z.read('docProps/core.xml'))
  subject=core.find('{http://purl.org/dc/elements/1.1/}subject')
  text=''.join(body.itertext()).strip()
  if not text:raise ValueError('Empty document: '+str(p))
  return {'path':str(p),'source_version':subject.text if subject is not None else None,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'body_sha256':hashlib.sha256(text.encode()).hexdigest(),'media_count':sum(n.startswith('word/media/') for n in z.namelist())}
def audit(a,b):
 x,y=inspect(a),inspect(b);errors=[]
 if Path(a).resolve()==Path(b).resolve() or x['body_sha256']==y['body_sha256']:errors.append('Two different documents are required')
 if not x['source_version'] or x['source_version']!=y['source_version']:errors.append('Set matching nonempty source identity in DOCX core subject')
 return {'documents':[x,y],'errors':errors,'limitation':'Container and source identity checks only; manual semantic and visual verification required.'}
if __name__=='__main__':
 try:
  if len(sys.argv)!=3:raise ValueError('Usage: audit_pair.py translation.docx report.docx')
  result=audit(sys.argv[1],sys.argv[2]);print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(result['errors']))
 except Exception as exc:print(str(exc),file=sys.stderr);sys.exit(2)
