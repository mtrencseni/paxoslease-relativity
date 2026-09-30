import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.size':7,'font.family':'serif',
                     'font.serif':['STIXGeneral','DejaVu Serif'],
                     'mathtext.fontset':'stix','axes.linewidth':0.8})

# one palette for every figure
C_OLD = '#1f4e9c'   # observer A / old owner / proposer
C_NEW = '#b02a1f'   # observer B / new owner
C_ARR = '#2e7d32'   # light arrivals, acceptor side
C_RES = '#111111'   # resource and acceptor worldline
C_AXIS= '0.55'      # the axes of the diagram's own frame
C_OVL = '#6a1b9a'   # overlap of the two authority regions
C_AUX = '0.45'      # light rays, construction lines

# one style vocabulary for every figure
LW_WORLD, LW_LEASE, LW_RAY, LW_NOW, LW_ARROW = 1.4, 2.2, 0.9, 0.9, 1.0
MS_EVENT, MS_ARR, MS_DATE = 5.0, 4.5, 4.5
FS_TITLE, FS_AXIS, FS_EVENT, FS_ANNOT, FS_BOX = 7.2, 7.0, 7.5, 6.4, 6.2
BOX = dict(boxstyle='round,pad=0.30', fc='0.96', ec='0.7', lw=0.8)

def axis_arrow(ax,p0,p1,color):
    """One axis: a thin arrow.  An arrowhead means an axis; worldlines have none."""
    ax.annotate('',xy=p1,xytext=p0,annotation_clip=False,
                arrowprops=dict(arrowstyle='-|>,head_width=0.16,head_length=0.38',
                                color=color,lw=0.8,shrinkA=0,shrinkB=0))

def axes_arrows(ax,color=None):
    """The two axes of the frame the diagram is drawn in."""
    color = C_AXIS if color is None else color
    for sp in ('top','right','left','bottom'): ax.spines[sp].set_visible(False)
    (x0,x1),(y0,y1)=ax.get_xlim(),ax.get_ylim()
    axis_arrow(ax,(x0,y0),(x1,y0),color); axis_arrow(ax,(x0,y0),(x0,y1),color)

def frame(ax,xl,yl,title=''):
    ax.set_aspect('equal'); ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('$x$',fontsize=FS_AXIS,labelpad=1,color=C_AXIS)
    ax.set_ylabel('$ct$',fontsize=FS_AXIS,labelpad=1,color=C_AXIS)
    ax.set_title(title,fontsize=FS_TITLE,pad=4) if title else None
    axes_arrows(ax)

