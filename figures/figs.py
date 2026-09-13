import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.size':9,'font.family':'serif','axes.linewidth':0.8})
def frame(ax,xl,yl,title):
    ax.set_aspect('equal'); ax.set_xlim(*xl); ax.set_ylim(*yl)
    ax.set_xlabel('$x$'); ax.set_ylabel('$ct$'); ax.set_title(title,fontsize=10,pad=8)
    ax.spines[['top','right']].set_visible(False)

# ---- FIG 1: orderings must actually reverse -------------------------------
# E=(1.0,3.0) on A ; B=(2.6,3.3) on B.  dx=1.6, dct=0.3 -> spacelike.
# A frame (bA=0.15): dt-bA*dx = +0.06 > 0  -> E first.
# B frame (bB=0.60): dt-bB*dx = -0.66 < 0  -> B first.
# key: A's command arrives 4.0, B's 5.9 -> unambiguous, A first.
E=(1.0,3.0); Bv=(2.6,3.3); bA,bB=0.15,0.60
fig,ax=plt.subplots(figsize=(6.0,5.0))
frame(ax,(-1.15,4.6),(0.6,7.0),'Figure 1.  Two ledgers, one key')
ax.plot([0,0],[0.6,7.0],'k-',lw=2.4); ax.text(-1.10,6.65,'relay worldline\n(the key)',fontsize=8)
t=np.array([1.0,6.9])
ax.plot(E[0]+bA*(t-E[1]),t,color='C0',lw=1.7)
ax.plot(Bv[0]+bB*(t-Bv[1]),t,color='C3',lw=1.7)
ax.text(1.30,6.75,'probe A',color='C0',fontsize=8); ax.text(4.05,6.35,'probe B',color='C3',fontsize=8)
for p,c,lab in ((E,'C0','$E$  A expires'),(Bv,'C3','$S$  B activates')):
    ax.plot(*p,'o',color=c,ms=7,zorder=6); ax.text(p[0]+.13,p[1]-.30,lab,color=c,fontsize=8.5)
xs=np.array([-1.1,4.55])
ax.plot(xs,E[1]+bA*(xs-E[0]),'--',color='C0',lw=1.2)
ax.plot(xs,Bv[1]+bB*(xs-Bv[0]),'--',color='C3',lw=1.2)
ax.text(-1.10,E[1]+bA*(-1.1-E[0])+.10,"A's slice",color='C0',fontsize=7.5)
ax.text(-1.10,Bv[1]+bB*(-1.1-Bv[0])+.10,"B's slice",color='C3',fontsize=7.5)
for s in (1,-1): ax.plot([E[0],E[0]+s*3.4],[E[1],E[1]+3.4],':',color='0.55',lw=1.0)
ax.text(E[0]+1.35,E[1]+1.75,'light cone of $E$',color='0.4',fontsize=7.5,rotation=45)
for p,c,lab,dy in ((E,'C0',"A's last command",-.02),(Bv,'C3',"B's first command",.02)):
    ax.annotate('',xy=(0,p[1]+p[0]),xytext=p,arrowprops=dict(arrowstyle='-|>',color=c,lw=1.4))
    ax.plot(0,p[1]+p[0],'s',color=c,ms=6,zorder=7)
    ax.text(.10,p[1]+p[0]+dy,lab,color=c,fontsize=7.5,va='center')
ax.text(-1.10,1.05,"A's ledger:  $E$ before $S$\n"
                   "B's ledger:  $S$ before $E$\n"
                   "the key:       A's command, then B's",fontsize=8,
        bbox=dict(boxstyle='round,pad=0.4',fc='0.96',ec='0.7',lw=.8))
fig.tight_layout(); fig.savefig('fig1.png',dpi=200); fig.savefig('fig1.pdf'); plt.close(fig)

