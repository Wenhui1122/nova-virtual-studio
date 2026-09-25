"""Build a studio asset pack and a self-contained MAXScript. Z up, centimetres.
No third-party models. Preview renderer requires NumPy and Pillow only.
"""
from pathlib import Path
import math, json, zipfile
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
nodes=[]
MATS={
 'Floor':('#202a38',0),'Stage':('#354658',0),'White':('#d6e0df',0),
 'Metal':('#778992',0),'Dark':('#101a2a',0),'Screen':('#143354',15),
 'Cyan':('#43d7db',70),'Warm':('#c9a77c',0),'Glass':('#3a6980',0),
 'Light':('#fff1cd',90)}

def add(name,verts,faces,mat,layer):
    nodes.append(dict(name=name,v=np.array(verts,float),f=np.array(faces,int),mat=mat,layer=layer))

def box(name,pos,size,mat,layer,angle=0):
    x,y,z=size; v=np.array([[-x,-y,-z],[x,-y,-z],[x,y,-z],[-x,y,-z],[-x,-y,z],[x,-y,z],[x,y,z],[-x,y,z]])/2
    a=math.radians(angle);rot=np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
    v=v@rot.T+pos
    f=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),(1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
    add(name,v,f,mat,layer)

def extrude(name,poly,z0,z1,mat,layer,scale_top=1):
    # convex planar contour, CCW viewed from above
    poly=np.array(poly);n=len(poly);center=poly.mean(axis=0)
    upper=center+(poly-center)*scale_top
    v=[(*p,z0) for p in poly]+[(*p,z1) for p in upper]
    f=[]
    for i in range(1,n-1):f.extend([(0,i+1,i),(n,n+i,n+i+1)])
    for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j),(i,n+j,n+i)])
    add(name,v,f,mat,layer)

def ellipse(name,c,rx,ry,z0,z1,mat,layer,n=64):
    extrude(name,[(c[0]+rx*math.cos(i*2*math.pi/n),c[1]+ry*math.sin(i*2*math.pi/n)) for i in range(n)],z0,z1,mat,layer)

def beam(name,a,b,r,mat,layer,n=10):
    a=np.array(a,float);b=np.array(b,float);axis=b-a;axis/=np.linalg.norm(axis)
    helper=np.array([0,0,1]) if abs(axis[2])<.9 else np.array([1,0,0])
    u=np.cross(helper,axis);u/=np.linalg.norm(u);w=np.cross(axis,u)
    verts=[p+r*(u*math.cos(i*2*math.pi/n)+w*math.sin(i*2*math.pi/n)) for p in (a,b) for i in range(n)]
    faces=[]
    for i in range(1,n-1):faces.extend([(0,i+1,i),(n,n+i,n+i+1)])
    for i in range(n):j=(i+1)%n;faces.extend([(i,j,n+j),(i,n+j,n+i)])
    add(name,verts,faces,mat,layer)

def arc(name,r0,r1,a0,a1,z0,z1,mat,layer,n=12):
    angles=np.linspace(math.radians(a0),math.radians(a1),n+1)
    v=[(r*math.cos(a),r*math.sin(a),z) for z in (z0,z1) for r in (r0,r1) for a in angles]
    k=n+1;f=[]
    for i in range(n):
        for a,b,c,d in ((i,i+1,2*k+i+1,2*k+i),(k+i,3*k+i,3*k+i+1,k+i+1),
                         (i,k+i,k+i+1,i+1),(2*k+i,2*k+i+1,3*k+i+1,3*k+i)):
            f.extend([(a,b,c),(a,c,d)])
    f.extend([(0,2*k,3*k),(0,3*k,k),(n,k+n,3*k+n),(n,3*k+n,2*k+n)])
    add(name,v,[tuple(reversed(t)) for t in f],mat,layer)

def rounded_rect(cx,cy,w,h,r,n=8):
    out=[]
    for x,y,start in ((cx+w/2-r,cy+h/2-r,0),(cx-w/2+r,cy+h/2-r,90),
                       (cx-w/2+r,cy-h/2+r,180),(cx+w/2-r,cy-h/2+r,270)):
        for a in np.linspace(start,start+90,n,endpoint=False):
            a=math.radians(a);out.append((x+r*math.cos(a),y+r*math.sin(a)))
    return out

