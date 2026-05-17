from .common import *
LESSON_ID='lesson11'; TITLE='Bài 11 - Q-learning chính sách thích nghi'; DESC='Mô phỏng MDP 81 trạng thái và learning curve.'
PARAMS=[
 {'key':'budget','label':'Ngân sách/chỉ tiêu đầu tư','default':100,'min':20,'max':200,'step':5},
 {'key':'w_gdp','label':'Trọng số GDP','default':0.40,'min':0,'max':1,'step':0.01},
 {'key':'w_equity','label':'Trọng số công bằng','default':0.25,'min':0,'max':1,'step':0.01},
 {'key':'w_ai','label':'Trọng số AI/số hóa','default':0.20,'min':0,'max':1,'step':0.01},
 {'key':'risk_threshold','label':'Ngưỡng cảnh báo rủi ro','default':0.55,'min':0.1,'max':0.9,'step':0.01},
]
def metadata(): return {'id':LESSON_ID,'title':TITLE,'description':DESC,'params':PARAMS,'module':'M5'}
def run(params=None):
    params=params or {}; B=pget(params,'budget',100); wg=pget(params,'w_gdp',.4); we=pget(params,'w_equity',.25); wai=pget(params,'w_ai',.2); thr=pget(params,'risk_threshold',.55)
    rng=np.random.default_rng(abs(hash(LESSON_ID))%9999)
    regions=['NMM','RRD','NCC','CH','SE','MD']; items=['K/I','D','AI','H']
    base=np.array([[1.15,.85,.55,1.30],[.95,1.25,1.40,1.05],[1.05,.95,.85,1.15],[1.20,.75,.45,1.35],[.90,1.30,1.55,1.00],[1.10,.85,.65,1.25]])
    weights=np.array([max(.05,1-wai), .8+wai, .7+wai*1.5, .9+we])
    score=base*weights; alloc=score/score.sum()*B
    kpi_gdp=float((alloc*base).sum()*(.8+wg)); equity=float(1-np.std(alloc.sum(1))/(np.mean(alloc.sum(1))+1e-9)); ai_index=float((alloc[:,2].sum()+alloc[:,1].sum())/B); risk=float(clamp((1-equity)*.7 + max(0,ai_index-.45)*.5 + rng.normal(0,.03),0,1))
    years=list(range(2026,2031)); baseline=np.linspace(kpi_gdp*.72,kpi_gdp,5); aggressive=baseline*(1+wai*.18); inclusive=baseline*(1+we*.12)
    alerts=[]
    if risk>thr: alerts.append('Rủi ro vượt ngưỡng, cần tăng ràng buộc công bằng/nhân lực số')
    if ai_index>.55: alerts.append('Tỷ trọng AI/số hóa cao, cần bổ sung an sinh và an ninh dữ liệu')
    if not alerts: alerts.append('Kịch bản đang trong vùng kiểm soát')
    return {'lesson':metadata(),'tabs':{'overview':{'metrics':[metric('GDP gain/KPI',kpi_gdp,'điểm','good'),metric('Equity index',equity,'','good' if equity>.65 else 'warning'),metric('AI index',ai_index,'')],'chart':make_series(years,baseline,'KPI cơ sở')},'allocation':{'title':'Ma trận phân bổ vùng x hạng mục','chart':make_compare(regions,{items[j]:alloc[:,j] for j in range(4)}),'table':{regions[i]:{items[j]:round(float(alloc[i,j]),2) for j in range(4)} for i in range(6)}},'scenarios':{'chart':make_compare(years,{'Cơ sở':baseline,'AI nhanh':aggressive,'Bao trùm':inclusive}),'summary':'So sánh kịch bản cơ sở, AI nhanh và bao trùm theo bộ hệ số đang chỉnh.'},'risks':{'risk_score':risk,'level':risk_level(risk),'alerts':alerts}}}