# ---- FIG 1: Newtonian vs relativistic simultaneity, with light cones ----
P=(0.28,1.00); Q=(1.15,1.18); b=0.6
XL,YL=(-0.10,1.88),(-0.08,1.88)
def panel(ax,rel,title):
    ax.set_aspect('equal'); ax.set_xlim(*XL); ax.set_ylim(*YL)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('$x$',fontsize=FS_AXIS,labelpad=1,color=C_OLD)
    # Newtonian mechanics has no invariant speed, so (a) plots t, not ct
    ax.set_ylabel('$ct$' if rel else '$t$',fontsize=FS_AXIS,labelpad=1,color=C_OLD)
    # A's axes meet at the origin, so A's worldline x = 0 is the drawn ct axis
    for sp in ('top','right','left','bottom'): ax.spines[sp].set_visible(False)
    axis_arrow(ax,(0,0),(XL[1],0),C_OLD); axis_arrow(ax,(0,0),(0,YL[1]),C_OLD)
    ax.set_title(title,fontsize=FS_TITLE,pad=4)
    ax.text(0.05,1.72,'A',color=C_OLD,fontsize=FS_EVENT)
    ct2=1.78; axis_arrow(ax,(0,0),(b*ct2,ct2),C_NEW)
    ax.text(b*ct2+0.05,ct2-0.12,"B, $ct'$" if rel else "B, $t'$",color=C_NEW,fontsize=FS_EVENT)
    if rel:
        x2=1.78; axis_arrow(ax,(0,0),(x2,b*x2),C_NEW)
        ax.text(x2-0.10,b*x2-0.20,"$x'$",color=C_NEW,fontsize=FS_EVENT)
    else:
        ax.text(1.40,0.07,"$x'$ axis $=$ $x$ axis",color=C_NEW,fontsize=FS_ANNOT,ha='right')
    xs=np.array((0.0,XL[1])); sB = b if rel else 0.0
    for E in (P,Q):
        if rel:
            ax.plot(xs,E[1]+0*xs,'--',color=C_OLD,lw=LW_NOW,alpha=.75)
            ax.plot(xs,E[1]+sB*(xs-E[0]),'--',color=C_NEW,lw=LW_NOW,alpha=.75)
        else:
            ax.plot(xs,E[1]+0*xs,'--',color=C_AUX,lw=LW_NOW,alpha=.75)
        ax.plot(0,E[1],'d',color=C_OLD,ms=MS_DATE,zorder=7)
        ctp=(E[1]-sB*E[0])/(1-sB*b); ax.plot(b*ctp,ctp,'d',color=C_NEW,ms=MS_DATE,zorder=7)
    # The diamonds are the events' time coordinates, t on A's axis and t' on B's:
    # follow the line through the event parallel to that observer's space axis
    # until it meets its time axis.  A is at rest in the diagram's frame, so its
    # lines are horizontal in both panels.
    for E,lab in ((P,'P'),(Q,'Q')):
        ctp=(E[1]-sB*E[0])/(1-sB*b)
        # in (b) B's labels sit where no dashed line runs: P_B upper left, Q_B lower right
        offB=((-0.06,0.08,'right') if lab=='P' else (0.07,-0.09,'left')) if rel else (0.07,0.05,'left')
        for pt,who,(dx,dy,ha) in (((0.0,E[1]),'A',(0.07,0.05,'left')),((b*ctp,ctp),'B',offB)):
            tl=('$t_{%s}$' if who=='A' else '$t^{\prime}_{%s}$')%lab   # the event's time coordinate for that observer
            ax.text(pt[0]+dx,pt[1]+dy,tl,fontsize=FS_ANNOT,color=C_OLD if who=='A' else C_NEW,va='center',ha=ha)
    for E,lab,c,dx,dy in ((P,'$P$',C_OLD,-0.17,-0.13),(Q,'$Q$',C_NEW,0.07,-0.13)):
        ax.plot(*E,'o',color=c,ms=MS_EVENT,zorder=10); ax.text(E[0]+dx,E[1]+dy,lab,color=c,fontsize=FS_EVENT)
    msg=("A: $P$ then $Q$\nB: $Q$ then $P$" if rel else "A: $P$ then $Q$\nB: $P$ then $Q$")
    ax.text(1.84,0.20,msg,fontsize=FS_BOX,bbox=BOX,ha='right',va='bottom')
fig,axs=plt.subplots(1,2,figsize=(6.9,2.35))
panel(axs[0],False,"(a)  Newtonian: one global time")
panel(axs[1],True ,"(b)  Special relativity: $x'$ tilts with $ct'$")
fig.tight_layout(w_pad=1.4); fig.savefig('fig1.png',dpi=200); fig.savefig('fig1.pdf'); plt.close(fig)

# ---- FIG 2: light cones, authority regions, and the three conditions ------
fig,axs=plt.subplots(1,2,figsize=(7.0,2.75))
X=np.linspace(-1.6,4.4,900); T=np.linspace(-0.2,4.0,900)
XX,TT=np.meshgrid(X,T)
def band(ax,acq,exp,color,alpha):
    inA=(TT-acq[1])>=np.abs(XX-acq[0]); inB=(TT-exp[1])>=np.abs(XX-exp[0])
    ax.contourf(XX,TT,(inA&~inB).astype(float),levels=[.5,1.5],colors=[color],alpha=alpha)
    return inA&~inB
def cone_edges(ax,e,color,ls,lw=LW_RAY):
    for sgn in (1,-1): ax.plot([e[0],e[0]+sgn*6],[e[1],e[1]+6],ls,color=color,lw=lw)
def setup(ax,title):
    ax.set_xlim(-1.6,4.4); ax.set_ylim(-0.2,3.35); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('$x$',fontsize=FS_AXIS,labelpad=1,color=C_AXIS)
    ax.set_ylabel('$ct$',fontsize=FS_AXIS,labelpad=1,color=C_AXIS)
    axes_arrows(ax)
    ax.set_title(title,fontsize=FS_TITLE,pad=4)

