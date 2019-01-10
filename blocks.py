"""Collection of functions for writing HTML of blocks.

Functions are referenced from architettura.aframe.make_block, a-block CAD blocks
have TYPE attribute that are essentially block names except for BIM blocks,
that use TYPE attribute for setting 'partition type'. Block appearance is
determined by MATERIAL attribute (multiple components may be used depending on
TYPE), other features depend on PARAM attributes. Some blocks may have
parameters of their own.
"""

from math import fabs
from random import random, gauss

def make_table_01(data):
    """Table 01, default block (t01)

    A simple table with four legs. Gets dimensions from block scaling, except for
    leg diameter (5cm). Gets top material from first component and leg material
    from third component.
    """
    values = (
        ('pool', 2, 'leg', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)

    outstr = ''#blocks need to close wrapper
    #table top
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-table-top" \n'
    outstr += f'position="0 {data["43"]-0.025*unit(data["43"])} 0" \n'
    outstr += f'scale="{fabs(data["41"])} 0.05 {fabs(data["42"])}" \n'
    outstr += f'material="src: #{data["8"]}; color: {data["color"]} '
    outstr += is_repeat(data["repeat"], fabs(data["41"]), fabs(data["42"]))
    outstr += '"></a-box>\n'
    data['leg'] = data["43"]-0.025*unit(data["43"])
    scale_x = data["41"]/2-0.05*unit(data["41"])
    scale_y = data["42"]/2-0.05*unit(data["42"])
    #first leg
    outstr += f'<a-cylinder id="{data["2"]}-{data["num"]}-leg-1" \n'
    outstr += f'position="{scale_x} {data["leg"]/2} {scale_y}" \n'
    outstr += close_leg(data)
    #second leg
    outstr += f'<a-cylinder id="{data["2"]}-{data["num"]}-leg-2" \n'
    outstr += f'position="{scale_x} {data["leg"]/2} {-scale_y}" \n'
    outstr += close_leg(data)
    #third leg
    outstr += f'<a-cylinder id="{data["2"]}-{data["num"]}-leg-3" \n'
    outstr += f'position="{-scale_x} {data["leg"]/2} {scale_y}" \n'
    outstr += close_leg(data)
    #fourth leg
    outstr += f'<a-cylinder id="{data["2"]}-{data["num"]}-leg-4" \n'
    outstr += f'position="{-scale_x} {data["leg"]/2} {-scale_y}" \n'
    outstr += close_leg(data)

    return outstr

def close_leg(data):
    #repetitive task in making tables
    outstr = 'radius="0.025" \n'
    outstr += f'height="{data["leg"]}" \n'
    outstr += f'material="src: #{data["leg_image"]}; color: {data["leg_color"]} '
    outstr += '"></a-cylinder>\n'
    return outstr

def make_stalker(page, data):
    """Stalker, a look-at image with eventual balloon text and link.

    Stalker always looks towards camera. Plane dimension is set by block X and Z
    scaling. Image is set by MATERIAL, text is on PARAM1 (sorry, no è, à, ; etc.),
    link tree is on PARAM2 (allowed values: parent, child, next, previous).
    """
    outstr = 'look-at="#camera-foot"> \n'#blocks need to close wrapper
    outstr += f'<a-plane id="{data["TYPE"]}-{data["num"]}" \n'
    outstr += f'position="0 {data["43"]/2} 0" \n'
    outstr += f'width="{fabs(data["41"])}" height="{fabs(data["43"])}" \n'
    outstr += entity_material(data)
    outstr += '</a-plane>\n'
    if data['PARAM1']:
        length = len(data['PARAM1'])
        if length <= 8:
            wrapcount = length+1
        elif length <= 30:
            wrapcount = 10
        else:
            wrapcount = length/3
        outstr += f'<a-entity id="stalker-{data["num"]}-balloon-ent" \n'
        outstr += f'position="0 {data["43"]+data["41"]/4+.1} 0" \n'
        outstr += f'text="width: {data["41"]*.9}; align: center; color: black; '
        outstr += f'value: {data["PARAM1"]}; wrap-count: {wrapcount};"> \n'
        outstr += f'<a-cylinder id="stalker-{data["num"]}-balloon" \n'
        outstr += f'position="0 0 -0.01" \n'
        outstr += f'rotation="90 0 0" \n'
        outstr += f'scale="{fabs(data["41"])/1.5} 0 {fabs(data["41"])/3}"> \n'
        outstr += '</a-cylinder></a-entity>\n'
        outstr += f'<a-triangle id="stalker-triangle-{data["num"]}" \n'
        outstr += f'geometry="vertexA:0 {data["43"]+.1} 0.0005; \n'
        outstr += f'vertexB:0 {data["43"]-.05} 0.0005; \n'
        outstr += f'vertexC:{data["41"]/4} {data["43"]+.1} 0.0005"> \n'
        outstr += '</a-triangle> \n'
    if data['PARAM2']:
        try:
            outstr += f'<a-link id="stalker-link-{data["num"]}" \n'
            outstr += f'position="{data["41"]*.7} {data["43"]*.5} 0.02" \n'
            outstr += f'scale="{data["41"]*.35} {data["41"]*.35}"\n'
            if data['PARAM2'] == 'parent':
                target = page.get_parent()
            elif data['PARAM2'] == 'child':
                target = page.get_first_child()
            elif data['PARAM2'] == 'previous' or data['PARAM2'] == 'prev':
                target = page.get_prev_sibling()
            else:#we default to next sibling
                target = page.get_next_sibling()

            outstr += f'href="{target.url}"\n'
            outstr += f'title="{target.title}" on="click"\n'
            try:
                eq_image = target.specific.equirectangular_image
                if eq_image:
                    outstr += f'image="{eq_image.file.url}"'
            except:
                outstr += 'image="#default-sky"'
            outstr += '>\n'
            outstr += '</a-link>\n'
        except:
            pass

    return outstr

def make_door(data):
    """Door default BIM block.

    A simple framed door. Gets dimensions from block scaling, except for frame
    dimension. TYPE sets door features. If set to 'ghost' panel will not be
    rendered. SLIDING and DOUBLE are boolean. Gets panel material from first
    component and frame material from third component.
    """
    values = (
        ('pool', 2, 'frame', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)

    outstr = ''#blocks need to close wrapper

    #left frame
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-left-frame" \n'
    outstr += f'position="{-0.049*unit(data["41"])} {(data["43"]+0.099*unit(data["43"]))/2} {-data["42"]/2}" \n'
    outstr += 'rotation="0 0 90" \n'
    outstr += f'scale="{fabs(data["43"])+0.099} 0.1 {fabs(data["42"])+0.02}" \n'
    outstr += f'material="src: #{data["frame_image"]}; color: {data["frame_color"]}">'
    outstr += '</a-box>\n'
    #right frame
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-right-frame" \n'
    outstr += f'position="{data["41"]+0.049*unit(data["41"])} {(data["43"]+0.099*unit(data["43"]))/2} {-data["42"]/2}" \n'
    outstr += 'rotation="0 0 90" \n'
    outstr += f'scale="{fabs(data["43"])+0.099} 0.1 {fabs(data["42"])+0.02}" \n'
    outstr += f'material="src: #{data["frame_image"]}; color: {data["frame_color"]}">'
    outstr += '</a-box>\n'
    #top frame
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-top-frame" \n'
    outstr += f'position="{data["41"]/2} {data["43"]+0.049*unit(data["43"])} {-data["42"]/2}" \n'
    outstr += f'scale="{fabs(data["41"])-0.002} 0.1 {fabs(data["42"])+0.02}" \n'
    outstr += f'material="src: #{data["frame_image"]}; color: {data["frame_color"]}">'
    outstr += '</a-box>\n'

    if data["TYPE"] == 'ghost':
        return outstr
    else:
        if eval(data["SLIDING"]):
            if eval(data["DOUBLE"]):
                #animated slide 1
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-slide-1"> \n'
                outstr += f'<a-animation attribute="position" from="0 0 0" to="{-(data["41"])/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part-1" \n'
                outstr += f'position="{data["41"]/4} {(data["43"]-0.001*unit(data["43"]))/2} {-data["42"]/2}" \n'
                outstr += f'scale="{(fabs(data["41"]))/2-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
                outstr += is_repeat(data["repeat"], (fabs(data["41"]))/2-0.002, data["43"]-0.001*unit(data["43"]))
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                #animated slide 2
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-slide-2" \n'
                outstr += f'position="{data["41"]} 0 0"> \n'
                outstr += f'<a-animation attribute="position" from="{data["41"]} 0 0" to="{(data["41"])*3/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 2
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part-2" \n'
                outstr += f'position="{-data["41"]/4} {(data["43"]-0.001*unit(data["43"]))/2} {-data["42"]/2}" \n'
                outstr += f'scale="{(fabs(data["41"]))/2-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
                outstr += is_repeat(data["repeat"], (fabs(data["41"]))/2-0.002, data["43"]-0.001*unit(data["43"]))
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                return outstr
            else:#single
                #animated slide
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-slide"> \n'
                outstr += f'<a-animation attribute="position" from="0 0 0" to="{-data["41"]} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part" \n'
                outstr += f'position="{data["41"]/2} {(data["43"]-0.001*unit(data["43"]))/2} {-data["42"]/2}" \n'
                outstr += f'scale="{fabs(data["41"])-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
                outstr += is_repeat(data["repeat"], fabs(data["41"])-0.002, data["43"]-0.001*unit(data["43"]))
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                return outstr
        else:#hinged
            if eval(data["DOUBLE"]):
                #animated hinge 1
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-hinge-1"> \n'
                outstr += f'<a-animation attribute="rotation" from="0 0 0" to="0 {-90*unit(data["41"])*unit(data["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part-1" \n'
                outstr += f'position="{data["41"]/4} {(data["43"]-0.001*unit(data["43"]))/2} {-0.025*unit(data["42"])}" \n'
                outstr += f'scale="{(fabs(data["41"]))/2-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
                outstr += is_repeat(data["repeat"], (fabs(data["41"]))/2-0.002, data["43"]-0.001*unit(data["43"]))
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                #animated hinge 2
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-hinge-2" '
                outstr += f'position="{data["41"]} 0 0"> \n'
                outstr += f'<a-animation attribute="rotation" from="0 0 0" to="0 {90*unit(data["41"])*unit(data["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 2
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part-2" \n'
                outstr += f'position="{-data["41"]/4} {(data["43"]-0.001*unit(data["43"]))/2} {-0.025*unit(data["42"])}" \n'
                outstr += f'scale="{(fabs(data["41"]))/2-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
                outstr += is_repeat(data["repeat"], (fabs(data["41"]))/2-0.002, data["43"]-0.001*unit(data["43"]))
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                return outstr
            else:#single
                #animated hinge
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-hinge"> \n'
                outstr += f'<a-animation attribute="rotation" from="0 0 0" to="0 {-90*unit(data["41"])*unit(data["42"])} 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part" \n'
                outstr += f'position="{data["41"]/2} {(data["43"]-0.001*unit(data["43"]))/2} {-0.025*unit(data["42"])}" \n'
                outstr += f'scale="{fabs(data["41"])-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
                outstr += is_repeat(data["repeat"], fabs(data["41"])-0.002, data["43"]-0.001*unit(data["43"]))
                outstr += '"></a-box>\n'
                outstr += '</a-entity>\n'
                return outstr

def make_slab(data):
    """Slab default BIM block.

    An horizontal partition. Gets dimensions from block scaling. TYPE sets
    partition type (TODO). Gets ceiling material from first component and
    floor material from third component.
    """
    values = (
        ('pool', 2, 'floor', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)

    #floor
    outstr = f'<a-box id="{data["2"]}-{data["num"]}-floor" \n'
    outstr += f'position="{data["41"]/2} {-0.005*unit(data["43"])} {-data["42"]/2}" \n'
    outstr += f'scale="{fabs(data["41"])} 0.01 {fabs(data["42"])}" \n'
    outstr += f'material="src: #{data["floor_image"]}; color: {data["floor_color"]}'
    outstr += is_repeat(data["floor_repeat"], data["41"], data["42"])
    outstr += '"></a-box>\n'
    #ceiling
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-ceiling" \n'
    outstr += f'position="{data["41"]/2} {-data["43"]/2-0.005*unit(data["43"])} {-data["42"]/2}" \n'
    outstr += f'scale="{fabs(data["41"])} {fabs(data["43"])-0.01} {fabs(data["42"])}" \n'
    outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
    outstr += is_repeat(data["repeat"], data["41"], data["42"])
    outstr += '"></a-box>\n'

    return outstr

def make_wall(data):
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
    data = prepare_material_values(values, data)
    wall_h = wall2_h = fabs(data['43'])
    tile_h = fabs(float(data['TILING']))
    skirt_h = fabs(float(data['SKIRTING']))
    tile2_h = fabs(float(data['TILING2']))
    skirt2_h = fabs(float(data['SKIRTING2']))
    if data['2'] == 'a-openwall-above':
        door_h = data['door_height']
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
    values = (
        (skirt_h, 'int-skirt', skirt_h/2, data["42"]/2, fabs(data["42"]), 'skirt'),
        (tile_h, 'int-tile', tile_h/2+skirt_h, data["42"]/2, fabs(data["42"]), 'tile'),
        (wall_h, 'int-wall', wall_h/2+tile_h+skirt_h, data["42"]/2, fabs(data["42"]), 'wall'),
        (skirt2_h, 'ext-skirt', skirt2_h/2, data["42"], 0.02, 'skirt2'),
        (tile2_h, 'ext-tile', tile2_h/2+skirt2_h, data["42"], 0.02, 'tile2'),
        (wall2_h, 'ext-wall', wall2_h/2+tile2_h+skirt2_h, data["42"], 0.02, 'wall2'),
    )
    for v in values:
        if v[0]:
            outstr += f'<a-box id="{data["2"]}-{data["num"]}-{v[1]}" \n'
            outstr += f'position="{data["41"]/2} {v[2]*unit(data["43"])} {-v[3]+0.005*unit(data["42"])}" \n'
            outstr += f'scale="{fabs(data["41"])} {v[0]} {v[4]-0.01}" \n'
            outstr += f'material="src: #{data[v[5]+"_image"]}; color: {data[v[5]+"_color"]}'
            outstr += is_repeat(data[v[5]+"_repeat"], data["41"], v[0])
            outstr += '"></a-box>\n'

    return outstr

def unit(nounit):
    #returns positive/negative scaling
    unit = fabs(nounit)/nounit
    return unit

def is_repeat(repeat, rx, ry):
    #returns repeat attribute for images
    if repeat:
        output = f'; repeat:{fabs(rx)} {fabs(ry)}'
        return output
    else:
        return ';'

def entity_material(data):
    #returns entity material
    outstr = f'material="src: #{data["8"]}; color: {data["color"]}'
    outstr += is_repeat(data["repeat"], data["41"], data["43"])
    outstr += '">\n'
    return outstr

def prepare_material_values(values, data):

    for v in values:
        try:
            component_pool = data[v[0]]
            component = component_pool[v[1]]
            data[v[2]+'_color'] = component[1]
            data[v[2]+'_image'] = data[v[3]] + '-' + component[0]
            data[v[2]+'_repeat'] = component[2]

        except:
            data[v[2]+'_color'] = data['color']
            data[v[2]+'_image'] = data['8']
            data[v[2]+'_repeat'] = data['repeat']

    return data

def make_object(data):
    """Object block

    Block loads a Object Model (Wavefront) along with it's *.mtl file. PARAM1
    must be equal to *.obj and *.mtl filename (use lowercase extension). Files
    must share same filename and must be loaded in the media/document folder.
    If PARAM2 is set to 'noscale', object will not be scaled.
    If set, MATERIAL attribute is alternative to MTL.
    """
    outstr = ''
    outstr += f'<a-entity id="{data["2"]}-{data["num"]}-object" \n'
    outstr += f'obj-model="obj: #{data["PARAM1"]}-obj; \n'
    if data['MATERIAL']:
        outstr += f'" material="src: #{data["8"]}; color: {data["color"]}" \n'
    else:
        outstr += f' mtl: #{data["PARAM1"]}-mtl" \n'
    if data['PARAM2'] == 'noscale':
        outstr += 'scale="1 1 1"> \n'
    else:
        outstr += f'scale="{fabs(data["41"])} {fabs(data["43"])} {fabs(data["42"])}"> \n'
    outstr += '</a-entity>'
    return outstr

def make_tree(data):
    """Tree block

    TODO. Gets dimensions from block scaling. Gets trunk material from first
    component, branch from second and leaves from third.
    """
    values = (
        ('pool', 0, 'trunk', 'MATERIAL'),
        ('pool', 1, 'branch', 'MATERIAL'),
        ('pool', 2, 'leaf', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)
    ht = 0.7172 * data['43'] * gauss(1, .1)
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
    outstr = f'<a-entity id="{data["TYPE"]}-{data["num"]}-trunk-ent" \n'
    outstr += f'position="0 0 0" \n'
    outstr += f'rotation="{ang} {rot} 0"> \n'
    #outstr += f'<a-animation attribute="rotation" from="{ang} {rot} 0" '
    #outstr += f'to="{ang*gauss(1, .1)} {rot} 0" dur="{int(5000*gauss(1, .5))}" repeat="indefinite" direction="alternate"></a-animation>'
    outstr += f'<a-cone id="{data["TYPE"]}-{data["num"]}-trunk" \n'
    outstr += f'position="0 {lt/2} 0" \n'
    outstr += f'geometry="height: {lt}; radius-bottom: {lt/8}; radius-top: {lt/12};" \n'
    outstr += f'material="src: #{data["trunk_image"]}; color: {data["trunk_color"]}'
    outstr += is_repeat(data["trunk_repeat"], data["41"], lt)
    outstr += '">\n'
    outstr += '</a-cone> \n'#close trunk
    osc = 30 * gauss(1, .1)
    outstr += make_branch('0', l0, lt, osc, data)
    outstr += make_branch('00', l00, l0, osc, data)
    outstr += make_branch('000', l000, l00, osc, data)
    outstr += make_leaves('000', l000, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('001', l001, l00, -osc, data)
    outstr += make_leaves('001', l001, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('01', l01, l0, -osc, data)
    outstr += make_branch('010', l010, l01, osc, data)
    outstr += make_leaves('010', l010, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('011', l011, l01, -osc, data)
    outstr += make_leaves('011', l011, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('1', l1, lt, -osc, data)
    outstr += make_branch('10', l10, l1, osc, data)
    outstr += make_branch('100', l100, l10, osc, data)
    outstr += make_leaves('100', l100, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('101', l101, l10, -osc, data)
    outstr += make_leaves('101', l101, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('11', l11, l1, -osc, data)
    outstr += make_branch('110', l110, l11, osc, data)
    outstr += make_leaves('110', l110, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('111', l111, l11, -osc, data)
    outstr += make_leaves('111', l111, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'

    outstr += '</a-entity> \n'
    return outstr

def make_branch(branch, lb, lp, angle, data):
    ang = gauss(angle, 10)
    rot = random()*360
    outstr = f'<a-entity id="{data["TYPE"]}-{data["num"]}-branch-{branch}-ent" \n'
    outstr += f'position="0 {lp*.95-lp*fabs(gauss(0, .2))} 0" \n'
    outstr += f'rotation="{ang} {rot} 0"> \n'
    outstr += f'<a-cone id="{data["TYPE"]}-{data["num"]}-branch-{branch}" \n'
    outstr += f'position="0 {lb/2} 0" \n'
    outstr += f'geometry="height: {lb}; radius-bottom: {lb/12}; radius-top: {lb/14};" \n'
    outstr += f'material="src: #{data["branch_image"]}; color: {data["branch_color"]}'
    outstr += is_repeat(data["branch_repeat"], data["41"], lb)
    outstr += '">\n'
    outstr += '</a-cone> \n'#close branch
    return outstr

def make_leaves(branch, lb, data):
    outstr = f'<a-icosahedron id="{data["TYPE"]}-{data["num"]}-leaves-{branch}" \n'
    outstr += f'position="0 {lb} 0" \n'
    outstr += f'geometry="radius: {gauss(lb, lb/5)};" \n'
    outstr += f'material="src: #{data["leaf_image"]}; color: {data["leaf_color"]}'
    outstr += is_repeat(data["leaf_repeat"], lb, lb)
    outstr += 'side: back;">\n'
    outstr += '</a-icosahedron> \n'#close branch
    return outstr
