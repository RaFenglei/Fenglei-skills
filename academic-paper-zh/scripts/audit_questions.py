"""Structural checks only; not a certificate of novelty or scientific validity."""
import json, sys, re
from pathlib import Path

def audit(data):
    errors=[]; ids=set(); questions=set()
    common=['id','question','anchor','hypothesis','prediction','minimal_test','distinction','novelty_status']
    counts=data.get('counts', {'priority':3,'divergent':10})
    if not isinstance(counts,dict): return ['counts: expected object']
    for group,default in [('priority',3),('divergent',10)]:
        count=counts.get(group,default)
        if isinstance(count,bool) or not isinstance(count,int) or count<0:
            errors.append(f'{group}: count must be nonnegative integer');continue
        items=data.get(group,[])
        if not isinstance(items,list): errors.append(group+': expected list');continue
        if len(items)!=count:errors.append(f'{group}: expected {count}, got {len(items)}')
        for i,item in enumerate(items):
            if not isinstance(item,dict):errors.append(f'{group}[{i}]: expected object');continue
            required=common+(['rival','value','resources','falsifier','inconclusive','risks','search_log'] if group=='priority' else [])
            for key in required:
                if not item.get(key) or (isinstance(item[key],str) and not item[key].strip()):errors.append(f'{group}[{i}]: missing {key}')
            identity=item.get('id')
            if identity in ids: errors.append(f'duplicate id: {identity}')
            ids.add(identity)
            q=re.sub(r'[\s\W_]+','',str(item.get('question',''))).lower()
            if q in questions:errors.append('duplicate question: '+q)
            questions.add(q)
            log=item.get('search_log')
            if not isinstance(log,dict): errors.append(f'{identity}: missing search_log object')
            elif log.get('mode')=='online':
                for key in ['date','queries','sources','scope']:
                    if not log.get(key):errors.append(f'{identity}: online search missing {key}')
                if log.get('sources') and (not isinstance(log['sources'],list) or any(not isinstance(u,str) or not u.startswith('https://') for u in log['sources'])):
                    errors.append(f'{identity}: sources must be HTTPS URL list')
                if not isinstance(log.get('queries'),list):errors.append(f'{identity}: queries must be list')
            elif log.get('mode')=='offline':
                if not log.get('reason') or '待核实' not in item.get('novelty_status',''):errors.append(f'{identity}: offline must state reason and pending novelty')
            else:errors.append(f'{identity}: search mode must be online or offline')
    return errors

if __name__=='__main__':
    data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
    errors=audit(data)
    print(json.dumps({'errors':errors,'scope':'structure only; semantic review required'},ensure_ascii=False,indent=2))
    sys.exit(bool(errors))
