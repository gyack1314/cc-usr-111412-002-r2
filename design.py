"""两阶段饱和设计的合法性与真实分配抽样。"""
import random,math,itertools
from common import digest

def validate(data):
    membership={}
    for g in data['groups']:
        n=len(g['units']);levels=g['levels']
        if not n or len(set(g['units']))!=n:raise ValueError('组成员非法')
        if abs(sum(x['p'] for x in levels)-1)>1e-12:raise ValueError('饱和档概率和不为一')
        for l in levels:
            if type(l['m']) is not int or not 0<=l['m']<=n or l['p']<=0:raise ValueError('饱和档非法')
        for u in g['units']:
            if u in membership:raise ValueError('企业重复分组')
            membership[u]=g['id']
    invited=set(data['invited'])
    if not invited<=set(membership):raise ValueError('未知邀请企业')
    for g in data['groups']:
        if len(invited&set(g['units'])) not in {x['m'] for x in g['levels']}:raise ValueError('实际分配不在设计支持内')
    if set(data['outcomes'])!=set(membership) or any(type(v) is not int or v not in (0,1) for v in data['outcomes'].values()):raise ValueError('试验结果不完整')
    return membership

def draw(data,seed):
    validate(data);rng=random.Random(seed);out=[]
    for g in data['groups']:
        l=rng.choices(g['levels'],weights=[x['p'] for x in g['levels']])[0]
        out+=rng.sample(sorted(g['units']),l['m'])
    return sorted(out)

def local_space(g):
    for l in g['levels']:
        prob=l['p']/math.comb(len(g['units']),l['m'])
        for combination in itertools.combinations(sorted(g['units']),l['m']):yield combination,prob
