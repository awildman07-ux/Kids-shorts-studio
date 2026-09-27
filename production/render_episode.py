import json
import math
import sys
from pathlib import Path

import bpy


def arg_after_double_dash():
    return Path(sys.argv[sys.argv.index("--") + 1])


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    return mat


def add_world():
    bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, 0))
    bpy.context.object.data.materials.append(material("grass", (0.19, 0.55, 0.24)))
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.04), scale=(2.6, 24, 0.04))
    bpy.context.object.data.materials.append(material("trail", (0.63, 0.43, 0.24)))
    for i in range(30):
        x = -5 if i % 2 == 0 else 5
        y = -22 + i * 1.5
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=.22, depth=2.5, location=(x, y, 1.25))
        bpy.context.object.data.materials.append(material(f"trunk{i}", (.23, .10, .04)))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.4, location=(x, y, 3.0))
        bpy.context.object.data.materials.append(material(f"leaves{i}", (.12, .46 + (i % 3) * .04, .18)))


def add_camera_and_light():
    bpy.ops.object.light_add(type="AREA", location=(4, -4, 10))
    bpy.context.object.data.energy = 1400
    bpy.context.object.data.shape = "DISK"
    bpy.context.object.data.size = 8
    bpy.ops.object.camera_add(location=(0, -11, 4.2), rotation=(math.radians(72), 0, 0))
    camera = bpy.context.object
    bpy.context.scene.camera = camera


def add_audio(timeline, fps):
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    for i, line in enumerate(timeline["lines"]):
        frame = int(line["start"] * fps) + 1
        scene.sequence_editor.sequences.new_sound(f"voice-{i}", line["audio"], 1, frame)


def main():
    episode = json.loads(arg_after_double_dash().read_text())
    timeline = json.loads(Path("build/timeline.json").read_text())
    bpy.ops.wm.read_factory_settings(use_empty=True)
    add_world()
    add_camera_and_light()
    fps = episode.get("fps", 24)
    add_audio(timeline, fps)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = episode.get("resolution", [1080, 1920])
    scene.render.resolution_percentage = 50
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = int(timeline["duration"] * fps)
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.audio_codec = "AAC"
    scene.render.filepath = "//output/episode.mp4"
    Path("output").mkdir(exist_ok=True)
    bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    main()

