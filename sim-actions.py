import bpy
import os, random
from math import radians, degrees
import time
from mathutils import Vector
import pyautogui as pog


grid_box_size = 3.2
bound_main_size = 16
bound_main_loc = (-8,-8)
min_drop_height = 15
max_drop_height = 30

animation_frames_count = 130

render_wait_time = 110

number_of_renders = 3

brick_count = 200

primary_box = []

secondary_box = []

metadata_save_dir = 'E:\\DATA\\Blocks-2\\DataGen\\Metadata'

renders_save_dir = 'E:\\DATA\\Blocks-2\\DataGen\\Renders'

pop_parts = 'E:\\Documents\\PRGM\\NEURAL\\Blocks\\parts-popular.txt'

def get_bricks():
    return [obj for obj in bpy.data.objects if 'Mesh' in obj.name]

def import_bricks(brick_count):
    parts = open(pop_parts,'r')
    parts = parts.readlines()
    parts = ['E:\\DATA\\Blocks-2\\part-objs\\'+part.replace('\n','')+'.obj' for part in parts][:brick_count]
    for obj_path in parts:
        imported = bpy.ops.import_scene.obj(filepath=obj_path)
        time.sleep(0.1)
        
def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))
        
class Box:

    dim_x = 1
    dim_y = 1

    def __init__(self, min_x, min_y, max_x, max_y, dim_x=dim_x, dim_y=dim_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.dim_x = dim_x
        self.dim_y = dim_y

    @property
    def x(self):
        return round(self.min_x * self.dim_x)

    @property
    def y(self):
        return round(self.dim_y - self.max_y * self.dim_y)

    @property
    def width(self):
        return round((self.max_x - self.min_x) * self.dim_x)

    @property
    def height(self):
        return round((self.max_y - self.min_y) * self.dim_y)

    def __str__(self):
        return "<Box, x=%i, y=%i, width=%i, height=%i>" % \
               (self.x, self.y, self.width, self.height)

    def to_tuple(self):
        if self.width == 0 or self.height == 0:
            return (0, 0, 0, 0)
        return (self.x, self.y, self.width, self.height)


def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return (0, 0, 0, 0)

    return (
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    )
        

def get_grid_main():
    num_box_axis = int(bound_main_size/grid_box_size)
    axis_pos_xy = [round((bound_main_loc[0]+(i*grid_box_size)+(grid_box_size/2)),3) for i in range(0,num_box_axis)]
    num_box_vertical = int(brick_count/(num_box_axis**2))
    axis_pos_z = [round((i*grid_box_size + min_drop_height),3) for i in range(0,num_box_vertical)]
    grid_positions = []
    for x in axis_pos_xy:
        for y in axis_pos_xy:
            for z in axis_pos_z:
                grid_positions.append((x,y,z))
    return grid_positions

def arrange_on_grid(bricks,grid_positions):
    random.shuffle(bricks)
    for index,brick in enumerate(bricks):
        brick.location.x,brick.location.y,brick.location.z = grid_positions[index][0],grid_positions[index][1],grid_positions[index][2]
        
def random_arrange_on_grid(bricks,grid_positions):
    random.shuffle(bricks)
    for index,brick in enumerate(bricks):
        brick.location.x,brick.location.y,brick.location.z = random.uniform(bound_main_loc[0],bound_main_loc[0]+bound_main_size),random.uniform(bound_main_loc[1],bound_main_loc[1]+bound_main_size),random.uniform(min_drop_height,max_drop_height)

def random_rotation(bricks):
    for brick in bricks:
        x,y,z = random.choice(range(0,360)),random.choice(range(0,360)),random.choice(range(0,360))
        brick.rotation_euler = (radians(x),radians(y),radians(z))
        
def random_materials(bricks):
    brick_mats = [mat for mat in bpy.data.materials if 'm' in mat.name]
    for brick in bricks:
        random_mat = random.choice(brick_mats)
        brick.active_material = random_mat

def run_animation(bricks):
    bpy.context.scene.frame_set(1)
    bpy.app.handlers.frame_change_pre.clear()
    def stop_playback(scene):
        if scene.frame_current == animation_frames_count:
            bpy.ops.screen.animation_cancel(restore_frame=False)
            
    bpy.app.handlers.frame_change_pre.append(stop_playback)
    bpy.ops.screen.animation_play()
    
def change_light():
    light_x_rotation = random.choice(range(35,65))
    light_z_rotation = random.choice(range(0,360))
    light = bpy.data.objects['Light']
    light.rotation_euler = (radians(light_x_rotation),0,radians(light_z_rotation))


def save_metadata(render_number,bricks):
    render_metadata = [render_number,(round(degrees(bpy.data.objects['Light'].rotation_euler[0]),2),round(degrees(bpy.data.objects['Light'].rotation_euler[2]),2))]
    brick_metadata_individual = []
    
    for brick in bricks:
        if ('Mesh' in brick.name):
            brick_metadata_individual.append([(brick.name).split('.')[0].split('_')[1],camera_view_bounds_2d(bpy.context.scene,
                                                                    bpy.context.scene.camera,
                                                                    bpy.data.objects.get(brick.name)),brick.active_material.name])
    metadata_file = open(metadata_save_dir+'\\'+str(render_number)+'.txt','w')
    metadata_file.write(str(render_metadata)+'\n')
    for m in brick_metadata_individual:
        metadata_file.write(str(m)+'\n')
        
    metadata_file.close()
    
    
    
def clean_materials():
    mats = bpy.data.materials
    
    for mat in mats:
        if ('Glow' not in mat.name and 'm' not in mat.name):
            mats.remove(mat)
    

def get_current_render_number():
    existing_renders = os.listdir(renders_save_dir)
    if (existing_renders != []):
        existing_renders = [int(name.split('.')[0]) for name in existing_renders]
        existing_renders.sort()
        return existing_renders[-1] + 1
    else:
        return 0

def step():
    bricks = get_bricks()

    random_materials(bricks)

    grid_positions = get_grid_main()

    random_rotation(bricks)
    random_arrange_on_grid(bricks,grid_positions)
    
    change_light()

    run_animation(bricks)
    
    render_number = get_current_render_number()
    
    save_metadata(render_number,bricks)
    

step()