def build():
    box('Floor foundation',(0,0,-10),(1400,1100,20),'Floor','01_Architecture')
    for x in range(-600,701,100):box('Floor seam X '+str(x),(x,0,.2),(1,1100,.3),'Stage','01_Architecture')
    for y in range(-500,501,100):box('Floor seam Y '+str(y),(0,y,.2),(1400,1,.3),'Stage','01_Architecture')
    ellipse('Stage lower step',(0,50),510,325,0,14,'Stage','02_Stage')
    ellipse('Stage luminous rim',(0,50),478,294,14,18,'Cyan','02_Stage')
    ellipse('Stage upper deck',(0,50),474,290,18,35,'Dark','02_Stage')
    ellipse('Presenter zone',(0,15),245,158,35,38,'Stage','02_Stage')
    for i in range(18):
        a=29+i*122/18;b=29+(i+1)*122/18-.5
        arc(f'LED wall segment {i+1:02}',430,442,a,b,40,355,'Screen','03_LED_Wall',4)
    for z in (40,356):arc('LED border '+str(z),428,444,28,152,z,z+5,'Cyan','03_LED_Wall',60)
    # Vertical graphic bars follow the screen curvature.
    for i in range(31):
        a=33+i*3.8;height=40+42*(1+math.sin(i*.63))
        arc('Screen data bar '+str(i),428,429,a,a+.5,65,65+height,'Cyan','04_Screen_Graphics',1)
    for x in (-500,500):
        box('Acoustic tower '+str(x),(x,220,200),(55,75,400),'Dark','01_Architecture')
        for z in range(45,390,28):box('Tower fin '+str(x)+' '+str(z),(x,176,z),(68,15,8),'Metal','01_Architecture')
        box('Tower accent '+str(x),(x-20,165,210),(4,4,345),'Warm','01_Architecture')
    # Three nested rounded profiles make the desk a separate editable assembly.
    extrude('Desk recessed plinth',rounded_rect(0,-35,265,88,30),38,51,'Dark','05_Anchor_Desk')
    extrude('Desk tapered body',rounded_rect(0,-35,290,95,34),51,126,'White','05_Anchor_Desk',1.10)
    extrude('Desk top illuminated edge',rounded_rect(0,-35,331,113,39),126,130,'Cyan','05_Anchor_Desk')
    extrude('Desk worktop',rounded_rect(0,-35,337,117,41),130,139,'Dark','05_Anchor_Desk')
    box('Desk front inset',(0,-86,91),(172,3,43),'Screen','05_Anchor_Desk')
    for x in (-76,76):box('Desk inset trim '+str(x),(x,-89,91),(3,3,32),'Cyan','05_Anchor_Desk')
    for x in (-65,65):
        box('Monitor base '+str(x),(x,-21,143),(34,24,6),'Metal','06_Props')
        box('Monitor support '+str(x),(x,-15,158),(5,6,26),'Metal','06_Props')
        box('Monitor housing '+str(x),(x,-15,179),(56,9,34),'Dark','06_Props')
        box('Monitor display '+str(x),(x,-20,179),(51,1,29),'Glass','06_Props')
    # Truss with four chords and alternating diagonal braces.
    for y in (-120,220):
        for dy in (-13,13):
            for z in (414,440):beam('Truss chord',(-530,y+dy,z),(530,y+dy,z),3,'Metal','07_Lighting_Rig')
        for i in range(20):
            x=-530+i*53
            for dy in (-13,13):beam('Truss diagonal',(x,y+dy,414),(x+53,y+dy,440),1.8,'Metal','07_Lighting_Rig')
        for x in (-380,-190,0,190,380):
            beam('Lamp hanger',(x,y,414),(x,y,386),3,'Dark','07_Lighting_Rig')
            box('Studio softbox',(x,y,378),(58,46,18),'Dark','07_Lighting_Rig')
            box('Softbox diffuser',(x,y,368),(50,39,2),'Light','07_Lighting_Rig')
    for x,y in ((-350,-325),(350,-325)):
        for dx,dy in ((-32,-24),(32,-24),(0,38)):
            beam('Camera tripod',(x+dx,y+dy,3),(x,y,128),3,'Metal','08_Camera_Props')
        beam('Camera pedestal',(x,y,105),(x,y,153),7,'Dark','08_Camera_Props')
        box('Broadcast camera body',(x,y,169),(35,57,30),'Dark','08_Camera_Props')
        beam('Camera lens',(x,y+26,169),(x,y+51,169),11,'Dark','08_Camera_Props',24)
        beam('Camera lens glass',(x,y+51,169),(x,y+52,169),9,'Glass','08_Camera_Props',24)
        box('Camera handle',(x,y,192),(7,28,5),'Metal','08_Camera_Props')
    # Physical block-letter geometry on a central signage panel.
    box('Central identity panel',(0,413,265),(305,6,102),'Dark','04_Screen_Graphics')
    glyph={'N':['10001','11001','10101','10011','10001'],
           'O':['01110','10001','10001','10001','01110'],
           'V':['10001','10001','10001','01010','00100'],
           'A':['01110','10001','11111','10001','10001']}
    for c,char in enumerate('NOVA'):
        for r,row in enumerate(glyph[char]):
            for col,on in enumerate(row):
                if on=='1':box('Identity letter '+char,(-105+c*58+col*10,408,287-r*11),(9,3,10),'White','04_Screen_Graphics')
    box('Identity underline',(0,408,224),(232,3,3),'Cyan','04_Screen_Graphics')