# (a) causal exclusion holds
ax=axs[0]; setup(ax,"(a)  $\\mathsf{C}$ holds:  $P \\in J^-(Q)$")
P0,P=(0,0.0),(0,0.8); Q,Q0=(0.8,1.8),(0.8,2.6)
band(ax,P0,P,C_OLD,.30); band(ax,Q,Q0,C_NEW,.30)
for e,c in ((P0,C_OLD),(P,C_OLD),(Q,C_NEW),(Q0,C_NEW)): cone_edges(ax,e,c,':')
ax.plot([0,0],[-0.2,0.8],'-',color=C_OLD,lw=LW_LEASE)
ax.plot([0.8,0.8],[1.8,2.6],'-',color=C_NEW,lw=LW_LEASE)
for e,lab,c,dx,dy in ((P0,'$P_0$',C_OLD,-.42,-.04),(P,'$P$',C_OLD,-.32,.02),
                      (Q,'$Q$',C_NEW,-.34,-.02),(Q0,'$Q_1$',C_NEW,-.44,.02)):
    ax.plot(*e,'o',color=c,ms=MS_EVENT,zorder=6); ax.text(e[0]+dx,e[1]+dy,lab,color=c,fontsize=FS_EVENT)
ax.plot([2.4,2.4],[-0.2,4.0],'-',color=C_RES,lw=LW_WORLD)
ax.text(2.48,3.05,'$W$',fontsize=FS_EVENT,color=C_RES)
ax.text(-1.38,1.68,'$\\mathcal{A}_{\\rm old}$',color=C_OLD,fontsize=FS_EVENT)
ax.text(1.02,2.98,'$\\mathcal{A}_{\\rm new}$',color=C_NEW,fontsize=FS_EVENT)

# (b) causal exclusion fails
ax=axs[1]; setup(ax,"(b)  $\\mathsf{C}$ fails:  $P$, $Q$ spacelike")
P0,P=(0,0.0),(0,0.8); Q,Q0=(2.0,1.1),(2.0,1.9)
mo=band(ax,P0,P,C_OLD,.30); mn=band(ax,Q,Q0,C_NEW,.30)
ax.contourf(XX,TT,(mo&mn).astype(float),levels=[.5,1.5],colors=[C_OVL],alpha=.55)
for e,c in ((P0,C_OLD),(P,C_OLD),(Q,C_NEW),(Q0,C_NEW)): cone_edges(ax,e,c,':')
ax.plot([0,0],[-0.2,0.8],'-',color=C_OLD,lw=LW_LEASE)
ax.plot([2.0,2.0],[1.1,1.9],'-',color=C_NEW,lw=LW_LEASE)
for e,lab,c,dx,dy in ((P0,'$P_0$',C_OLD,-.42,-.04),(P,'$P$',C_OLD,-.32,.02),
                      (Q,'$Q$',C_NEW,.10,-.10),(Q0,'$Q_1$',C_NEW,.10,.04)):
    ax.plot(*e,'o',color=c,ms=MS_EVENT,zorder=6); ax.text(e[0]+dx,e[1]+dy,lab,color=c,fontsize=FS_EVENT)
ax.plot([0.5,0.5],[-0.2,4.0],'-',color=C_RES,lw=LW_WORLD)
ax.plot([1.6,1.6],[-0.2,4.0],'-',color=C_RES,lw=LW_WORLD)
ax.text(0.42,3.05,'$W_a$',fontsize=FS_EVENT,color=C_RES,ha='right')
ax.text(1.68,3.05,'$W_b$',fontsize=FS_EVENT,color=C_RES)
ax.text(-1.38,1.68,'$\\mathcal{A}_{\\rm old}$',color=C_OLD,fontsize=FS_EVENT)
ax.text(3.36,2.84,'$\\mathcal{A}_{\\rm new}$',color=C_NEW,fontsize=FS_EVENT)
ax.annotate('',xy=(1.82,2.05),xytext=(2.62,2.92),arrowprops=dict(arrowstyle='-|>',color=C_OVL,lw=LW_ARROW))
ax.text(2.34,2.98,'both owners',color=C_OVL,fontsize=FS_ANNOT)
ax.plot([-1.6,4.4],[0.95,0.95],'--',color=C_AUX,lw=LW_NOW,alpha=.75)
ax.text(2.60,0.60,"line of now in $S$",fontsize=FS_ANNOT,color=C_AUX)
for src,lab,dy in ((P,'$R_P$',-.04),(Q,'$R_Q$',.04)):
    arr=(0.5, src[1]+abs(src[0]-0.5))
    ax.plot([src[0],arr[0]],[src[1],arr[1]],':',color=C_AUX,lw=LW_RAY,zorder=2)
    ax.plot(*arr,'s',color=C_ARR,ms=MS_ARR,zorder=7)
    ax.text(arr[0]-.50,arr[1]+dy,lab,color=C_ARR,fontsize=FS_ANNOT)
