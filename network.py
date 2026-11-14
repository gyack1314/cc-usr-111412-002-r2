"""事前网络的暴露编码与来源绑定。"""
from design import validate
from common import digest

def exposure(data,invited=None):
    members=validate(data);neighbors={u:set() for u in members}
    for a,b in data['edges']:
        if a==b or a not in members or b not in members or members[a]!=members[b]:raise ValueError('网络跨组或有非法边')
        neighbors[a].add(b);neighbors[b].add(a)
    z=set(data['invited'] if invited is None else invited)
    if not z<=set(members):raise ValueError('未知分配企业')
    return {u:[int(u in z),int(bool(neighbors[u]&z))] for u in sorted(members)}

def prepared(data):return {'design_digest':digest(data['groups']),'network_digest':digest(sorted(sorted(e) for e in data['edges'])),'observed_exposure':exposure(data),'outcomes':data['outcomes']}