def validate():
    report=[]
    for node in nodes:
        v,f=node['v'],node['f'];assert np.isfinite(v).all() and f.min()>=0 and f.max()<len(v)
        xyz=v[f];norm=np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]);assert (np.linalg.norm(norm,axis=1)>1e-7).all(),node['name']
        edges=Counter(tuple(sorted((int(a),int(b)))) for tri in f for a,b in zip(tri,np.roll(tri,-1)))
        assert all(n==2 for n in edges.values()),node['name']
        directed=Counter((int(a),int(b)) for tri in f for a,b in zip(tri,np.roll(tri,-1)))
        assert all(count==directed[(b,a)] for (a,b),count in directed.items()),node['name']
        vol=np.einsum('ij,ij->i',xyz[:,0],np.cross(xyz[:,1],xyz[:,2])).sum()/6
        assert vol>0,(node['name'],vol)
    return dict(objects=len(nodes),vertices=sum(len(n['v']) for n in nodes),triangles=sum(len(n['f']) for n in nodes),
                checks=['finite coordinates','valid indices','nondegenerate faces','closed edge topology','positive signed volume'],
                max_runtime_tested=False)

def export():
    obj=['# NOVA virtual studio | centimetres | Z up','mtllib NovaStudio.mtl'];offset=1
    for index,n in enumerate(nodes):
        obj.extend(['o '+n['name'].replace(' ','_')+'_'+str(index),'usemtl '+n['mat']])
        obj.extend('v '+' '.join(f'{x:.5f}' for x in p) for p in n['v'])
        obj.extend('f '+' '.join(str(int(x)+offset) for x in f) for f in n['f']);offset+=len(n['v'])
    (ROOT/'Models/NovaStudio.obj').write_text('\n'.join(obj)+'\n')
    mtl=[]
    for name,(color,emit) in MATS.items():
        rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
        mtl.extend(['newmtl '+name,'Kd '+' '.join(map(str,rgb)),'Ks 0.2 0.2 0.2','Ns 32',''])
    (ROOT/'Models/NovaStudio.mtl').write_text('\n'.join(mtl))
    ms=['/* NOVA studio | centimetres | generated geometry | no external dependencies. */',
        '(', 'if objects.count > 0 then (messageBox "Please open a new empty scene before running this script. Your scene has not been changed." title:"NOVA Studio") else (',
        'units.SystemType = #centimeters','units.SystemScale = 1.0','units.DisplayType = #metric','units.MetricType = #centimeters',
        'local studioMaterials = #()','local studioNodes = #()', 'local studioLayer = undefined']
    for name,(color,emit) in MATS.items():
        rgb=[int(color[i:i+2],16) for i in (1,3,5)]
        ms.append(f'append studioMaterials (standardMaterial name:"NOVA_{name}" diffuse:(color {rgb[0]} {rgb[1]} {rgb[2]}) specularLevel:25 glossiness:35 selfIllumAmount:{emit})')
    layers=sorted({n['layer'] for n in nodes})
    for layer in layers:ms.append(f'if (LayerManager.getLayerFromName "{layer}") == undefined do LayerManager.newLayerFromName "{layer}"')
    def pt(p):return '['+','.join(f'{float(x):.5f}' for x in p)+']'
    for index,n in enumerate(nodes):
        name=n['name']+' '+str(index+1)
        ms.extend(['(', 'local verts = #('+','.join(pt(v) for v in n['v'])+')',
            'local faces = #('+','.join('['+','.join(str(int(i)+1) for i in f)+']' for f in n['f'])+')',
            f'local item = mesh name:"{name}" vertices:verts faces:faces',
            f'item.material = studioMaterials[{list(MATS).index(n["mat"])+1}]',
            'item.wirecolor = item.material.diffuse','update item','convertToPoly item',
            f'studioLayer = LayerManager.getLayerFromName "{n["layer"]}"','studioLayer.addNode item','append studioNodes item',')'])
    ms.extend(['local cam = targetCamera name:"NOVA Main Camera" pos:[820,-1180,690] target:(targetObject pos:[0,65,155])',
        'cam.fov = 48','local frontCam = targetCamera name:"NOVA Presenter Camera" pos:[0,-1050,260] target:(targetObject pos:[0,60,175])','frontCam.fov = 50',
        'local keyLight = omniLight name:"NOVA Key" pos:[-300,-300,600] multiplier:1.0 color:(color 232 242 255)',
        'local fillLight = omniLight name:"NOVA Fill" pos:[400,-50,430] multiplier:0.55 color:(color 180 220 255)',
        'local backLight = omniLight name:"NOVA Back" pos:[0,360,450] multiplier:0.65 color:(color 255 225 180)',
        'renderers.current = Default_Scanline_Renderer()','renderWidth = 1920','renderHeight = 1080',
        'backgroundColor = color 15 21 31','viewport.setCamera cam','completeRedraw()',
        'messageBox "NOVA Studio created. All geometry is editable and organized into 8 layers. Use File > Save As to create NovaStudio.max. Press F9 for a draft render. This script has not been runtime-tested in 3ds Max." title:"NOVA Studio"',')',')'])
    (ROOT/'Scripts/Build_NovaStudio.ms').write_text('\n'.join(ms),encoding='utf8')

