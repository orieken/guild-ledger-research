"""Deliberate defects, maintained separately from evaluator expectations."""
from pathlib import Path
import shutil

API={
 'shared-data-mutated':("params = request.query_params","params = request.query_params\n    if params.get('difficulty') == 'easy':\n        QUESTS.pop()"),
 'quest-write-added':("@app.get('/health')","@app.post('/api/quests')\ndef write_quest():\n    return {'created': True}\n\n@app.get('/health')"),
 'or-filters':("and ('status' not in params or q['status'] == params['status'])","or ('status' not in params or q['status'] == params['status'])"),
 'regex-search':("query in q['title'].casefold()","__import__('re').search(query, q['title'].casefold())"),
 'list-payload':("return {'quests': sorted(selected, key=lambda q: (q['title'].casefold(), q['id']))}","return {'quests': [{'id': q['id']} for q in selected]}"),
 'unsorted':("sorted(selected, key=lambda q: (q['title'].casefold(), q['id']))","selected"),
 'difficulty-ignored':("q['difficulty'] == params['difficulty']","True"),
 'search-not-trimmed':("params.get('q', '').strip().casefold()","params.get('q', '').casefold()"),
 'search-case-sensitive':("query in q['title'].casefold()","query in q['title']"),
 'status-ignored':("q['status'] == params['status']","True"),
 'empty-enum-accepted':("if name in params and params[name] not in values:","if name in params and params[name] and params[name] not in values:"),
 'duplicates-accepted':("if len(params.getlist(name)) > 1:","if False:"),
 'unknown-rejected':("params = request.query_params","params = request.query_params\n    if any(k not in ('q','difficulty','status') for k in params):\n        return error(400, 'INVALID_REQUEST', 'Unknown query')"),
 'detail-incomplete':("return quest","return {'id': quest['id'], 'description': quest['description']}"),
 'missing-id-200':("return error(404, 'NOT_FOUND', 'Quest not found')","return error(200, 'NOT_FOUND', 'Quest not found')"),
 'health-broken':("return {'status': 'ok', 'service': 'guild'}","return {'status': 'broken', 'service': 'guild'}"),
}
UI={
 'initial-load-missing':('onMounted(load)', 'onMounted(()=>{})'),
 'network-error-swallowed':("if(version===listVersion)error.value='Could not load quests. Please try again.'","if(false)error.value='Could not load quests. Please try again.'"),
 'http-status-ignored':("if(!response.ok)throw new Error('List failed')","// HTTP status ignored by deliberate mutant"),
 'loading-missing':('v-if="loading" role="status"','v-if="false" role="status"'),
 'empty-missing':('v-else-if="empty" role="status"','v-else-if="false" role="status"'),
 'alert-missing':('v-if="error" role="alert"','v-if="error" role="status"'),
 'detail-reward-missing':('<dt>Reward gold</dt><dd>{{detail.reward_gold}}</dd>',''),
 'filters-reset':('detail.value=body',"detail.value=body;difficulty.value='';status.value=''"),
 'detail-error-clears-list':("error.value='Could not load quest details.'","{error.value='Could not load quest details.';quests.value=[]}"),
 'stale-list':('if(version!==listVersion)return','if(false)return'),
 'stale-detail':('if(version!==detailVersion)return','if(false)return'),
 'apply-inaccessible':('<button type="submit">Apply</button>','<span @click="load">Apply</span>'),
}
EXPECTED={
 'shared-data-mutated':'A13','initial-load-missing':'U01','network-error-swallowed':'U06',
 'quest-write-added':'A12','or-filters':'A05','regex-search':'A04','http-status-ignored':'U07',
 'list-payload':'A01','unsorted':'A02','difficulty-ignored':'A03','search-not-trimmed':'A04','search-case-sensitive':'A04','status-ignored':'A05','empty-enum-accepted':'A06','duplicates-accepted':'A07','unknown-rejected':'A08','detail-incomplete':'A09','missing-id-200':'A10','health-broken':'A11',
 'loading-missing':'U04','empty-missing':'U05','alert-missing':'U07','detail-reward-missing':'U03','filters-reset':'U03','detail-error-clears-list':'U08','stale-list':'U09','stale-detail':'U10','apply-inaccessible':'U02',
}
def materialize(starter,reference,target,mutation=None):
    shutil.copytree(starter,target)
    shutil.copyfile(reference/'app.py',target/'services/guild/app.py')
    shutil.copyfile(reference/'App.vue',target/'web/src/App.vue')
    if mutation:
        path=target/('services/guild/app.py' if mutation in API else 'web/src/App.vue')
        old,new=(API|UI)[mutation];source=path.read_text()
        if source.count(old)!=1:raise ValueError('Mutation anchor must occur exactly once: '+mutation)
        path.write_text(source.replace(old,new))
