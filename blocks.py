"""Collection of functions for writing HTML of blocks.

Functions are referenced from architettura.aframe.make_block, a-block CAD blocks
have NAME attribute that are essentially block names, while BIM blocks use TYPE
attribute for setting 'partition type'. Block appearance is determined by
MATERIAL attribute (multiple components may be used depending on NAME), other
features depend on PARAM attributes.
"""

from math import degrees, sqrt, pow, fabs, atan2
from random import random, gauss

def make_box(d):
    values = (
        ('pool', 0, 'box', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'box'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    outstr = ''
    outstr += f'<a-box id="{d["2"]}-{d["num"]}" \n'
    outstr += f'position="{d["10"]} {d["30"]} {d["20"]}" \n'
    outstr += f'rotation="{d["210"]} {d["50"]} {d["220"]}" \n'
    outstr += f'scale="{d["rx"]} {d["43"]} {d["ry"]}" \n'
    outstr += object_material(d)
    outstr += '"> \n'
    outstr += '</a-box> \n'

    return outstr

def make_triangle(page, d):
    values = (
        ('pool', 0, 'triangle', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'triangle'
    d['rx'] = 1
    d['ry'] = 1
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    outstr += f'<a-triangle id="a-triangle-{d["num"]}" \n'
    outstr += 'geometry="vertexA:0 0 0; \n'
    outstr += f'vertexB:{d["11"]} {d["31"]} {d["21"]}; \n'
    outstr += f'vertexC:{d["12"]} {d["32"]} {d["22"]}" \n'
    outstr += object_material(d)
    if page.double_face:
        outstr += 'side: double; '
    outstr += '">\n</a-triangle></a-entity><!--close triangle reset--> \n'
    return outstr

def make_circular(d):
    values = (
        ('pool', 0, d['2'], 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = d['2']
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    outstr = ''
    outstr += f'<{d["2"]} id="{d["2"]}-{d["num"]}" \n'
    if d['2'] == 'a-circle':
        outstr += f'radius="{fabs(d["41"])}" \n'
    else:
        outstr += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    if float(d['43']) < 0:
        if d['2'] == 'a-cone' or d['2'] == 'a-cylinder' or d['2'] == 'a-sphere':
            outstr += 'rotation="180 0 0" \n'
    outstr += entity_geometry(d)
    outstr += object_material(d)
    outstr += '"> \n'
    outstr += f'</{d["2"]}> \n'

    return outstr

def make_curvedimage(d):
    values = (
        ('pool', 0, 'curved', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'curved'
    outstr = ''
    outstr += f'<a-curvedimage id="{d["2"]}-{d["num"]}" \n'
    outstr += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    outstr += entity_geometry(d)
    outstr += object_material(d)
    outstr += '"> \n'
    outstr += '</a-curvedimage> \n'
    return outstr

def entity_geometry(d):
    attr_dict = {
        'a-cone': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-cylinder': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-circle': ('SEGMENTS', 'THETA-LENGTH', 'THETA-START', ),
        'a-curvedimage': ('THETA-LENGTH', 'THETA-START', ),
        'a-sphere': ('PHI-LENGTH', 'PHI-START', 'SEGMENTS-HEIGHT', 'SEGMENTS-WIDTH', 'THETA-LENGTH', 'THETA-START', ),
    }
    attributes = attr_dict[d['2']]
    outstr = 'geometry="'
    for attribute in attributes:
        try:
            if d[attribute]:
                outstr += f'{attribute.lower()}: {d[attribute]};'
        except:
            pass

    outstr += '" \n'
    return outstr

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
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    #table top
    d['prefix'] = 'top'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    outstr += f'<a-box id="{d["2"]}-{d["num"]}-table-top" \n'
    outstr += f'position="0 {d["43"]-0.025*unit(d["43"])} 0" \n'
    outstr += f'scale="{d["rx"]} 0.05 {d["ry"]}" \n'
    outstr += object_material(d)
    outstr += '"></a-box>\n'
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
        outstr += f'<a-cylinder id="{d["2"]}-{d["num"]}-leg-{v[0]}" \n'
        outstr += f'position="{v[1]} {height/2} {v[2]}" \n'
        outstr += 'radius="0.025" \n'
        outstr += f'height="{height}" \n'
        outstr += object_material(d)
        outstr += '"></a-cylinder>\n'
    outstr += '</a-entity><!--close table01 reset--> \n'
    return outstr

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

    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    d['prefix'] = 'frame'
    d['rx'] = 1
    d['ry'] = 1
    #left frame
    outstr += f'<a-box id="{d["2"]}-{d["num"]}-left-frame" \n'
    outstr += f'position="{-0.049*unit(d["41"])} {(d["43"]+0.099*unit(d["43"]))/2} {-d["42"]/2}" \n'
    outstr += 'rotation="0 0 90" \n'
    outstr += f'scale="{fabs(d["43"])+0.099} 0.1 {fabs(d["42"])+0.02}" \n'
    outstr += object_material(d)
    outstr += '"></a-box>\n'
    #right frame
    outstr += f'<a-box id="{d["2"]}-{d["num"]}-right-frame" \n'
    outstr += f'position="{d["41"]+0.049*unit(d["41"])} {(d["43"]+0.099*unit(d["43"]))/2} {-d["42"]/2}" \n'
    outstr += 'rotation="0 0 90" \n'
    outstr += f'scale="{fabs(d["43"])+0.099} 0.1 {fabs(d["42"])+0.02}" \n'
    outstr += object_material(d)
    outstr += '"></a-box>\n'
    #top frame
    outstr += f'<a-box id="{d["2"]}-{d["num"]}-top-frame" \n'
    outstr += f'position="{d["41"]/2} {d["43"]+0.049*unit(d["43"])} {-d["42"]/2}" \n'
    outstr += f'scale="{fabs(d["41"])-0.002} 0.1 {fabs(d["42"])+0.02}" \n'
    outstr += object_material(d)
    outstr += '"></a-box>\n'

    if d["TYPE"] == 'ghost':
        outstr += '</a-entity><!--close door reset--> \n'
        return outstr
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
                outstr += f'<a-entity id="{d["2"]}-{d["num"]}-slide-1"> \n'
                outstr += f'<a-animation attribute="position" from="0 0 0" to="{-(d["41"])/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                outstr += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-1" \n'
                outstr += f'position="{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-d["42"]/2}" \n'
                outstr += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                outstr += object_material(d)
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                #animated slide 2
                outstr += f'<a-entity id="{d["2"]}-{d["num"]}-slide-2" \n'
                outstr += f'position="{d["41"]} 0 0"> \n'
                outstr += f'<a-animation attribute="position" from="{d["41"]} 0 0" to="{(d["41"])*3/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 2
                outstr += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-2" \n'
                outstr += f'position="{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-d["42"]/2}" \n'
                outstr += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                outstr += object_material(d)
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                outstr += '</a-entity><!--close door reset--> \n'
                return outstr
            else:#single
                #animated slide
                outstr += f'<a-entity id="{d["2"]}-{d["num"]}-slide"> \n'
                outstr += f'<a-animation attribute="position" from="0 0 0" to="{-d["41"]} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part
                outstr += f'<a-box id="{d["2"]}-{d["num"]}-moving-part" \n'
                outstr += f'position="{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} {-d["42"]/2}" \n'
                outstr += f'scale="{fabs(d["41"])-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                outstr += object_material(d)
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                outstr += '</a-entity><!--close door reset--> \n'
                return outstr
        else:#hinged
            if eval(d["DOUBLE"]):
                #animated hinge 1
                outstr += f'<a-entity id="{d["2"]}-{d["num"]}-hinge-1"> \n'
                outstr += f'<a-animation attribute="rotation" from="0 0 0" to="0 {-90*unit(d["41"])*unit(d["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                outstr += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-1" \n'
                outstr += f'position="{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
                outstr += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                outstr += object_material(d)
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                #animated hinge 2
                outstr += f'<a-entity id="{d["2"]}-{d["num"]}-hinge-2" '
                outstr += f'position="{d["41"]} 0 0"> \n'
                outstr += f'<a-animation attribute="rotation" from="0 0 0" to="0 {90*unit(d["41"])*unit(d["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 2
                outstr += f'<a-box id="{d["2"]}-{d["num"]}-moving-part-2" \n'
                outstr += f'position="{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
                outstr += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                outstr += object_material(d)
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                outstr += '</a-entity><!--close door reset--> \n'
                return outstr
            else:#single
                #animated hinge
                outstr += f'<a-entity id="{d["2"]}-{d["num"]}-hinge"> \n'
                outstr += f'<a-animation attribute="rotation" from="0 0 0" to="0 {-90*unit(d["41"])*unit(d["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part
                outstr += f'<a-box id="{d["2"]}-{d["num"]}-moving-part" \n'
                outstr += f'position="{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
                outstr += f'scale="{fabs(d["41"])-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
                outstr += object_material(d)
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                outstr += '</a-entity><!--close door reset--> \n'
                return outstr

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
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'

    d['prefix'] = 'floor'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    #floor
    outstr += f'<a-box id="{d["2"]}-{d["num"]}-floor" \n'
    outstr += f'position="{d["41"]/2} {-0.005*unit(d["43"])} {-d["42"]/2}" \n'
    outstr += f'scale="{d["rx"]} 0.01 {d["ry"]}" \n'
    outstr += object_material(d)
    outstr += '"></a-box>\n'
    #ceiling
    d['prefix'] = 'ceiling'
    outstr += f'<a-box id="{d["2"]}-{d["num"]}-ceiling" \n'
    outstr += f'position="{d["41"]/2} {-d["43"]/2-0.005*unit(d["43"])} {-d["42"]/2}" \n'
    outstr += f'scale="{d["rx"]} {fabs(d["43"])-0.01} {d["ry"]}" \n'
    outstr += object_material(d)
    outstr += '"></a-box>\n'
    outstr += '</a-entity><!--close slab reset--> \n'

    return outstr

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

    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'

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
            outstr += f'<a-box id="{d["2"]}-{d["num"]}-{v[1]}" \n'
            outstr += f'position="{d["41"]/2} {v[2]*unit(d["43"])} {-v[3]+0.005*unit(d["42"])}" \n'
            outstr += f'scale="{d["rx"]} {v[0]} {v[4]-0.01}" \n'
            outstr += object_material(d)
            outstr += '"></a-box>\n'

    outstr += '</a-entity><!--close wall reset--> \n'
    return outstr

def make_openwall(d):
    outstr = ''

    #make left wall
    d2 = d.copy()
    d2['41'] = d2['door_off_1']
    d2['2'] = 'a-openwall-left'
    outstr += make_wall(d2)
    #make part above door
    d2 = d.copy()
    d2['41'] = d2['door_off_2'] - d2['door_off_1']
    d2['2'] = 'a-openwall-above'
    outstr += f'<a-entity id="{d2["2"]}-{d2["num"]}-ent" \n'
    outstr += f'position="{d2["door_off_1"]} {d2["door_height"]} 0"> \n'
    outstr += make_wall(d2)
    outstr += '</a-entity> \n'
    #make right wall
    d2 = d.copy()
    d2['41'] = d2['41'] - d2['door_off_2']
    d2['2'] = 'a-openwall-right'
    outstr += f'<a-entity id="{d2["2"]}-{d2["num"]}-ent" \n'
    outstr += f'position="{d2["door_off_2"]} 0 0"> \n'
    outstr += make_wall(d2)
    outstr += '</a-entity> \n'

    return outstr

def make_plane(page, d):
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="0 {-d["zg"]-d["zs"]} 0"> \n'
    outstr += make_w_plane(page, d)
    outstr += '</a-entity><!--close plane reset--> \n'
    return outstr

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
    outstr = ''
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
            outstr += f'<a-plane id="{d["2"]}-{d["num"]}-{v[1]}" \n'
            outstr += f'position="0 {v[2]*unit(d["43"])} 0" \n'
            outstr += f'width="{d["rx"]}" height="{v[0]}" \n'
            outstr += object_material(d)
            if page.double_face:
                outstr += 'side: double; '
            outstr += '"></a-plane>\n'

    return outstr

def make_light(page, d):
    #set defaults
    if d['TYPE'] == '':
        d['TYPE'] = 'point'
        d['INTENSITY'] = 0.75
        d['DISTANCE'] = 50
        d['DECAY'] = 2
    if d['COLOR'] == '':
        d['COLOR'] = d['color']

    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}" \n'


    outstr += f'light="type: {d["TYPE"]}; color: {d["COLOR"]}; intensity: {d["INTENSITY"]}; '
    if d['TYPE'] != 'ambient':
        if page.shadows:
            outstr += 'castShadow: true; '
    if d['TYPE'] == 'point' or d['TYPE'] == 'spot':
        outstr += f'decay: {d["DECAY"]}; distance: {d["DISTANCE"]}; '
    if d['TYPE'] == 'spot':
        outstr += f'angle: {d["ANGLE"]}; penumbra: {d["PENUMBRA"]}; '
    if d['TYPE'] == 'directional':
        outstr += f'shadowCameraBottom: {-5*fabs(d["42"])}; \n'
        outstr += f'shadowCameraLeft: {-5*fabs(d["41"])}; \n'
        outstr += f'shadowCameraTop: {5*fabs(d["42"])}; \n'
        outstr += f'shadowCameraRight: {5*fabs(d["41"])}; \n'
    if d['TYPE'] == 'directional' or d['TYPE'] == 'spot':
        outstr += make_light_target(d)
    else:
        outstr += '">\n'

    outstr += '</a-entity> \n'#close light entity
    return outstr

def make_light_target(d):
    outstr = f'target: #light-{d["num"]}-target;"> \n'
    outstr += f'<a-entity id="light-{d["num"]}-target" position="0 -1 0"> </a-entity> \n'
    return outstr

def make_text(d):
    values = (
        ('pool', 0, 'text', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    outstr = ''
    outstr += f'<a-entity id="a-text-{d["num"]}" \n'
    outstr += f'text="width: {d["41"]}; align: {d["ALIGN"]}; color: {d["text_color"]}; '
    outstr += f'value: {d["TEXT"]}; wrap-count: {d["WRAP-COUNT"]}; '
    outstr += '">\n'
    outstr += '</a-entity>\n'
    return outstr

def make_link(page, d):
    outstr = f'<a-link id="a-link-{d["num"]}" \n'
    outstr += f'scale="{d["41"]} {d["43"]} {d["42"]}"\n'
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
        outstr += f'href="{target.url}" \n'
        outstr += f'title="{target.title}" on="click" \n'
        try:
            eq_image = target.specific.equirectangular_image
            if eq_image:
                outstr += f'image="{eq_image.file.url}"'
        except:
            outstr += 'image="#default-sky"'
    else:
        outstr += f'href="{d["LINK"]}" \n'
        outstr += 'title="Sorry, no title" on="click" \n'
        outstr += 'image="#default-sky"'
    outstr += '></a-link>\n'
    return outstr

def unit(nounit):
    #returns positive/negative scaling
    if nounit == 0:
        return 0
    unit = fabs(nounit)/nounit
    return unit

def object_material(d):
    #returns object material
    outstr = ''
    if d['wireframe']:
        outstr += f'material="wireframe: true; wireframe-linewidth: {d["wf_width"]}; color: {d[d["prefix"]+"_color"]}; '
    else:
        outstr += f'material="src: #{d[d["prefix"]+"_image"]}; color: {d[d["prefix"]+"_color"]};'
        if d[d['prefix']+'_repeat']:
            outstr += f' repeat:{d["rx"]} {d["ry"]};'
    return outstr

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
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-object" \n'
    outstr += f'obj-model="obj: #{d["PARAM1"]}-obj; \n'
    outstr += f' mtl: #{d["PARAM1"]}-mtl" \n'
    if d['PARAM2'] == 'scale':
        outstr += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    outstr += '></a-entity><!--close object--> \n'
    outstr += '</a-entity><!--close object reset--> \n'
    return outstr

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
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    d['prefix'] = 'trunk'
    d['rx'] = fabs(d["41"])
    d['ry'] = lt
    outstr += f'<a-entity id="{d["NAME"]}-{d["num"]}-trunk-ent" \n'
    outstr += f'position="0 0 0" \n'
    outstr += f'rotation="{ang} {rot} 0"> \n'
    #outstr += f'<a-animation attribute="rotation" from="{ang} {rot} 0" '
    #outstr += f'to="{ang*gauss(1, .1)} {rot} 0" dur="{int(5000*gauss(1, .5))}" repeat="indefinite" direction="alternate"></a-animation>'
    outstr += f'<a-cone id="{d["NAME"]}-{d["num"]}-trunk" \n'
    outstr += f'position="0 {lt/2} 0" \n'
    outstr += f'geometry="height: {lt}; radius-bottom: {lt/8}; radius-top: {lt/12};" \n'
    outstr += object_material(d)
    outstr += '">\n'
    outstr += '</a-cone> \n'#close trunk
    osc = 30 * gauss(1, .1)
    rot0 = random()*360
    rot00 = random()*360
    rot000 = random()*360
    rot010 = random()*360
    rot10 = random()*360
    rot100 = random()*360
    rot110 = random()*360
    outstr += make_branch('0', l0, lt, osc, rot0, d)
    outstr += make_branch('00', l00, l0, osc, rot00, d)
    outstr += make_branch('000', l000, l00, osc, rot000, d)
    outstr += make_leaves('000', l000, d)
    outstr += '</a-entity> \n'
    outstr += make_branch('001', l001, l00, -osc, 180-rot000, d)
    outstr += make_leaves('001', l001, d)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('01', l01, l0, -osc, 180-rot00, d)
    outstr += make_branch('010', l010, l01, osc, rot010, d)
    outstr += make_leaves('010', l010, d)
    outstr += '</a-entity> \n'
    outstr += make_branch('011', l011, l01, -osc, 180-rot010, d)
    outstr += make_leaves('011', l011, d)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('1', l1, lt, -osc, 180-rot0, d)
    outstr += make_branch('10', l10, l1, osc, rot10, d)
    outstr += make_branch('100', l100, l10, osc, rot100, d)
    outstr += make_leaves('100', l100, d)
    outstr += '</a-entity> \n'
    outstr += make_branch('101', l101, l10, -osc, 180-rot100, d)
    outstr += make_leaves('101', l101, d)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('11', l11, l1, -osc, 180-rot10, d)
    outstr += make_branch('110', l110, l11, osc, rot110, d)
    outstr += make_leaves('110', l110, d)
    outstr += '</a-entity> \n'
    outstr += make_branch('111', l111, l11, -osc, 180-rot110, d)
    outstr += make_leaves('111', l111, d)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'

    outstr += '</a-entity><!--close tree--> \n'
    outstr += '</a-entity><!--close polyline reset--> \n'
    return outstr

def make_branch(branch, lb, lp, angle, rotx, d):
    d['prefix'] = 'branch'
    d['rx'] = fabs(d["41"])
    d['ry'] = lb
    ang = gauss(angle, 10)
    rot = gauss(rotx, 20)
    outstr = f'<a-entity id="{d["TYPE"]}-{d["num"]}-branch-{branch}-ent" \n'
    outstr += f'position="0 {lp*.95-lp*fabs(gauss(0, .2))} 0" \n'
    outstr += f'rotation="{ang} {rot} 0"> \n'
    outstr += f'<a-cone id="{d["TYPE"]}-{d["num"]}-branch-{branch}" \n'
    outstr += f'position="0 {lb/2} 0" \n'
    outstr += f'geometry="height: {lb}; radius-bottom: {lb/12}; radius-top: {lb/14};" \n'
    outstr += object_material(d)
    outstr += '">\n'
    outstr += '</a-cone> \n'#close branch
    return outstr

def make_leaves(branch, lb, d):
    d['prefix'] = 'leaf'
    d['rx'] = lb
    d['ry'] = lb
    outstr = f'<a-sphere id="{d["NAME"]}-{d["num"]}-leaves-{branch}" \n'
    outstr += f'position="0 {lb} 0" \n'
    outstr += f'geometry="radius: {gauss(lb, lb/5)};" \n'
    outstr += object_material(d)
    outstr += 'side: back;">\n'
    outstr += '</a-sphere> \n'#close branch
    return outstr

def make_poly(page, d):
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
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
            outstr += f'<a-entity id="{d["2"]}-{d["num"]}-wall-ent" \n'
            outstr += f'position="{d["vx"][i]-dx/2} 0 {d["vy"][i]-dy/2}" \n'
            outstr += f'rotation="0 {d["50"]} 0"> \n'
            outstr += make_w_plane(page, d)
            outstr +='</a-entity>'
        if d['70']:
            d['num'] = str(d['num1']) + '-' + str(i+1)
            dx = d['vx'][i+1]
            dy = d['vy'][i+1]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            outstr += f'<a-entity id="{d["2"]}-{d["num"]}-wall-ent" \n'
            outstr += f'position="{dx/2} 0 {dy/2}" \n'
            outstr += f'rotation="0 {d["50"]} 0"> \n'
            outstr += make_w_plane(page, d)
            outstr +='</a-entity>'
    else:
        outstr += f'<a-entity id="{d["2"]}-{d["num"]}" \n'
        outstr += f'line="start:0 0 0; \n'
        outstr += f'end:{d["vx"][1]} 0 {d["vy"][1]}; \n'
        outstr += f'color: {d["color"]}" \n'
        for i in range(1, d['90']-1):
            outstr += f'line__{i+1}="start:{d["vx"][i]} 0 {d["vy"][i]}; \n'
            outstr += f'end:{d["vx"][i+1]} 0 {d["vy"][i+1]}; \n'
            outstr += f'color: {d["color"]}" \n'
        if d['70']:
            outstr += f'line__{i+2}=start:{d["vx"][i+1]} 0 {d["vy"][i+1]}; \n'
            outstr += 'end:0 0 0; \n'
            outstr += f'color: {d["color"]}" \n'
        outstr += '></a-entity>'
    outstr += '</a-entity><!--close polyline reset--> \n'
    return outstr

def make_line(page, d):
    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-reset" \n'
    outstr += f'position="{-d["xg"]-d["xs"]} {-d["zg"]-d["zs"]} {-d["yg"]-d["ys"]}"> \n'
    if d['39']:
        d['42'] = 0
        d['43'] = d['39']
        d['41'] = sqrt(pow(d['11'], 2) + pow(d['21'], 2))
        d['50'] = -degrees(atan2(d['21'], d['11']))
        outstr += f'<a-entity id="{d["2"]}-{d["num"]}-wall-ent" \n'
        outstr += f'position="{d["11"]/2} 0 {d["21"]/2}" \n'
        outstr += f'rotation="0 {d["50"]} 0"> \n'
        outstr += make_w_plane(page, d)
        outstr +='</a-entity><!--close wall--> \n'
    else:
        outstr += f'<a-entity id="{d["2"]}-{d["num"]}" \n'
        outstr += 'line="start:0 0 0; \n'
        outstr += f'end:{d["11"]} {d["31"]} {d["21"]}; \n'
        outstr += f'color: {d["color"]};"> \n'
        outstr += '</a-entity><!--close line--> \n'
    outstr += '</a-entity><!--close line reset--> \n'
    return outstr