fig.tight_layout(w_pad=1.2)
fig.savefig('fig2.png',dpi=200); fig.savefig('fig2.pdf'); plt.close(fig)

# ---- FIG 3: one factor of k ----------------------------------------------
b=0.5; g=1/np.sqrt(1-b**2); Dp=1.4; k=np.sqrt((1+b)/(1-b))
fig,ax=plt.subplots(figsize=(3.35,2.40))
frame(ax,(-1.05,4.3),(0.75,5.40))
ax.plot([0,0],[0.75,5.40],'-',color=C_RES,lw=LW_WORLD); ax.text(-0.10,5.12,'acceptor',color=C_RES,fontsize=FS_ANNOT,ha='right')
t=np.array([0.8,5.35]); ax.plot(0.35+b*(t-0.3),t,color=C_OLD,lw=LW_WORLD)
ax.text(2.58,4.30,'proposer',color=C_OLD,fontsize=FS_ANNOT)
t1=1.2; t2=t1+g*Dp
p1=(0.35+b*(t1-0.3),t1); p2=(0.35+b*(t2-0.3),t2)
for p in (p1,p2): ax.plot(*p,'o',color=C_OLD,ms=MS_EVENT,zorder=6)
off=0.30
ax.annotate('',xy=(p2[0]+off,p2[1]-off*0.25),xytext=(p1[0]+off,p1[1]-off*0.25),
            arrowprops=dict(arrowstyle='<->',color=C_OLD,lw=LW_ARROW))
ax.text(p2[0]+off+.10,(p1[1]+p2[1])/2-.30,'$D_P$ proper',color=C_OLD,fontsize=FS_ANNOT)
a1,a2=t1+p1[0],t2+p2[0]
for p,a in ((p1,a1),(p2,a2)):
    ax.plot([p[0],0],[p[1],a],':',color=C_AUX,lw=LW_RAY); ax.plot(0,a,'s',color=C_ARR,ms=MS_ARR,zorder=7)
ax.annotate('',xy=(-0.17,a2),xytext=(-0.17,a1),arrowprops=dict(arrowstyle='<->',color=C_ARR,lw=LW_ARROW))
ax.text(-0.44,(a1+a2)/2,'$k\\,D_P$',color=C_ARR,fontsize=FS_EVENT,rotation=90,va='center')
# gamma*D_P, the proposer's timer dilated into the acceptor's frame, timed from
# the same start as the exclusion (no earlier than light from Prepare arrives,
# since the Accept follows it): it ends beta*gamma*D_P before light from P arrives
ag=a1+g*Dp
ax.annotate('',xy=(-0.66,ag),xytext=(-0.66,a1),arrowprops=dict(arrowstyle='<->',color=C_AUX,lw=LW_ARROW))
ax.plot([-0.74,-0.02],[ag,ag],':',color=C_AUX,lw=LW_RAY)
ax.text(-0.93,(a1+ag)/2,'$\\gamma\\,D_P$',color=C_AUX,fontsize=FS_EVENT,rotation=90,va='center')
# in that gap an acquisition beside the acceptor is spacelike to the expiry P
ax.plot([0,0],[ag,a2],'-',color=C_OVL,lw=LW_LEASE*1.6,alpha=.85,zorder=5,solid_capstyle='butt')
ym=(ag+a2)/2
ax.text(0.34,5.12,'an acquisition here\nis spacelike to $P$',color=C_OVL,fontsize=FS_ANNOT,ha='left',va='center')
ax.annotate('',xy=(0.06,ym+0.08),xytext=(0.45,4.86),arrowprops=dict(arrowstyle='-|>',color=C_OVL,lw=LW_ARROW))
ax.text(p2[0]+0.12,p2[1]-0.05,'$P$',color=C_OLD,fontsize=FS_EVENT)
ax.annotate('',xy=(0.22,a2+0.5),xytext=(0.22,a1),arrowprops=dict(arrowstyle='<->',color=C_NEW,lw=LW_ARROW))
ax.text(0.30,2.45,'$D_A$',color=C_NEW,fontsize=FS_EVENT)
fig.tight_layout(); fig.savefig('fig3.png',dpi=200); fig.savefig('fig3.pdf'); plt.close(fig)