def font(size,bold=False):
    candidates=[
        '/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',
        'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',
        'arialbd.ttf' if bold else 'arial.ttf',
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate,size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)

def render(path,eye,target,wire=False):
    W,H=1800,1120;canvas=np.zeros((H,W,3),dtype=np.uint8);canvas[:]=[231,236,239]
    zbuf=np.full((H,W),np.inf)
    eye=np.array(eye,float);target=np.array(target,float);forward=target-eye;forward/=np.linalg.norm(forward)
    right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,forward)
    view=np.stack([right,up,forward],axis=1);focal=1400
    light=np.array([-.4,-.6,1.]);light/=np.linalg.norm(light)
    for n in nodes:
        verts=(n['v']-eye)@view
        p=np.column_stack([W/2+focal*verts[:,0]/verts[:,2],H/2-focal*verts[:,1]/verts[:,2]-5])
        color,emit=MATS[n['mat']];base=np.array([int(color[i:i+2],16) for i in (1,3,5)])
        for face in n['f']:
            xyz=n['v'][face];normal=np.cross(xyz[1]-xyz[0],xyz[2]-xyz[0]);normal/=np.linalg.norm(normal)
            if np.dot(normal,eye-xyz.mean(axis=0))<=0:continue
            tri=p[face];depth=verts[face,2]
            if min(depth)<=1:continue
            xmin=max(0,int(np.floor(tri[:,0].min())));xmax=min(W-1,int(np.ceil(tri[:,0].max())))
            ymin=max(150,int(np.floor(tri[:,1].min())));ymax=min(H-72,int(np.ceil(tri[:,1].max())))
            if xmin>xmax or ymin>ymax:continue
            xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
            a,b,c=tri;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-10:continue
            w0=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
            w1=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;w2=1-w0-w1
            mask=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
            dz=1/(w0/depth[0]+w1/depth[1]+w2/depth[2]);sl=np.s_[ymin:ymax+1,xmin:xmax+1]
            mask &= dz<zbuf[sl]
            shade=max(.42+.58*max(0,np.dot(normal,light)),emit/100)
            rgb=np.clip(base*shade,0,255).astype(np.uint8)
            canvas[sl][mask]=rgb;zbuf[sl][mask]=dz[mask]
            if wire:
                lengths=[np.linalg.norm(b-c),np.linalg.norm(c-a),np.linalg.norm(a-b)]
                edge=np.minimum.reduce([w0*abs(den)/lengths[0],w1*abs(den)/lengths[1],w2*abs(den)/lengths[2]])<.6
                canvas[sl][mask & edge]=[86,155,165]
    im=Image.fromarray(canvas);d=ImageDraw.Draw(im)
    d.text((60,40),'NOVA / VIRTUAL STUDIO',font=font(42,True),fill='#1d2d40')
    d.text((62,99),'EDITABLE SCENE STUDY  /  '+('MESH TOPOLOGY' if wire else 'SPACE, FORM & LIGHT'),font=font(18),fill='#657786')
    d.text((60,H-49),'PROJECT GEOMETRY PREVIEW  |  Independent software render — not a 3ds Max screenshot',font=font(17),fill='#657786')
    im.save(path)

if __name__=='__main__':
    build();report=validate();export()
    (ROOT/'Documentation/validation.json').write_text(json.dumps(report,indent=2))
    render(ROOT/'Preview/01_Studio_Overview.png',(1120,-1600,1000),(0,60,175))
    render(ROOT/'Preview/02_Studio_Front.png',(0,-1750,670),(0,80,180))
    render(ROOT/'Preview/03_Topology.png',(1120,-1600,1000),(0,60,175),True)
    print(json.dumps(report,indent=2))
