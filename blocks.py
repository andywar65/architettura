"""Collection of functions for writing HTML of blocks.

Functions are referenced from architettura.aframe.make_block, a-block CAD blocks
have NAME attribute that are essentially block names, while BIM blocks use TYPE
attribute for setting 'partition type'. Block appearance is determined by
MATERIAL attribute (multiple components may be used depending on NAME), other
features depend on PARAM attributes.
"""

from math import degrees, sqrt, pow, fabs, atan2, sin, cos, radians
from random import random, gauss

def make_box(page, d):
    values = (
        ('pool', 0, 'box', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'box'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    d['dx'] = d['41']/2
    d['dy'] = -d['42']/2
    d['dz'] = d['43']/2
    d['ent'] = 'a-box'
    oput = ''
    if d['animation']:
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-rig" \n'
        oput += make_position(d)
        oput += f'rotation="{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}"> \n'
        oput += make_insertion(page, d)
    else:
        oput += make_insertion(page, d)
        oput += make_position(d)
        oput += f'rotation="{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}" \n'
    oput += f'scale="{round(d["41"], 4)} {round(d["43"], 4)} {round(d["43"], 4)}" \n'
    oput += object_material(d)
    oput += '"> \n'
    if d['ATTRIBUTE'] == 'stalker':
        oput += add_stalker(page, d)
    if d['animation']:
        oput += add_animation(d)
        oput += f'</{d["ent"]}></a-entity> \n'
    else:
        oput += f'</{d["ent"]}> \n'

    return oput

def make_insertion(page, d):
    oput = ''
    if d['ID']:
        oput += f'<{d["ent"]} id="{d["ID"]}" \n'
    else:
        oput += f'<{d["ent"]} id="{d["2"]}-{d["num"]}" \n'
    if d['ATTRIBUTE'] == 'checkpoint':
        oput += 'checkpoint '
    elif d['ATTRIBUTE'] == 'look-at':
        if d['TARGET']:
            oput += f'look-at="#{d["TARGET"]}" '
        else:
            oput += 'look-at="#camera" '
    elif d['ATTRIBUTE'] == 'stalker':
        oput += 'look-at="#camera" '
    if page.shadows:
        if d['2'] == 'a-curvedimage':
            oput += 'shadow="receive: false; cast: false" \n'
        elif d['2'] == 'a-light':
            pass
        else:
            oput += 'shadow="receive: true; cast: true" \n'
    return oput

def make_position(d):
    sx = sin(radians(-d['210']))
    cx = cos(radians(-d['210']))
    sy = sin(radians(-d['220']))
    cy = cos(radians(-d['220']))
    sz = sin(radians(-d['50']))
    cz = cos(radians(-d['50']))
    #Euler angles, yaw (Z), pitch (X), roll (Y)
    d['10'] = d['10'] + (cy*cz-sx*sy*sz)*d['dx'] + (-cx*sz)*d['dy'] +  (cz*sy+cy*sx*sz)*d['dz']
    d['20'] = d['20'] + (cz*sx*sy+cy*sz)*d['dx'] +  (cx*cz)*d['dy'] + (-cy*cz*sx+sy*sz)*d['dz']
    d['30'] = d['30'] +         (-cx*sy)*d['dx'] +     (sx)*d['dy']+            (cx*cy)*d['dz']
    oput = ''
    oput += f'position="{round(d["10"], 4)} {round(d["30"], 4)} {round(d["20"], 4)}" \n'
    return oput

def make_triangle(page, d):
    values = (
        ('pool', 0, 'triangle', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'triangle'
    d['rx'] = 1
    d['ry'] = 1
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    oput += f'<a-triangle id="a-triangle-{d["num"]}" \n'
    oput += 'geometry="vertexA:0 0 0; \n'
    oput += f'vertexB:{d["11"]} {d["31"]} {d["21"]}; \n'
    oput += f'vertexC:{d["12"]} {d["32"]} {d["22"]}" \n'
    oput += object_material(d)
    if page.double_face:
        oput += 'side: double; '
    oput += '">\n</a-triangle></a-entity><!--close triangle reset--> \n'
    return oput

def make_circular(d):
    values = (
        ('pool', 0, d['2'], 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = d['2']
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    oput = ''
    oput += f'<{d["2"]} id="{d["2"]}-{d["num"]}" \n'
    if d['2'] == 'a-circle':
        oput += f'radius="{fabs(d["41"])}" \n'
    else:
        oput += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    if float(d['43']) < 0:
        if d['2'] == 'a-cone' or d['2'] == 'a-cylinder' or d['2'] == 'a-sphere':
            oput += 'rotation="180 0 0" \n'
    oput += entity_geometry(d)
    oput += object_material(d)
    oput += '"> \n'
    oput += f'</{d["2"]}> \n'

    return oput

def make_curvedimage(d):
    values = (
        ('pool', 0, 'curved', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'curved'
    oput = ''
    oput += f'<a-curvedimage id="{d["2"]}-{d["num"]}" \n'
    oput += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    oput += entity_geometry(d)
    oput += object_material(d)
    oput += '"> \n'
    oput += '</a-curvedimage> \n'
    return oput

def entity_geometry(d):
    attr_dict = {
        'a-cone': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-cylinder': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-circle': ('SEGMENTS', 'THETA-LENGTH', 'THETA-START', ),
        'a-curvedimage': ('THETA-LENGTH', 'THETA-START', ),
        'a-sphere': ('PHI-LENGTH', 'PHI-START', 'SEGMENTS-HEIGHT', 'SEGMENTS-WIDTH', 'THETA-LENGTH', 'THETA-START', ),
    }
    attributes = attr_dict[d['2']]
    oput = 'geometry="'
    for attribute in attributes:
        try:
            if d[attribute]:
                oput += f'{attribute.lower()}: {d[attribute]};'
        except:
            pass

    oput += '" \n'
    return oput

def make_table_01(d):
    """Table 01, default block (t01)

    A simple table with four legs. Gets dimensions from block scaling, except for
    leg diameter (5cm). Gets top material from first component and leg material
    from third component.
    """
    values = (
        ('pool', 0, 'top', 'MATERIAL'),
        ('pool', 2, 'leg', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    #table top
    d['prefix'] = 'top'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    oput += f'<a-box id="{d["2"]}-{d["num"]}-table-top" \n'
    oput += f'position="0 {d["43"]-0.025*unit(d["43"])} 0" \n'
    oput += f'scale="{d["rx"]} 0.05 {d["ry"]}" \n'
    oput += object_material(d)
    oput += '"></a-box>\n'
    #prepare legs
    d['prefix'] = 'leg'
    scale_x = d["41"]/2-0.05*unit(d["41"])
    scale_y = d["42"]/2-0.05*unit(d["42"])
    height = d["43"]-0.025*unit(d["43"])
    d['rx'] = 1
    d['ry'] = 1
    values = (
        (1, scale_x, scale_y),
        (2, scale_x, -scale_y),
        (3, -scale_x, scale_y),
        (4, -scale_x, -scale_y),
    )
    #make legs
    for v in values:
        oput += f'<a-cylinder id="{d["2"]}-{d["num"]}-leg-{v[0]}" \n'
        oput += f'position="{v[1]} {height/2} {v[2]}" \n'
        oput += 'radius="0.025" \n'
        oput += f'height="{height}" \n'
        oput += object_material(d)
        oput += '"></a-cylinder>\n'
    oput += '</a-entity><!--close table01 reset--> \n'
    return oput

def make_door(d):
    """Door default BIM block.

    A simple framed door. Gets dimensions from block scaling, except for frame
    dimension. TYPE sets door features. If set to 'ghost' panel will not be
    rendered. SLIDING and DOUBLE are boolean. Gets panel material from first
    component and frame material from third component.
    """
    values = (
        ('pool', 0, 'panel', 'MATERIAL'),
        ('pool', 2, 'frame', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)

    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    d['prefix'] = 'frame'
    d['rx'] = 1
    d['ry'] = 1
    #left frame
    oput += f'<a-box id="{d["2"]}-{d["num"]}-left-frame" \n'
    oput += f'position="{-0.049*unit(d["41"])} {(d["43"]+0.099*unit(d["43"]))/2} {-d["42"]/2}" \n'
    oput += 'rotation="0 0 90" \n'
    oput += f'scale="{fabs(d["43"])+0.099} 0.1 {fabs(d["42"])+0.02}" \n'
    oput += object_material(d)
    oput += '"></a-box>\n'
    #right frame
    oput += f'<a-box id="{d["2"]}-{d["num"]}-right-frame" \n'
    oput += f'position="{d["41"]+0.049*unit(d["41"])} {(d["43"]+0.099*unit(d["43"]))/2} {-d["42"]/2}" \n'
    oput += 'rotation="0 0 90" \n'
    oput += f'scale="{fabs(d["43"])+0.099} 0.1 {fabs(d["42"])+0.02}" \n'
    oput += object_material(d)
    oput += '"></a-box>\n'
    #top frame
    oput += f'<a-box id="{d["2"]}-{d["num"]}-top-frame" \n'
    oput += f'position="{d["41"]/2} {d["43"]+0.049*unit(d["43"])} {-d["42"]/2}" \n'
    oput += f'scale="{fabs(d["41"])-0.002} 0.1 {fabs(d["42"])+0.02}" \n'
    oput += object_material(d)
    oput += '"></a-box>\n'

    if d["TYPE"] == 'ghost':
        oput += '</a-entity><!--close door reset--> \n'
        return oput
    else:
        d['prefix'] = 'panel'
        if eval(d["DOUBLE"]):
            d['rx'] = fabs(d["41"])/2-0.002
        else:
            d['rx'] = fabs(d["41"])-0.002
        d['ry'] = d["43"]-0.001*unit(d["43"])
        if eval(d["SLIDING"]):
            if eval(d["DOUBLE"]):
                #animated slide 1
                oput += f'<a-entity id="{d["2"]}-{d["num"]}-slide-1"> \n'
                oput += f'<a-animation attribute="position" from="0 0 0" to="{-(d["41"])/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                oput += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-1" \n'
                oput += f'position="{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-d["42"]/2}" \n'
                oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                oput += object_material(d)
                oput += '"></a-box>\n'
                oput += '</a-entity>\n'
                #animated slide 2
                oput += f'<a-entity id="{d["2"]}-{d["num"]}-slide-2" \n'
                oput += f'position="{d["41"]} 0 0"> \n'
                oput += f'<a-animation attribute="position" from="{d["41"]} 0 0" to="{(d["41"])*3/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 2
                oput += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-2" \n'
                oput += f'position="{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-d["42"]/2}" \n'
                oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                oput += object_material(d)
                oput += '"></a-box>\n'
                oput += '</a-entity>\n'
                oput += '</a-entity><!--close door reset--> \n'
                return oput
            else:#single
                #animated slide
                oput += f'<a-entity id="{d["2"]}-{d["num"]}-slide"> \n'
                oput += f'<a-animation attribute="position" from="0 0 0" to="{-d["41"]} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part
                oput += f'<a-box id="{d["2"]}-{d["num"]}-moving-part" \n'
                oput += f'position="{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} {-d["42"]/2}" \n'
                oput += f'scale="{fabs(d["41"])-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                oput += object_material(d)
                oput += '"></a-box>\n'
                oput += '</a-entity>\n'
                oput += '</a-entity><!--close door reset--> \n'
                return oput
        else:#hinged
            if eval(d["DOUBLE"]):
                #animated hinge 1
                oput += f'<a-entity id="{d["2"]}-{d["num"]}-hinge-1"> \n'
                oput += f'<a-animation attribute="rotation" from="0 0 0" to="0 {-90*unit(d["41"])*unit(d["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                oput += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-1" \n'
                oput += f'position="{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
                oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                oput += object_material(d)
                oput += '"></a-box>\n'
                oput += '</a-entity>\n'
                #animated hinge 2
                oput += f'<a-entity id="{d["2"]}-{d["num"]}-hinge-2" '
                oput += f'position="{d["41"]} 0 0"> \n'
                oput += f'<a-animation attribute="rotation" from="0 0 0" to="0 {90*unit(d["41"])*unit(d["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 2
                oput += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-2" \n'
                oput += f'position="{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
                oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                oput += object_material(d)
                oput += '"></a-box>\n'
                oput += '</a-entity>\n'
                oput += '</a-entity><!--close door reset--> \n'
                return oput
            else:#single
                #animated hinge
                oput += f'<a-entity id="{d["2"]}-{d["num"]}-hinge"> \n'
                oput += f'<a-animation attribute="rotation" from="0 0 0" to="0 {-90*unit(d["41"])*unit(d["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part
                oput += f'<a-box id="{d["2"]}-{d["num"]}-moving-part" \n'
                oput += f'position="{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
                oput += f'scale="{fabs(d["41"])-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                oput += object_material(d)
                oput += '"></a-box>\n'
                oput += '</a-entity>\n'
                oput += '</a-entity><!--close door reset--> \n'
                return oput

def make_slab(d):
    """Slab default BIM block.

    An horizontal partition. Gets dimensions from block scaling. TYPE sets
    partition type (TODO). Gets ceiling material from first component and
    floor material from third component.
    """
    values = (
        ('pool', 0, 'ceiling', 'MATERIAL'),
        ('pool', 2, 'floor', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'

    d['prefix'] = 'floor'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    #floor
    oput += f'<a-box id="{d["2"]}-{d["num"]}-floor" \n'
    oput += f'position="{d["41"]/2} {-0.005*unit(d["43"])} {-d["42"]/2}" \n'
    oput += f'scale="{d["rx"]} 0.01 {d["ry"]}" \n'
    oput += object_material(d)
    oput += '"></a-box>\n'
    #ceiling
    d['prefix'] = 'ceiling'
    oput += f'<a-box id="{d["2"]}-{d["num"]}-ceiling" \n'
    oput += f'position="{d["41"]/2} {-d["43"]/2-0.005*unit(d["43"])} {-d["42"]/2}" \n'
    oput += f'scale="{d["rx"]} {fabs(d["43"])-0.01} {d["ry"]}" \n'
    oput += object_material(d)
    oput += '"></a-box>\n'
    oput += '</a-entity><!--close slab reset--> \n'

    return oput

def make_wall(d):
    """Wall default BIM block.

    A vertical partition. Gets dimensions from block scaling, TILING and
    SKIRTING height from respective attributes. TYPE sets partition type
    (TODO). Gets two different MATERIALs for internal and external surface, and
    respectively first component for wall, second for tiling and third for
    skirting.
    """
    values = (
        ('pool', 0, 'wall', 'MATERIAL'),
        ('pool', 1, 'tile', 'MATERIAL'),
        ('pool', 2, 'skirt', 'MATERIAL'),
        ('pool2', 0, 'wall2', 'MATERIAL2'),
        ('pool2', 1, 'tile2', 'MATERIAL2'),
        ('pool2', 2, 'skirt2', 'MATERIAL2'),
    )
    d = prepare_material_values(values, d)
    wall_h = wall2_h = fabs(d['43'])
    tile_h = fabs(float(d['TILING']))
    skirt_h = fabs(float(d['SKIRTING']))
    tile2_h = fabs(float(d['TILING2']))
    skirt2_h = fabs(float(d['SKIRTING2']))
    if d['2'] == 'a-openwall-above':
        door_h = d['door_height']
    else:
        door_h = 0
    if tile_h > wall_h:
        tile_h = wall_h
    if skirt_h > wall_h:
        skirt_h = wall_h
    if skirt_h < door_h:
        skirt_h = door_h
    if skirt_h > tile_h:
        tile_h = skirt_h
    if tile2_h > wall2_h:
        tile2_h = wall2_h
    if skirt2_h > wall2_h:
        skirt2_h = wall2_h
    if skirt2_h < door_h:
        skirt2_h = door_h
    if skirt2_h > tile2_h:
        tile2_h = skirt2_h
    wall_h = wall_h - tile_h
    tile_h = tile_h - skirt_h
    skirt_h = skirt_h - door_h
    wall2_h = wall2_h - tile2_h
    tile2_h = tile2_h - skirt2_h
    skirt2_h = skirt2_h - door_h

    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'

    values = (
        (skirt_h, 'int-skirt', skirt_h/2, d["42"]/2, fabs(d["42"]), 'skirt'),
        (tile_h, 'int-tile', tile_h/2+skirt_h, d["42"]/2, fabs(d["42"]), 'tile'),
        (wall_h, 'int-wall', wall_h/2+tile_h+skirt_h, d["42"]/2, fabs(d["42"]), 'wall'),
        (skirt2_h, 'ext-skirt', skirt2_h/2, d["42"], 0.02, 'skirt2'),
        (tile2_h, 'ext-tile', tile2_h/2+skirt2_h, d["42"], 0.02, 'tile2'),
        (wall2_h, 'ext-wall', wall2_h/2+tile2_h+skirt2_h, d["42"], 0.02, 'wall2'),
    )
    for v in values:
        if v[0]:
            d['prefix'] = v[5]
            d['rx'] = fabs(d["41"])
            d['ry'] = v[0]
            oput += f'<a-box id="{d["2"]}-{d["num"]}-{v[1]}" \n'
            oput += f'position="{d["41"]/2} {v[2]*unit(d["43"])} {-v[3]+0.005*unit(d["42"])}" \n'
            oput += f'scale="{d["rx"]} {v[0]} {v[4]-0.01}" \n'
            oput += object_material(d)
            oput += '"></a-box>\n'

    oput += '</a-entity><!--close wall reset--> \n'
    return oput

def make_openwall(d):
    oput = ''

    #make left wall
    d2 = d.copy()
    d2['41'] = d2['door_off_1']
    d2['2'] = 'a-openwall-left'
    oput += make_wall(d2)
    #make part above door
    d2 = d.copy()
    d2['41'] = d2['door_off_2'] - d2['door_off_1']
    d2['2'] = 'a-openwall-above'
    oput += f'<a-entity id="{d2["2"]}-{d2["num"]}-ent" \n'
    oput += f'position="{d2["door_off_1"]} {d2["door_height"]} 0"> \n'
    oput += make_wall(d2)
    oput += '</a-entity> \n'
    #make right wall
    d2 = d.copy()
    d2['41'] = d2['41'] - d2['door_off_2']
    d2['2'] = 'a-openwall-right'
    oput += f'<a-entity id="{d2["2"]}-{d2["num"]}-ent" \n'
    oput += f'position="{d2["door_off_2"]} 0 0"> \n'
    oput += make_wall(d2)
    oput += '</a-entity> \n'

    return oput

def make_plane(page, d):
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="0 {-d["zg"]-d["zs"]} 0"> \n'
    oput += make_w_plane(page, d)
    oput += '</a-entity><!--close plane reset--> \n'
    return oput

def make_w_plane(page, d):
    """Wall plane default BIM block.

    A vertical surface. Gets dimensions from plane scaling, TILING and
    SKIRTING height from respective attributes. Gets MATERIAL with 3 components,
    first for wall, second for tiling and third for skirting.
    """
    #prepare values for materials
    values = (
        ('pool', 0, 'wall', 'MATERIAL'),
        ('pool', 1, 'tile', 'MATERIAL'),
        ('pool', 2, 'skirt', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    #prepare height values
    wall_h = fabs(d['43'])
    if 'TILING' in d:
        tile_h = fabs(float(d['TILING']))
    else:
        tile_h = 0
    if 'SKIRTING' in d:
        skirt_h = fabs(float(d['SKIRTING']))
    else:
        skirt_h = 0
    if tile_h > wall_h:
        tile_h = wall_h
    if skirt_h > wall_h:
        skirt_h = wall_h
    if skirt_h > tile_h:
        tile_h = skirt_h
    wall_h = wall_h - tile_h
    tile_h = tile_h - skirt_h
    oput = ''
    #prepare values for surfaces
    values = (
        (skirt_h, 'skirt', skirt_h/2,),
        (tile_h, 'tile', tile_h/2+skirt_h,),
        (wall_h, 'wall', wall_h/2+tile_h+skirt_h,),
    )
    #loop surfaces
    d['rx'] = fabs(d["41"])
    for v in values:
        if v[0]:
            d['prefix'] = v[1]
            d['ry'] = v[0]
            oput += f'<a-plane id="{d["2"]}-{d["num"]}-{v[1]}" \n'
            oput += f'position="0 {v[2]*unit(d["43"])} 0" \n'
            oput += f'width="{d["rx"]}" height="{v[0]}" \n'
            oput += object_material(d)
            if page.double_face:
                oput += 'side: double; '
            oput += '"></a-plane>\n'

    return oput

def make_light(page, d):
    #set defaults
    if d['TYPE'] == '':
        d['TYPE'] = 'point'
        d['INTENSITY'] = 0.75
        d['DISTANCE'] = 50
        d['DECAY'] = 2
    if d['COLOR'] == '':
        d['COLOR'] = d['color']

    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}" \n'


    oput += f'light="type: {d["TYPE"]}; color: {d["COLOR"]}; intensity: {d["INTENSITY"]}; '
    if d['TYPE'] != 'ambient':
        if page.shadows:
            oput += 'castShadow: true; '
    if d['TYPE'] == 'point' or d['TYPE'] == 'spot':
        oput += f'decay: {d["DECAY"]}; distance: {d["DISTANCE"]}; '
    if d['TYPE'] == 'spot':
        oput += f'angle: {d["ANGLE"]}; penumbra: {d["PENUMBRA"]}; '
    if d['TYPE'] == 'directional':
        oput += f'shadowCameraBottom: {-5*fabs(d["42"])}; \n'
        oput += f'shadowCameraLeft: {-5*fabs(d["41"])}; \n'
        oput += f'shadowCameraTop: {5*fabs(d["42"])}; \n'
        oput += f'shadowCameraRight: {5*fabs(d["41"])}; \n'
    if d['TYPE'] == 'directional' or d['TYPE'] == 'spot':
        oput += make_light_target(d)
    else:
        oput += '">\n'

    oput += '</a-entity> \n'#close light entity
    return oput

def make_light_target(d):
    oput = f'target: #light-{d["num"]}-target;"> \n'
    oput += f'<a-entity id="light-{d["num"]}-target" position="0 -1 0"> </a-entity> \n'
    return oput

def make_text(d):
    values = (
        ('pool', 0, 'text', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    oput = ''
    oput += f'<a-entity id="a-text-{d["num"]}" \n'
    oput += f'text="width: {d["41"]}; align: {d["ALIGN"]}; color: {d["text_color"]}; '
    oput += f'value: {d["TEXT"]}; wrap-count: {d["WRAP-COUNT"]}; '
    oput += '">\n'
    oput += '</a-entity>\n'
    return oput

def make_link(page, d):
    oput = f'<a-link id="a-link-{d["num"]}" \n'
    oput += f'scale="{d["41"]} {d["43"]} {d["42"]}"\n'
    target = False
    try:
        if d['LINK'] == 'parent':
            target = page.get_parent()
        elif d['LINK'] == 'child':
            target = page.get_first_child()
        elif d['LINK'] == 'previous' or d['LINK'] == 'prev':
            target = page.get_prev_sibling()
        elif d['LINK'] == 'next':
            target = page.get_next_sibling()
    except:
        d['LINK'] = ''
    if target:
        oput += f'href="{target.url}" \n'
        oput += f'title="{target.title}" on="click" \n'
        try:
            eq_image = target.specific.equirectangular_image
            if eq_image:
                oput += f'image="{eq_image.file.url}"'
        except:
            oput += 'image="#default-sky"'
    else:
        oput += f'href="{d["LINK"]}" \n'
        oput += 'title="Sorry, no title" on="click" \n'
        oput += 'image="#default-sky"'
    oput += '></a-link>\n'
    return oput

def unit(nounit):
    #returns positive/negative scaling
    if nounit == 0:
        return 0
    unit = fabs(nounit)/nounit
    return unit

def object_material(d):
    #returns object material
    oput = ''
    if d['wireframe']:
        oput += f'material="wireframe: true; wireframe-linewidth: {d["wf_width"]}; color: {d[d["prefix"]+"_color"]}; '
    else:
        oput += f'material="src: #{d[d["prefix"]+"_image"]}; color: {d[d["prefix"]+"_color"]};'
        if d[d['prefix']+'_repeat']:
            oput += f' repeat:{d["rx"]} {d["ry"]};'
    return oput

def prepare_material_values(values, d):

    for v in values:
        try:
            component_pool = d[v[0]]
            component = component_pool[v[1]]
            d[v[2]+'_color'] = component[1]
            d[v[2]+'_image'] = d[v[3]] + '-' + component[0]
            d[v[2]+'_repeat'] = component[2]

        except:
            d[v[2]+'_color'] = d['color']
            d[v[2]+'_image'] = d['8']
            d[v[2]+'_repeat'] = d['repeat']

    return d

def make_object(d):
    """Object block

    Block loads a Object Model (Wavefront) along with it's *.mtl file. PARAM1
    must be equal to *.obj and *.mtl filename (use lowercase extension). Files
    must share same filename and must be loaded in the media/document folder.
    If PARAM2 is set to 'scale', object will be scaled.
    """
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-object" \n'
    oput += f'obj-model="obj: #{d["PARAM1"]}-obj; \n'
    oput += f' mtl: #{d["PARAM1"]}-mtl" \n'
    if d['PARAM2'] == 'scale':
        oput += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    oput += '></a-entity><!--close object--> \n'
    oput += '</a-entity><!--close object reset--> \n'
    return oput

def make_tree(d):
    """Tree block

    Gets dimensions from block scaling. Gets trunk material from first
    component, branch from second and leaves from third.
    """
    values = (
        ('pool', 0, 'trunk', 'MATERIAL'),
        ('pool', 1, 'branch', 'MATERIAL'),
        ('pool', 2, 'leaf', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    ht = 0.7172 * d['43'] * gauss(1, .1)
    lt = ht * gauss(1, .1)
    l0 = 0.7172 * lt * gauss(1, .1)
    l00 = 0.7172 * l0 * gauss(1, .1)
    l000 = 0.7172 * l00 * gauss(1, .1)
    l001 = 0.7172 * l00 * gauss(1, .1)
    l01 = 0.7172 * l0 * gauss(1, .1)
    l010 = 0.7172 * l01 * gauss(1, .1)
    l011 = 0.7172 * l01 * gauss(1, .1)
    l1 = 0.7172 * lt * gauss(1, .1)
    l10 = 0.7172 * l1 * gauss(1, .1)
    l100 = 0.7172 * l10 * gauss(1, .1)
    l101 = 0.7172 * l10 * gauss(1, .1)
    l11 = 0.7172 * l1 * gauss(1, .1)
    l110 = 0.7172 * l11 * gauss(1, .1)
    l111 = 0.7172 * l11 * gauss(1, .1)
    ang = gauss(0, 5)
    rot = random()*360
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    d['prefix'] = 'trunk'
    d['rx'] = fabs(d["41"])
    d['ry'] = lt
    oput += f'<a-entity id="{d["NAME"]}-{d["num"]}-trunk-ent" \n'
    oput += f'position="0 0 0" \n'
    oput += f'rotation="{ang} {rot} 0"> \n'
    #oput += f'<a-animation attribute="rotation" from="{ang} {rot} 0" '
    #oput += f'to="{ang*gauss(1, .1)} {rot} 0" dur="{int(5000*gauss(1, .5))}" repeat="indefinite" direction="alternate"></a-animation>'
    oput += f'<a-cone id="{d["NAME"]}-{d["num"]}-trunk" \n'
    oput += f'position="0 {lt/2} 0" \n'
    oput += f'geometry="height: {lt}; radius-bottom: {lt/8}; radius-top: {lt/12};" \n'
    oput += object_material(d)
    oput += '">\n'
    oput += '</a-cone> \n'#close trunk
    osc = 30 * gauss(1, .1)
    rot0 = random()*360
    rot00 = random()*360
    rot000 = random()*360
    rot010 = random()*360
    rot10 = random()*360
    rot100 = random()*360
    rot110 = random()*360
    oput += make_branch('0', l0, lt, osc, rot0, d)
    oput += make_branch('00', l00, l0, osc, rot00, d)
    oput += make_branch('000', l000, l00, osc, rot000, d)
    oput += make_leaves('000', l000, d)
    oput += '</a-entity> \n'
    oput += make_branch('001', l001, l00, -osc, 180-rot000, d)
    oput += make_leaves('001', l001, d)
    oput += '</a-entity> \n'
    oput += '</a-entity> \n'
    oput += make_branch('01', l01, l0, -osc, 180-rot00, d)
    oput += make_branch('010', l010, l01, osc, rot010, d)
    oput += make_leaves('010', l010, d)
    oput += '</a-entity> \n'
    oput += make_branch('011', l011, l01, -osc, 180-rot010, d)
    oput += make_leaves('011', l011, d)
    oput += '</a-entity> \n'
    oput += '</a-entity> \n'
    oput += '</a-entity> \n'
    oput += make_branch('1', l1, lt, -osc, 180-rot0, d)
    oput += make_branch('10', l10, l1, osc, rot10, d)
    oput += make_branch('100', l100, l10, osc, rot100, d)
    oput += make_leaves('100', l100, d)
    oput += '</a-entity> \n'
    oput += make_branch('101', l101, l10, -osc, 180-rot100, d)
    oput += make_leaves('101', l101, d)
    oput += '</a-entity> \n'
    oput += '</a-entity> \n'
    oput += make_branch('11', l11, l1, -osc, 180-rot10, d)
    oput += make_branch('110', l110, l11, osc, rot110, d)
    oput += make_leaves('110', l110, d)
    oput += '</a-entity> \n'
    oput += make_branch('111', l111, l11, -osc, 180-rot110, d)
    oput += make_leaves('111', l111, d)
    oput += '</a-entity> \n'
    oput += '</a-entity> \n'
    oput += '</a-entity> \n'

    oput += '</a-entity><!--close tree--> \n'
    oput += '</a-entity><!--close polyline reset--> \n'
    return oput

def make_branch(branch, lb, lp, angle, rotx, d):
    d['prefix'] = 'branch'
    d['rx'] = fabs(d["41"])
    d['ry'] = lb
    ang = gauss(angle, 10)
    rot = gauss(rotx, 20)
    oput = f'<a-entity id="{d["TYPE"]}-{d["num"]}-branch-{branch}-ent" \n'
    oput += f'position="0 {lp*.95-lp*fabs(gauss(0, .2))} 0" \n'
    oput += f'rotation="{ang} {rot} 0"> \n'
    oput += f'<a-cone id="{d["TYPE"]}-{d["num"]}-branch-{branch}" \n'
    oput += f'position="0 {lb/2} 0" \n'
    oput += f'geometry="height: {lb}; radius-bottom: {lb/12}; radius-top: {lb/14};" \n'
    oput += object_material(d)
    oput += '">\n'
    oput += '</a-cone> \n'#close branch
    return oput

def make_leaves(branch, lb, d):
    d['prefix'] = 'leaf'
    d['rx'] = lb
    d['ry'] = lb
    oput = f'<a-sphere id="{d["NAME"]}-{d["num"]}-leaves-{branch}" \n'
    oput += f'position="0 {lb} 0" \n'
    oput += f'geometry="radius: {gauss(lb, lb/5)};" \n'
    oput += object_material(d)
    oput += 'side: back;">\n'
    oput += '</a-sphere> \n'#close branch
    return oput

def make_poly(page, d):
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    if d['39']:
        d['42'] = 0
        d['43'] = d['39']
        d['num1'] = d['num']
        for i in range(d['90']-1):
            d['num'] = str(d['num1']) + '-' + str(i)
            dx = d['vx'][i]-d['vx'][i+1]
            dy = d['vy'][i]-d['vy'][i+1]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            oput += f'<a-entity id="{d["2"]}-{d["num"]}-wall-ent" \n'
            oput += f'position="{d["vx"][i]-dx/2} 0 {d["vy"][i]-dy/2}" \n'
            oput += f'rotation="0 {d["50"]} 0"> \n'
            oput += make_w_plane(page, d)
            oput +='</a-entity>'
        if d['70']:
            d['num'] = str(d['num1']) + '-' + str(i+1)
            dx = d['vx'][i+1]
            dy = d['vy'][i+1]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            oput += f'<a-entity id="{d["2"]}-{d["num"]}-wall-ent" \n'
            oput += f'position="{dx/2} 0 {dy/2}" \n'
            oput += f'rotation="0 {d["50"]} 0"> \n'
            oput += make_w_plane(page, d)
            oput +='</a-entity>'
    else:
        oput += f'<a-entity id="{d["2"]}-{d["num"]}" \n'
        oput += f'line="start:0 0 0; \n'
        oput += f'end:{d["vx"][1]} 0 {d["vy"][1]}; \n'
        oput += f'color: {d["color"]}" \n'
        for i in range(1, d['90']-1):
            oput += f'line__{i+1}="start:{d["vx"][i]} 0 {d["vy"][i]}; \n'
            oput += f'end:{d["vx"][i+1]} 0 {d["vy"][i+1]}; \n'
            oput += f'color: {d["color"]}" \n'
        if d['70']:
            oput += f'line__{i+2}=start:{d["vx"][i+1]} 0 {d["vy"][i+1]}; \n'
            oput += 'end:0 0 0; \n'
            oput += f'color: {d["color"]}" \n'
        oput += '></a-entity>'
    oput += '</a-entity><!--close polyline reset--> \n'
    return oput

def make_line(page, d):
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    oput += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    if d['39']:
        d['42'] = 0
        d['43'] = d['39']
        d['41'] = sqrt(pow(d['11'], 2) + pow(d['21'], 2))
        d['50'] = -degrees(atan2(d['21'], d['11']))
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-wall-ent" \n'
        oput += f'position="{d["11"]/2} 0 {d["21"]/2}" \n'
        oput += f'rotation="0 {d["50"]} 0"> \n'
        oput += make_w_plane(page, d)
        oput +='</a-entity><!--close wall--> \n'
    else:
        oput += f'<a-entity id="{d["2"]}-{d["num"]}" \n'
        oput += 'line="start:0 0 0; \n'
        oput += f'end:{d["11"]} {d["31"]} {d["21"]}; \n'
        oput += f'color: {d["color"]};"> \n'
        oput += '</a-entity><!--close line--> \n'
    oput += '</a-entity><!--close line reset--> \n'
    return oput

def add_animation(d):
    oput = ''
    oput += f'<a-animation id="{d["2"]}-{d["num"]}-animation" \n'
    oput += f'attribute="{d["ATTRIBUTE"]}"\n'
    oput += f'from="{d["FROM"]}"\n'
    oput += f'to="{d["TO"]}"\n'
    oput += f'begin="{d["BEGIN"]}"\n'
    oput += f'direction="{d["DIRECTION"]}"\n'
    oput += f'repeat="{d["REPEAT"]}"\n'
    oput += f'dur="{d["DURATION"]}"\n'
    oput += '></a-animation>\n'
    return oput

def add_stalker(page, d):
    oput = ''
    if d['TEXT']:
        length = len(d['TEXT'])
        if length <= 8:
            wrapcount = length+1
        elif length <= 30:
            wrapcount = 10
        else:
            wrapcount = length/3
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-balloon-ent" \n'
        oput += f'position="0 {d["43"]/2+d["41"]/4+.1} 0" \n'
        oput += f'text="width: {d["41"]*.9}; align: center; color: black; '
        oput += f'value: {d["TEXT"]}; wrap-count: {wrapcount};"> \n'
        oput += f'<a-cylinder id="{d["2"]}-{d["num"]}-balloon" \n'
        oput += f'position="0 0 -0.01" \n'
        oput += f'rotation="90 0 0" \n'
        oput += f'scale="{fabs(d["41"])/1.5} 0 {fabs(d["41"])/3}"> \n'
        oput += '</a-cylinder></a-entity>\n'
        oput += f'<a-triangle id="{d["2"]}-{d["num"]}-triangle" \n'
        oput += f'geometry="vertexA:0 {d["43"]/2+.1} 0.0005; \n'
        oput += f'vertexB:0 {d["43"]/2-.05} 0.0005; \n'
        oput += f'vertexC:{d["41"]/4} {d["43"]/2+.1} 0.0005"> \n'
        oput += '</a-triangle> \n'
    if d['LINK']:
        oput += f'<a-link id="{d["2"]}-{d["num"]}-link" \n'
        oput += f'position="{d["41"]*.7} 0 0.02" \n'
        oput += f'scale="{d["41"]*.35} {d["41"]*.35}"\n'
        target = False
        try:
            if d['LINK'] == 'parent':
                target = page.get_parent()
            elif d['LINK'] == 'child':
                target = page.get_first_child()
            elif d['LINK'] == 'previous' or d['LINK'] == 'prev':
                target = page.get_prev_sibling()
            elif d['LINK'] == 'next':
                target = page.get_next_sibling()
        except:
            d['LINK'] = ''
        if target:
            oput += f'href="{target.url}" \n'
            oput += f'title="{target.title}" on="click" \n'
            try:
                eq_image = target.specific.equirectangular_image
                if eq_image:
                    oput += f'image="{eq_image.file.url}"'
            except:
                oput += 'image="#default-sky"'
        else:
            oput += f'href="{d["LINK"]}" \n'
            oput += 'title="Sorry, no title" on="click" \n'
            oput += 'image="#default-sky"'
        oput += '>\n'
        oput += '</a-link>\n'
    return oput
