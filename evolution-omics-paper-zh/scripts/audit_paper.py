"""Read-only structural checks. Does not certify translation accuracy or layout."""
import argparse
import json
from pathlib import Path
import posixpath
import sys
import zipfile
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/package/2006/relationships}'

def coverage(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    errors = []
    blocks = data.get('blocks', [])
    if not data.get('source'):
        errors.append('Source identity/version missing')
    if not isinstance(blocks, list) or not blocks:
        raise ValueError('blocks must be a non-empty list')
    by_id = {}
    for b in blocks:
        bid = b.get('id')
        if not isinstance(bid, str) or not bid or bid in by_id:
            errors.append('Missing or duplicate block id: '+str(bid))
        else:
            by_id[bid] = b
        for field in ('locator','kind','source_text'):
            if not str(b.get(field,'')).strip():
                errors.append(f'{bid}: missing {field}')
        status = b.get('status')
        if status == 'translated':
            if not str(b.get('translation','')).strip():
                errors.append(f'{bid}: empty translation')
        elif status == 'preserved':
            if not str(b.get('note','')).strip():
                errors.append(f'{bid}: preserved without reason')
        else:
            errors.append(f'{bid}: unfinished or invalid status {status}')
    figures = data.get('figures')
    if not isinstance(figures, list):
        raise ValueError('figures must be a list, including [] for a paper with no figures')
    seen = set()
    for f in figures:
        fid=f.get('id')
        if not isinstance(fid,str) or not fid or fid in seen:
            errors.append('Missing or duplicate figure id: '+str(fid))
        else:
            seen.add(fid)
        asset=f.get('asset')
        if not isinstance(asset,str) or not asset or not (path.parent/asset).is_file():
            errors.append(f'{fid}: missing figure asset')
        if not f.get('locator'):
            errors.append(f'{fid}: missing locator')
        captions=f.get('caption_block_ids')
        if not isinstance(captions,list) or not captions:
            errors.append(f'{fid}: missing caption mapping')
        else:
            for cid in captions:
                if cid not in by_id or by_id[cid].get('kind') != 'caption':
                    errors.append(f'{fid}: invalid caption block {cid}')
        if f.get('included') is not True:
            errors.append(f'{fid}: not included in output')
        if f.get('visual_checked') is not True:
            errors.append(f'{fid}: visual check not recorded')
    if data.get('qa',{}).get('visual_review_completed') is not True:
        errors.append('Both Word documents need recorded visual review')
    return {'check':'coverage-record-consistency','blocks':len(blocks),
            'figures':len(figures),'errors':errors,
            'limitation':'Checks recorded coverage, not source completeness, semantic accuracy or truth of review flags.'}

def docx(path):
    errors=[]
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist())
        if 'word/document.xml' not in names:
            raise ValueError('Not a DOCX: missing word/document.xml')
        document=ET.fromstring(z.read('word/document.xml'))
        for relname in sorted(n for n in names if n.endswith('.rels')):
            rels=ET.fromstring(z.read(relname))
            # package _rels/.rels -> root; part/ _rels/file.xml.rels -> part/
            base=posixpath.dirname(posixpath.dirname(relname))
            for rel in rels.findall(R+'Relationship'):
                if rel.get('TargetMode') == 'External':
                    continue
                target=rel.get('Target','')
                from urllib.parse import unquote
                target=unquote(target.split('#',1)[0])
                resolved=posixpath.normpath(posixpath.join(base,target)).lstrip('/')
                if not target or resolved not in names:
                    errors.append(f'Missing internal relationship target: {relname} -> {target}')
        return {'check':'docx-structure',
                'paragraphs':len(document.findall('.//'+W+'p')),
                'tables':len(document.findall('.//'+W+'tbl')),
                'drawings':len(document.findall('.//'+W+'drawing')),
                'legacy_pictures':len(document.findall('.//'+W+'pict')),
                'media_files':len([n for n in names if n.startswith('word/media/') and not n.endswith('/')]),
                'errors':errors,
                'limitation':'Media/drawing counts are not figure counts; layout and scientific content require review.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['coverage','docx'])
    parser.add_argument('path',type=Path)
    args=parser.parse_args()
    try:
        result=coverage(args.path) if args.mode=='coverage' else docx(args.path)
    except (OSError,ValueError,TypeError,KeyError,AttributeError,ET.ParseError,zipfile.BadZipFile) as e:
        result={'check':args.mode,'errors':[str(e)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result['errors'] else 0

if __name__=='__main__':
    sys.exit(main())
