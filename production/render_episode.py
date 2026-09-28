import json, math, os, sys
from pathlib import Path
import bpy

def M(name, c):
    m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); return m
def K(o,f,loc=None,rot=None,scale=None):
    if loc is not None:o.location=loc;o.keyframe_insert("location",frame=f)
    if rot is not None:o.rotation_euler=rot;o.keyframe_insert("rotation_euler",frame=f)
    if scale is not None:o.scale=scale;o.keyframe_insert("scale",frame=f)
def cube(n,p,s,m,parent=None,b=.12):
    bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.scale=s
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    x=o.modifiers.new("soft","BEVEL");x.width=b;x.segments=3;o.data.materials.append(m);o.parent=parent;return o
def ball(n,p,s,m,parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=p)
    o=bpy.context.object;o.name=n;o.scale=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(m);o.parent=parent
    for face in o.data.polygons:face.use_smooth=True
    return o
def cyl(n,p,r,d,m,parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=d,location=p)
    o=bpy.context.object;o.name=n;o.data.materials.append(m);o.parent=parent
    bevel=o.modifiers.new("rounded ends","BEVEL");bevel.width=.12;bevel.segments=3
    o.modifiers.new("weighted normals","WEIGHTED_NORMAL")
    return o
def pivot(n,p,parent):
    o=bpy.data.objects.new(n,None);bpy.context.collection.objects.link(o)
    o.parent=parent;o.location=p
    return o

def child(name,x,y,shirt,hair,style,skin,dark):
    root=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(root);root.location=(x,y,0)
    sm=M(name+" shirt",shirt); hm=M(name+" hair",hair); pants=M(name+" pants",(.12,.28,.48))
    shoes=M(name+" shoes",(.16,.1,.07))
    ball(name+" shirt body",(0,0,1.88),(.46,.32,.64),sm,root)
    ball(name+" neck",(0,0,2.52),(.18,.17,.18),skin,root)
    ball(name+" head",(0,-.03,3.02),(.49,.43,.55),skin,root)
    for side in (-1,1):
        ball(name+f" ear{side}",(side*.49,-.015,3.01),(.095,.07,.15),skin,root)
    if style=="curls":
        for i,px in enumerate((-.37,-.18,0,.18,.37)):
            ball(name+f" curl{i}",(px,.025,3.52-abs(px)*.12),(.16,.19,.16),hm,root)
        ball(name+" back hair",(0,.2,3.13),(.47,.27,.42),hm,root)
    else:
        ball(name+" hair crown",(0,.12,3.43),(.48,.39,.22),hm,root)
        ball(name+" side fringe",(-.25,-.29,3.43),(.26,.12,.12),hm,root)
        if style=="pony":
            ball(name+" ponytail",(.43,.23,3.08),(.17,.18,.32),hm,root)
            ball(name+" hair tie",(.47,.23,3.31),(.12,.12,.08),M(name+" hair tie mat",shirt),root)
    white=M(name+" whites",(1,.98,.92)); mouthmat=M(name+" mouth",(.45,.04,.08))
    for side in (-1,1):
        ball(name+f" eye{side}",(side*.18,-.425,3.10),(.068,.03,.085),white,root)
        ball(name+f" pupil{side}",(side*.18,-.463,3.09),(.032,.015,.05),dark,root)
        ball(name+f" eyebrow{side}",(side*.18,-.422,3.32),(.10,.012,.018),hm,root)
        ball(name+f" cheek{side}",(side*.30,-.382,2.91),(.07,.015,.03),M(name+f" blush{side}",(.78,.38,.32)),root)
    ball(name+" nose",(0,-.46,3.02),(.055,.055,.05),skin,root)
    mouth=ball(name+" talking mouth",(0,-.449,2.84),(.085,.013,.025),mouthmat,root)
    arms=[];legs=[]
    for side in (-1,1):
        a=pivot(name+f" shoulder{side}",(side*.46,0,2.28),root)
        ball(name+f" sleeve{side}",(side*.015,0,-.10),(.23,.22,.29),sm,a)
        ball(name+f" arm{side}",(side*.015,0,-.40),(.13,.13,.30),skin,a)
        ball(name+f" hand{side}",(side*.015,0,-.66),(.14,.13,.16),skin,a)
        arms.append(a)
        l=pivot(name+f" hip{side}",(side*.22,0,1.39),root)
        ball(name+f" pantleg{side}",(0,0,-.52),(.20,.20,.58),pants,l)
        ball(name+f" shoe{side}",(0,-.13,-1.07),(.24,.34,.15),shoes,l)
        legs.append(l)
    ball(name+" backpack",(0,.31,1.94),(.36,.15,.45),M(name+" pack",(.66,.28,.1)),root)
    for side in (-1,1):
        ball(name+f" pack strap{side}",(side*.31,-.22,2.05),(.075,.07,.39),M(name+f" strap mat{side}",(.44,.2,.08)),root)
    return dict(root=root,mouth=mouth,arms=arms,legs=legs)

