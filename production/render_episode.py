import json, math, sys
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
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=p)
    o=bpy.context.object;o.name=n;o.scale=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(m);o.parent=parent;return o
def cyl(n,p,r,d,m,parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=d,location=p)
    o=bpy.context.object;o.name=n;o.data.materials.append(m);o.parent=parent;return o

def child(name,x,y,shirt,hair,style,skin,dark):
    root=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(root);root.location=(x,y,0)
    sm=M(name+" shirt",shirt); hm=M(name+" hair",hair); pants=M(name+" pants",(.12,.28,.48))
    cube(name+" torso",(0,0,2.05),(.6,.34,.7),sm,root,.2)
    ball(name+" head",(0,0,3.25),(.62,.54,.7),skin,root)
    if style=="curls":
        for i,px in enumerate((-.45,-.22,0,.22,.45)):ball(name+f" curl{i}",(px,.02,3.85-abs(px)*.15),(.23,.23,.25),hm,root)
    else:
        ball(name+" haircap",(0,.05,3.72),(.61,.53,.32),hm,root)
        if style=="pony":ball(name+" ponytail",(.57,.16,3.35),(.23,.2,.43),hm,root)
    white=M(name+" whites",(1,.98,.92)); mouthmat=M(name+" mouth",(.45,.04,.08))
    for side in (-1,1):
        ball(name+f" eye{side}",(side*.22,-.51,3.37),(.13,.06,.16),white,root)
        ball(name+f" pupil{side}",(side*.22,-.565,3.37),(.06,.025,.08),dark,root)
    mouth=ball(name+" talking mouth",(0,-.57,3.08),(.17,.025,.065),mouthmat,root)
    arms=[];legs=[]
    for side in (-1,1):
        a=cyl(name+f" arm{side}",(side*.77,0,2.2),.14,1.1,skin,root);a.rotation_euler[1]=math.radians(-8*side);arms.append(a)
        ball(name+f" hand{side}",(side*.86,0,1.62),(.17,.17,.19),skin,root)
        l=cyl(name+f" leg{side}",(side*.3,0,.82),.18,1.3,pants,root);legs.append(l)
        cube(name+f" boot{side}",(side*.3,-.12,.15),(.24,.34,.15),M(name+f" bootmat{side}",(.16,.1,.07)),root,.08)
    cube(name+" backpack",(0,.36,2.1),(.45,.18,.5),M(name+" pack",(.86,.35,.08)),root,.16)
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
    trail=M("trail",(.62,.4,.19))
    for i in range(17):cube("trail",(math.sin(i*.5)*1.1,i*2.4-6,.01),(2.2,1.5,.04),trail,b=.2)
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
    r=p["root"];K(r,a,(r.location.x,y1,0));K(r,b,(r.location.x,y2,0));step=max(3,int(fps*.27))
    for f in range(a,b+1,step):
        ph=((f-a)//step)%2;r.location.z=.07 if ph else 0;r.keyframe_insert("location",frame=f)
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
    bpy.ops.wm.read_factory_settings(use_empty=True);skin=M("skin",(.72,.42,.25));dark=M("eyes",(.015,.012,.012));world()
    P={"Luke":child("Luke",-1.1,-5,(.04,.36,.75),(.24,.1,.04),"swept",skin,dark),"Lydia":child("Lydia",0,-5.7,(.86,.15,.45),(.12,.05,.03),"pony",skin,dark),"Poppy":child("Poppy",1.1,-6.4,(1,.57,.03),(.55,.2,.04),"curls",skin,dark)}
    B=bear(skin,dark);fps=ep.get("fps",24);animate(P,B,t,fps);camera(t["duration"],fps)
    s=bpy.context.scene;s.sequence_editor_create()
    for i,line in enumerate(t["lines"]):s.sequence_editor.sequences.new_sound(f"voice{i}",line["audio"],1,int(line["start"]*fps)+1)
    bpy.ops.object.light_add(type="SUN",location=(4,-4,12));bpy.context.object.data.energy=2.2
    bpy.ops.object.light_add(type="AREA",location=(-4,-4,9));bpy.context.object.data.energy=900;bpy.context.object.data.size=7
    if s.world is None:s.world=bpy.data.worlds.new("Episode World")
    s.world.color=(.16,.43,.7);s.render.engine="BLENDER_EEVEE";s.eevee.use_gtao=True;s.eevee.gtao_factor=1.3
    s.render.resolution_x,s.render.resolution_y=ep.get("resolution",[1080,1920]);s.render.resolution_percentage=50;s.render.fps=fps;s.frame_start=1;s.frame_end=int(t["duration"]*fps)
    s.render.image_settings.file_format="FFMPEG";s.render.ffmpeg.format="MPEG4";s.render.ffmpeg.codec="H264";s.render.ffmpeg.audio_codec="AAC"
    Path("output").mkdir(exist_ok=True);s.render.filepath="//output/episode.mp4";bpy.ops.render.render(animation=True)
if __name__=="__main__":main()