# ---- FIG 2: one factor of k ----------------------------------------------
b=0.5; g=1/np.sqrt(1-b**2); Dp=1.4; k=np.sqrt((1+b)/(1-b))
fig,ax=plt.subplots(figsize=(5.2,5.0))
frame(ax,(-0.95,3.3),(0.4,6.4),'Figure 2.  Why one factor of $k$')
ax.plot([0,0],[0.4,6.4],'k-',lw=2.4); ax.text(-0.90,6.05,'acceptor',fontsize=8)
t=np.array([0.6,6.3]); ax.plot(0.35+b*(t-0.3),t,color='C0',lw=1.7)
ax.text(1.95,6.0,'proposer',color='C0',fontsize=8)
t1=1.2; t2=t1+g*Dp
p1=(0.35+b*(t1-0.3),t1); p2=(0.35+b*(t2-0.3),t2)
for p in (p1,p2): ax.plot(*p,'o',color='C0',ms=6.5,zorder=6)
off=0.30
ax.annotate('',xy=(p2[0]+off,p2[1]-off*0.25),xytext=(p1[0]+off,p1[1]-off*0.25),
            arrowprops=dict(arrowstyle='<->',color='C0',lw=1.8))
ax.text(p2[0]+off+.10,(p1[1]+p2[1])/2-.30,'$D_P$ proper',color='C0',fontsize=8.5)
a1,a2=t1+p1[0],t2+p2[0]
for p,a in ((p1,a1),(p2,a2)):
    ax.plot([p[0],0],[p[1],a],':',color='0.55',lw=1.1); ax.plot(0,a,'s',color='C2',ms=6,zorder=7)
ax.annotate('',xy=(-0.17,a2),xytext=(-0.17,a1),arrowprops=dict(arrowstyle='<->',color='C2',lw=2.0))
ax.text(-0.88,(a1+a2)/2,'$k\\,D_P$',color='C2',fontsize=10,rotation=90,va='center')
ax.annotate('',xy=(0.22,a2+0.5),xytext=(0.22,a1),arrowprops=dict(arrowstyle='<->',color='C3',lw=1.7))
ax.text(0.30,(a1+a2)/2+0.25,'$D_A$ must cover this',color='C3',fontsize=8.5)
ax.text(-0.90,5.55,f'$\\beta={b}$,  $k=\\sqrt{{(1+\\beta)/(1-\\beta)}}={k:.3f}$\n'
                   'light delay shifts both arrivals and cancels',fontsize=8,
        bbox=dict(boxstyle='round,pad=0.35',fc='0.96',ec='0.7',lw=.8))
fig.tight_layout(); fig.savefig('fig2.png',dpi=200); fig.savefig('fig2.pdf'); plt.close(fig)

# ---- FIG 3: equal PROPER-time pulses across a flyby ----------------------
def X(t): return 0.55+0.9*np.sqrt(1+((t-3.3)/1.5)**2)
tg=np.linspace(0.2,6.6,4000); v=np.gradient(X(tg),tg)
tau=np.concatenate([[0],np.cumsum(np.sqrt(np.clip(1-v[1:]**2,0,None))*np.diff(tg))])
fig,ax=plt.subplots(figsize=(5.4,5.0))
frame(ax,(-0.55,3.3),(0.0,7.4),'Figure 3.  Counting pulses across a flyby')
ax.plot([0,0],[0.0,7.4],'k-',lw=2.4); ax.text(-0.50,7.05,'acceptor',fontsize=8)
ax.plot(X(tg),tg,color='C0',lw=1.7); ax.text(2.30,6.2,'proposer',color='C0',fontsize=8)
for i,tt in enumerate(np.interp(np.linspace(tau[0]+.35,tau[-1]-.15,9),tau,tg)):
    xe=X(tt); ta=tt+xe
    if ta>7.3: continue
    ax.plot(xe,tt,'o',color='C0',ms=4,zorder=6)
    ax.plot([xe,0],[tt,ta],':',color='0.6',lw=.9)
    ax.plot(0,ta,'s',color='C2',ms=4.5,zorder=7); ax.text(.08,ta-.05,f'{i+1}',color='C2',fontsize=7.5)
ax.text(1.15,0.45,'pulses emitted at equal\nproper-time intervals',color='C0',fontsize=8)
ax.text(0.95,6.55,'arrivals bunch on approach,\nspread on recession',color='C2',fontsize=8)
fig.tight_layout(); fig.savefig('fig3.png',dpi=200); fig.savefig('fig3.pdf'); plt.close(fig)
print("ok")
