from .common import *
from scipy.optimize import linprog
LESSON_ID='lesson02'; TITLE='Bài 2 - LP phân bổ ngân sách 4 hạng mục'; DESC='Tối ưu ngân sách I, AI, H, R&D và phân tích độ nhạy.'
PARAMS=[{'key':'budget','label':'Ngân sách tổng','default':100,'min':70,'max':160,'step':5},{'key':'coef_I','label':'Hệ số I','default':0.85,'min':0.4,'max':2,'step':0.05},{'key':'coef_AI','label':'Hệ số AI','default':1.20,'min':0.4,'max':2,'step':0.05},{'key':'coef_H','label':'Hệ số H','default':0.95,'min':0.4,'max':2,'step':0.05},{'key':'coef_RD','label':'Hệ số R&D','default':1.35,'min':0.4,'max':2,'step':0.05}]
def metadata(): return {'id':LESSON_ID,'title':TITLE,'description':DESC,'params':PARAMS,'module':'M3'}
def solve(B, params):
    c=[-pget(params,'coef_I',.85),-pget(params,'coef_AI',1.2),-pget(params,'coef_H',.95),-pget(params,'coef_RD',1.35)]
    A=[[1,1,1,1],[-1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,-1],[.35,-.65,.35,-.65]]; b=[B,-25,-15,-20,-10,0]
    res=linprog(c,A_ub=A,b_ub=b,bounds=[(0,None)]*4,method='highs')
    x=res.x if res.success else np.zeros(4); return x, -res.fun if res.success else 0, res.success
def run(params=None):
    params=params or {}; B=pget(params,'budget',100); labels=['I hạ tầng','AI dữ liệu','H nhân lực','R&D']; x,z,ok=solve(B,params); bs=[100,120,140, B]; vals=[solve(bb,params)[1] for bb in bs]
    risk=0.2 if ok else .9
    return {'lesson':metadata(),'tabs':{'overview':{'metrics':[metric('Giá trị tối ưu Z*',z,'nghìn tỷ','good' if ok else 'danger'),metric('Ngân sách',B,'nghìn tỷ'),metric('Trạng thái',1 if ok else 0,'khả thi')],'chart':make_series(labels,x,'Phân bổ')},'allocation':{'title':'Phân bổ tối ưu 4 hạng mục','chart':make_series(labels,x,'Ngân sách'),'table':dict(zip(labels,[round(float(v),3) for v in x]))},'scenarios':{'chart':make_series([str(int(b)) for b in bs],vals,'Z*(B)'),'summary':'Độ nhạy theo ngân sách 100/120/140 và giá trị tùy chỉnh.'},'risks':{'risk_score':risk,'level':risk_level(risk),'alerts':['Bài toán khả thi' if ok else 'Bài toán không khả thi','R&D/AI dễ hút vốn do hệ số biên cao']}}}
