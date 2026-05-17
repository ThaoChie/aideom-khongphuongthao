from .common import *
LESSON_ID='lesson01'
TITLE='Bài 1 - Cobb-Douglas mở rộng với AI và số hóa'
DESC='Ước lượng TFP, phân rã tăng trưởng và dự báo GDP 2030.'
PARAMS=[
 {'key':'alpha','label':'α - Vốn vật chất K','default':0.33,'min':0.05,'max':0.60,'step':0.01},
 {'key':'beta','label':'β - Lao động L','default':0.42,'min':0.05,'max':0.60,'step':0.01},
 {'key':'gamma','label':'γ - Số hóa D','default':0.10,'min':0.01,'max':0.40,'step':0.01},
 {'key':'delta','label':'δ - Năng lực AI','default':0.08,'min':0.01,'max':0.40,'step':0.01},
 {'key':'theta','label':'θ - Nhân lực số H','default':0.07,'min':0.01,'max':0.40,'step':0.01},
 {'key':'tfp_growth','label':'Tăng TFP/năm đến 2030','default':0.012,'min':0.0,'max':0.05,'step':0.001},
]
def metadata(): return {'id':LESSON_ID,'title':TITLE,'description':DESC,'params':PARAMS,'module':'M1'}
def run(params=None):
    params=params or {}; years=np.arange(2020,2026); Y=np.array([8044.4,8487.5,9513.3,10221.8,11511.9,12847.6]); K=np.array([16500,17800,19600,21300,23500,25900]); L=np.array([53.6,50.5,51.7,52.4,52.9,53.4]); D=np.array([12.0,12.7,14.3,16.5,18.3,19.5]); AI=np.array([55.6,60.2,65.4,67.0,73.8,80.1]); H=np.array([24.1,26.1,26.2,27.0,28.4,29.2])
    a=pget(params,'alpha',.33); b=pget(params,'beta',.42); g=pget(params,'gamma',.10); d=pget(params,'delta',.08); t=pget(params,'theta',.07); s=a+b+g+d+t or 1
    a,b,g,d,t=[x/s for x in [a,b,g,d,t]]
    A=Y/(K**a*L**b*D**g*AI**d*H**t); yhat=A.mean()*K**a*L**b*D**g*AI**d*H**t; mape=np.mean(np.abs((Y-yhat)/Y))*100
    fy=np.arange(2026,2031); kg=pget(params,'k_growth',.06); lg=pget(params,'l_growth',.006); tfpg=pget(params,'tfp_growth',.012)
    Kf=K[-1]*(1+kg)**np.arange(1,6); Lf=L[-1]*(1+lg)**np.arange(1,6); Df=np.linspace(D[-1],30,5); AIf=np.linspace(AI[-1],100,5); Hf=np.linspace(H[-1],35,5); Af=A[-1]*(1+tfpg)**np.arange(1,6); Yf=Af*Kf**a*Lf**b*Df**g*AIf**d*Hf**t
    contrib={'K':a*np.mean(np.diff(np.log(K))),'L':b*np.mean(np.diff(np.log(L))),'D':g*np.mean(np.diff(np.log(D))),'AI':d*np.mean(np.diff(np.log(AI))),'H':t*np.mean(np.diff(np.log(H))),'TFP':np.mean(np.diff(np.log(A)))}
    total=sum(contrib.values()) or 1; contrib_pct={k:v/total*100 for k,v in contrib.items()}
    risk=0.25 if mape<5 else .55 if mape<10 else .8
    return {'lesson':metadata(),'tabs':{'overview':{'metrics':[metric('GDP dự báo 2030',Yf[-1],'nghìn tỷ VND','good'),metric('MAPE',mape,'%','good' if mape<8 else 'warning'),metric('TFP trung bình',A.mean(),'','neutral')],'chart':make_series([*years,*fy],[*Y,*Yf],'GDP thực tế/dự báo')},'allocation':{'title':'Phân rã đóng góp tăng trưởng','chart':make_series(contrib_pct.keys(),contrib_pct.values(),'Đóng góp %'),'table':contrib_pct},'scenarios':{'chart':make_compare(fy,{'Cơ sở':Yf,'TFP cao':Yf*1.05,'AI nhanh':Yf*1.035}),'summary':'So sánh kịch bản cơ sở, TFP cao và AI tăng nhanh.'},'risks':{'risk_score':risk,'level':risk_level(risk),'alerts':['MAPE cao cần kiểm định lại hệ số' if mape>=8 else 'Mô hình ổn định với bộ hệ số hiện tại','Tổng hệ số được tự chuẩn hóa về 1']}}}