def bear(skin,dark):
    r=bpy.data.objects.new("Benji bear",None);bpy.context.collection.objects.link(r);fur=M("bear fur",(.34,.15,.06))
    ball("bear body",(0,0,1.7),(1.1,.78,1.35),fur,r);ball("bear head",(0,-.05,3.18),(.9,.7,.82),fur,r)
    for side in (-1,1):
        ball("bear ear",(side*.64,0,3.8),(.31,.22,.32),fur,r);ball("bear eye",(side*.28,-.7,3.32),(.08,.04,.11),dark,r)
        cyl("bear leg",(side*.53,0,.55),.31,1.1,fur,r)
    ball("bear muzzle",(0,-.68,3.02),(.43,.25,.3),M("muzzle",(.65,.38,.18)),r);ball("bear nose",(0,-.89,3.13),(.16,.1,.12),dark,r)
    arm=cyl("bear wave arm",(.9,0,2.2),.26,1.35,fur,r);arm.rotation_euler[1]=math.radians(-25)
    return dict(root=r,arm=arm)

def world():
    cube("ground",(0,12,-.22),(14,34,.2),M("grass",(.08,.45,.16)),b=.03)
    trail=M("continuous earth trail",(.52,.35,.19))
    verts=[];faces=[]
    for i in range(45):
        y=-7+i*.8;center=math.sin((y+6)*.18)*.65
        verts.extend([(center-1.5,y,.016),(center+1.5,y,.016)])
        if i:faces.append((2*i-2,2*i-1,2*i+1,2*i))
    mesh=bpy.data.meshes.new("curving trail mesh");mesh.from_pydata(verts,[],faces);mesh.update()
    path=bpy.data.objects.new("continuous forest path",mesh);bpy.context.collection.objects.link(path);mesh.materials.append(trail)
    for f in mesh.polygons:f.use_smooth=True
    bark=M("bark",(.27,.12,.04));leaf=M("leaves",(.04,.34,.1))
    for i in range(24):
        side=-1 if i%2==0 else 1;y=-5+(i//2)*3.4;x=side*(4.2+(i%3)*.5)
        cyl("tree",(x,y,1.7),.28,3.4,bark);ball("canopy",(x,y,4),(1.2,.95,1.3),leaf)
    mud=M("tracks",(.23,.12,.06))
    for i in range(9):
        x=math.sin(i*.5)*.5;y=i*1.6+.5;ball("paw pad",(x,y,.08),(.32,.45,.04),mud)
        for toe in (-.23,0,.23):ball("paw toe",(x+toe,y-.38,.085),(.11,.14,.035),mud)
    bush=M("bush",(.03,.3,.08));berry=M("berries",(.5,.03,.12))
    for x in (2.2,3.3,4.4):
        ball("berry bush",(x,12,1),(1,.7,1),bush)
        for q in range(3):ball("berry",(x-.3+q*.3,11.35,1.1+(q%2)*.25),(.09,.07,.09),berry)

def walk(p,a,b,y1,y2,fps):
    r=p["root"];step=max(3,int(fps*.27))
    for f in sorted(set(list(range(a,b+1,step))+[b])):
        ph=((f-a)//step)%2
        progress=(f-a)/max(1,b-a)
        r.location=(r.location.x,y1+(y2-y1)*progress,.035 if ph else 0)
        r.keyframe_insert("location",frame=f)
        for j,o in enumerate(p["legs"]):o.rotation_euler[0]=math.radians(18 if (ph+j)%2 else -18);o.keyframe_insert("rotation_euler",frame=f)
        for j,o in enumerate(p["arms"]):o.rotation_euler[0]=math.radians(-18 if (ph+j)%2 else 18);o.keyframe_insert("rotation_euler",frame=f)
def talk(p,start,dur,fps):
    a=int(start*fps);b=int((start+dur)*fps);step=max(2,int(fps*.12))
    for f in range(a,b+1,step):K(p["mouth"],f,scale=(1,1,2 if ((f-a)//step)%2 else .6))

def animate(P,B,t,fps):
    for n,off,x in (("Luke",0,-1.1),("Lydia",-.7,0),("Poppy",-1.4,1.1)):
        walk(P[n],1,int(12*fps),-5+off,1.5+off,fps);walk(P[n],int(13*fps),int(34*fps),1.5+off,9+off,fps)
    # Point to the tracks, kneel, and react.
    K(P["Poppy"]["arms"][1],int(2*fps),rot=(math.radians(-55),0,math.radians(-35)));K(P["Poppy"]["arms"][1],int(5*fps),rot=(0,0,0))
    K(P["Lydia"]["root"],int(5*fps),scale=(1,1,1));K(P["Lydia"]["root"],int(7*fps),scale=(1,1,.7));K(P["Lydia"]["root"],int(10*fps),scale=(1,1,1))
    end=int(t["duration"]*fps);reveal=min(end-4*fps,int(41*fps))
    K(B["root"],1,(3.4,13,0),scale=(.01,.01,.01));K(B["root"],reveal-fps,(3.4,13,0),scale=(.01,.01,.01));K(B["root"],reveal+fps,(3,11.2,0),scale=(1,1,1))
    K(B["arm"],reveal+fps,rot=(0,math.radians(-25),0));K(B["arm"],reveal+2*fps,rot=(math.radians(30),math.radians(-55),math.radians(-15)));K(B["arm"],reveal+3*fps,rot=(math.radians(-20),math.radians(-55),math.radians(15)))
    for line in t["lines"]:
        if line["speaker"] in P:talk(P[line["speaker"]],line["start"],line["duration"],fps)

def camera(duration,fps):
    bpy.ops.object.camera_add(location=(0,-13,5.4));c=bpy.context.object;c.data.lens=43;bpy.context.scene.camera=c
    target=bpy.data.objects.new("camera target",None);bpy.context.collection.objects.link(target)
    q=c.constraints.new("TRACK_TO");q.target=target;q.track_axis="TRACK_NEGATIVE_Z";q.up_axis="UP_Y"
    shots=[(1,(0,-13,5.4),(0,-2,2.2)),(10*fps,(-2,-7,3),(0,1,.2)),(17*fps,(3,-4,4),(0,4,2.2)),(30*fps,(-3,1,3.2),(0,8,.3)),(41*fps,(0,2,5),(2,11,2.4)),(duration*fps,(0,1,5.7),(0,9,2.4))]
    for f,cp,tp in shots:K(c,int(f),cp);K(target,int(f),tp)

def main():
    ep=json.loads(Path(sys.argv[sys.argv.index("--")+1]).read_text());t=json.loads(Path("build/timeline.json").read_text())
    bpy.ops.wm.read_factory_settings(use_empty=True);skin=M("skin",(.95,.66,.47));dark=M("eyes",(.015,.012,.012));world()
    P={"Luke":child("Luke",-1.1,-5,(.04,.36,.75),(.24,.1,.04),"swept",skin,dark),"Lydia":child("Lydia",0,-5.7,(.86,.15,.45),(.12,.05,.03),"pony",skin,dark),"Poppy":child("Poppy",1.1,-6.4,(1,.57,.03),(.55,.2,.04),"curls",skin,dark)}
    B=bear(skin,dark);fps=ep.get("fps",24);animate(P,B,t,fps);camera(t["duration"],fps)
    s=bpy.context.scene;s.sequence_editor_create()
    for i,line in enumerate(t["lines"]):s.sequence_editor.sequences.new_sound(f"voice{i}",line["audio"],1,int(line["start"]*fps)+1)
    bpy.ops.object.light_add(type="SUN",location=(4,-4,12));bpy.context.object.data.energy=2.2
    bpy.ops.object.light_add(type="AREA",location=(-4,-4,9));bpy.context.object.data.energy=900;bpy.context.object.data.size=7
    if s.world is None:s.world=bpy.data.worlds.new("Episode World")
    s.world.color=(.16,.43,.7);s.render.engine="BLENDER_EEVEE";s.eevee.use_gtao=True;s.eevee.gtao_factor=.55
    s.render.resolution_x,s.render.resolution_y=ep.get("resolution",[1080,1920]);s.render.resolution_percentage=50;s.render.fps=fps;s.frame_start=1;s.frame_end=int(t["duration"]*fps)
    sample=os.environ.get("SAMPLE_FRAME")
    if sample:
        s.frame_set(int(sample));s.render.resolution_percentage=35
        s.render.image_settings.file_format="PNG"
        Path("output").mkdir(exist_ok=True)
        s.render.filepath="//output/sample.png"
        bpy.ops.render.render(write_still=True)
        return
    s.render.image_settings.file_format="FFMPEG";s.render.ffmpeg.format="MPEG4";s.render.ffmpeg.codec="H264";s.render.ffmpeg.audio_codec="AAC"
    Path("output").mkdir(exist_ok=True);s.render.filepath="//output/episode.mp4";bpy.ops.render.render(animation=True)
if __name__=="__main__":main()
