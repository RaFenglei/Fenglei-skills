"""Offline scaffold and validation only. Never calls a model or reads credentials."""
import argparse, hashlib, json, pathlib, urllib.parse

def fail(message):
    raise ValueError(message)

def family(role):
    value=role.get('family')
    return 'openai' if value=='codex' else value

def native_codex(role):
    return family(role)=='openai' and role.get('client', 'codex' if role.get('family')=='codex' else None)=='codex'

def check(providers, plan):
    routes=providers['providers']; mode=plan['mode']
    if mode not in ('ask','codex','harness'):fail('invalid mode')
    for key in ('max_calls','max_output_tokens','max_input_chars'):
        if type(plan.get(key)) is not int or plan[key]<=0:fail('invalid budget: '+key)
    for rid,r in routes.items():
        if not r.get('family') or not r.get('model'):fail('missing model/family: '+rid)
        if any(k in r for k in ('key','api_key','token','password')):fail('secret field forbidden')
        if r.get('protocol')=='external':continue
        if r.get('protocol') not in ('messages','chat','responses'):fail('unsupported protocol')
        u=urllib.parse.urlparse(r['base_url'])
        if u.scheme!='https' or u.username or u.password or u.query or u.fragment or u.hostname not in r.get('allowed_hosts',[]):fail('unsafe route: '+rid)
        if not r.get('key_env') or not r.get('quota_group'):fail('missing credential reference/quota group')
    modules=plan['modules']; ids=[m['id'] for m in modules]
    if len(set(ids))!=len(ids):fail('duplicate module')
    deps={m['id']:m.get('depends_on',[]) for m in modules}
    for m in modules:
        if not m.get('acceptance') or not m.get('execute') or not m.get('review'):fail('incomplete module')
        for rid in m['execute']+m['review']:
            if rid not in routes or not routes[rid].get('enabled'):fail('missing/disabled route: '+rid)
            if mode=='codex' and (not native_codex(routes[rid]) or routes[rid]['protocol']!='external'):fail('codex mode cannot use external models')
        for e in m['execute']:
            if mode!='codex' and not any(family(routes[e])!=family(routes[r]) for r in m['review']):fail('no independent reviewer: '+m['id'])
        if any(d not in deps for d in deps[m['id']]):fail('missing dependency')
    done=set(); visiting=set()
    def visit(n):
        if n in visiting:fail('dependency cycle')
        if n in done:return
        visiting.add(n)
        for d in deps[n]:visit(d)
        visiting.remove(n);done.add(n)
    for n in deps:visit(n)
    return {'valid':True,'mode':mode,'modules':len(modules),'execution_authorized':False}

def receipt_check(record, artifact):
    sha=hashlib.sha256(artifact).hexdigest();e=record['executor'];r=record['reviewer'];review=record['review']
    if record['mode'] not in ('codex','harness'):fail('receipt mode must be chosen')
    if record['status']!='accepted' or review['verdict']!='pass':fail('not accepted')
    if record['artifact_sha256']!=sha or review['artifact_sha256']!=sha:fail('artifact changed')
    if not e.get('session') or not r.get('session') or e['session']==r['session']:fail('same/missing session')
    if not e.get('family') or not r.get('family'):fail('missing family')
    if record['mode']=='harness' and family(e)==family(r):fail('same family')
    if record['mode']=='codex' and (not native_codex(e) or not native_codex(r)):fail('not codex-only')
    if not isinstance(review.get('issues'),list):fail('missing issues')
    for i in review['issues']:
        if i.get('severity') not in ('P0','P1','P2','P3') or not all(isinstance(i.get(k),str) for k in ('evidence','fix')):fail('invalid issue')
        if i['severity'] in ('P0','P1'):fail('blocking issue')
    return {'valid':True,'artifact_sha256':sha,'note':'Structural check, not proof of actual execution'}

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    for name in ('init','check'):
        sub.add_parser(name).add_argument('--project',required=True)
    q=sub.add_parser('receipt-check');q.add_argument('--receipt',required=True);q.add_argument('--artifact',required=True)
    a=p.parse_args()
    if a.command=='receipt-check':
        result=receipt_check(json.loads(pathlib.Path(a.receipt).read_text(encoding='utf8')),pathlib.Path(a.artifact).read_bytes())
    else:
        root=pathlib.Path(a.project).resolve();folder=root/'.harness'
        if a.command=='init':
            folder.mkdir(parents=True,exist_ok=True)
            defaults={'providers.json':{'schema_version':1,'project_root':str(root),'providers':{}},'plan.json':{'mode':'ask','max_calls':12,'max_output_tokens':4096,'max_input_chars':80000,'modules':[]}}
            for name,value in defaults.items():
                try:
                    with (folder/name).open('x',encoding='utf8') as f:json.dump(value,f,ensure_ascii=False,indent=2)
                except FileExistsError:pass
            result={'created_or_preserved':str(folder),'note':'Fill project-specific routes; no API calls'}
        else:
            providers=json.loads((folder/'providers.json').read_text(encoding='utf8'))
            if providers['project_root']!=str(root):fail('project mismatch')
            result=check(providers,json.loads((folder/'plan.json').read_text(encoding='utf8')))
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,TypeError,OSError) as e:raise SystemExit('Validation failed: '+str(e))