# ---- FIG 2: how classical PaxosLease acquires a lease -----------------------
# A message-sequence diagram, not a spacetime diagram: time runs up, horizontal
# position only separates the participants, and every message arrow is level so
# that no arrow can be read as a trajectory.
fig,ax=plt.subplots(figsize=(3.35,2.25))
P,A=0.0,(1.60,2.40,3.20)
TOP=3.85
ax.set_xlim(-1.62,4.85); ax.set_ylim(-0.10,TOP+0.55)
ax.set_xticks([]); ax.set_yticks([])
for sp in ('top','right','left','bottom'): ax.spines[sp].set_visible(False)
axis_arrow(ax,(-1.26,0.0),(-1.26,TOP+0.40),'black')
ax.text(-1.52,TOP*0.55,'time',color='black',fontsize=FS_AXIS,rotation=90,va='center')
for x,lab,c in [(P,'proposer',C_OLD)]+[(A[i],'acceptor %d'%(i+1),C_ARR) for i in range(3)]:
    ax.plot([x,x],[0.0,TOP],'-',color=c,lw=LW_WORLD)
    ax.text(x,TOP+0.12,lab,color=c,fontsize=FS_ANNOT,ha='center')
def arrow(t,x0,x1,c):
    ax.annotate('',xy=(x1,t),xytext=(x0,t),
                arrowprops=dict(arrowstyle='-|>',color=c,lw=LW_ARROW,shrinkA=1.5,shrinkB=1.5))
def group(t0,out,c,lab):
    for i,x in enumerate(A):
        t=t0+0.10*i
        arrow(t,P,x,c) if out else arrow(t,x,P,c)
    ax.text(3.62,t0-0.02,lab,color=c,fontsize=FS_ANNOT,ha='left',va='bottom')
def mark(t,lab):
    ax.plot(P,t,'o',color=C_OLD,ms=MS_EVENT,zorder=6)
    ax.text(P-0.26,t,lab,color=C_OLD,fontsize=FS_ANNOT,ha='right',va='center')
ax.plot(P,0.35,'*',color=C_OLD,ms=MS_EVENT*2.1,zorder=7)
ax.text(P-0.26,0.35,'$D_P$ starts',color=C_OLD,fontsize=FS_ANNOT,ha='right',va='center')
group(0.35,True ,C_OLD,'Prepare')
group(0.70,False,C_ARR,'promises')
mark(0.80,'majority')
group(1.35,True ,C_OLD,'Accept')
group(1.70,False,C_ARR,'acceptances')
mark(1.80,'acquired')
ax.plot([P-0.07,P+0.07],[2.45,2.45],'-',color=C_OLD,lw=LW_ARROW)
ax.text(P-0.26,2.45,'expires',color=C_OLD,fontsize=FS_ANNOT,ha='right',va='center')
ax.annotate('',xy=(P+0.22,2.45),xytext=(P+0.22,0.35),
            arrowprops=dict(arrowstyle='<->',color=C_OLD,lw=LW_ARROW))
ax.text(P+0.29,2.17,'$D_P$',color=C_OLD,fontsize=FS_EVENT,rotation=90,va='center')
for i,x in enumerate(A):
    ax.plot(x,1.35+0.10*i,'*',color=C_ARR,ms=MS_EVENT*2.1,zorder=7)
ax.text(A[0]-0.08,1.20,'$D_A$ starts',color=C_ARR,fontsize=FS_ANNOT,ha='right',va='top')
for i,x in enumerate(A):
    ax.annotate('',xy=(x+0.14,3.55+0.10*i),xytext=(x+0.14,1.35+0.10*i),
                arrowprops=dict(arrowstyle='<->',color=C_ARR,lw=LW_ARROW))
ax.text(A[0]+0.20,2.20,'$D_A$',color=C_ARR,fontsize=FS_EVENT,rotation=90,va='center')
ax.axhspan(2.45,3.55,xmin=0.05,xmax=0.79,color=C_ARR,alpha=0.09,lw=0,zorder=0)
ax.text(1.35,3.00,"the proposer's lease timer has expired, but\nthe acceptors' timers have not, so no other\nproposer can acquire the lease here.",
        color=C_ARR,fontsize=FS_ANNOT,ha='center',va='center',linespacing=1.4,bbox=BOX,zorder=8)
fig.tight_layout()
fig.savefig('figseq.png',dpi=200); fig.savefig('figseq.pdf'); plt.close(fig)
