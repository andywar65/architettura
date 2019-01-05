"""Collection of functions for writing HTML of blocks.

Functions are referenced from architettura.aframe.make_block, a-block CAD blocks
have TYPE attribute that are essentially block names except for BIM blocks,
that use TYPE attribute for setting 'partition type'. Block appearance is
determined by MATERIAL attribute (multiple components may be used depending on
TYPE), other features depend on PARAM attributes. Some blocks may have
parameters of their own.
"""

from math import fabs

def make_table_01(data):
    """Table 01, default block (t01)

    A simple table with four legs. Gets dimensions from block scaling, except for
    leg diameter (5cm). Gets top material from first component and leg material
    from third component.
    """
    try:
        component_pool = data['pool']
        component = component_pool[2]#gets third component for legs
        data['leg_color'] = component[1]
        data['leg_image'] = data['MATERIAL'] + '-' + component[0]
    except:
        data['leg_color'] = data['color']
        data['leg_image'] = data['8']

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
    scaling. Image is set by MATERIAL, text is on PARAM1, link tree is on PARAM2
    (allowed values: parent, child, next, previous).
    """
    outstr = 'look-at="#camera-foot"> \n'#blocks need to close wrapper
    outstr += f'<a-plane id="{data["TYPE"]}-{data["num"]}" \n'
    outstr += f'position="0 {data["43"]/2} 0" \n'
    outstr += f'width="{fabs(data["41"])}" height="{fabs(data["43"])}" \n'
    outstr += entity_material(data)
    outstr += '</a-plane>\n'
    if data['PARAM1']:
        outstr += f'<a-plane id="stalker-balloon-{data["num"]}" \n'
        outstr += f'position="0 {data["43"]+data["41"]/4+.1} 0.01" \n'
        outstr += f'width="{fabs(data["41"])}" height="{fabs(data["41"])/2}" \n'
        outstr += f'text="width: {data["41"]*.9}; align: center; color: black; '
        outstr += f'value: {data["PARAM1"]}; wrap-count: {data["41"]*9}; '
        outstr += '">\n</a-plane>\n'
        outstr += f'<a-triangle id="stalker-triangle-{data["num"]}" \n'
        outstr += f'geometry="vertexA:0 {data["43"]+.1} 0.01; \n'
        outstr += f'vertexB:0 {data["43"]-.05} 0.01; \n'
        outstr += f'vertexC:{data["41"]/4} {data["43"]+.1} 0.01"> \n'
        outstr += '</a-triangle> \n'
    if data['PARAM2']:
        outstr += f'<a-link id="stalker-link-{data["num"]}" \n'
        outstr += f'position="{data["41"]*.7} {data["43"]*.25} 0.02" \n'
        outstr += f'scale="{data["41"]*.25} {data["41"]*.25}"\n'
        if data['PARAM2'] == 'parent':
            target = page.get_parent()
        elif data['PARAM2'] == 'child':
            target = page.get_first_child()
        elif data['PARAM2'] == 'previous' or data['tree'] == 'prev':
            target = page.get_prev_sibling()
        else:#we default to next sibling
            target = page.get_next_sibling()
        try:
            if target:
                outstr += f'href="{target.url}"\n'
                outstr += f'title="{target.title}" on="click"\n'
                try:
                    eq_image = target.specific.equirectangular_image
                    if eq_image:
                        outstr += f'image="{eq_image.file.url}"'
                except:
                    outstr += 'image="#default-sky"'
        except:
            pass
        outstr += '>\n'
        outstr += '</a-link>\n'
    return outstr

def make_door(data):
    """Door default BIM block.

    A simple framed door. Gets dimensions from block scaling, except for frame
    dimension. TYPE sets door features. If set to 'ghost' panel will not be
    rendered. SLIDING and DOUBLE are boolean. Gets panel material from first
    component and frame material from third component.
    """
    try:
        component_pool = data['pool']
        component = component_pool[2]#gets third component for frame
        data['frame_color'] = component[1]
        data['frame_image'] = data['MATERIAL'] + '-' + component[0]
    except:
        data['frame_color'] = data['color']
        data['frame_image'] = data['8']

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
    try:
        component_pool = data['pool']
        component = component_pool[2]#gets third component for floor
        data['floor_color'] = component[1]
        data['floor_image'] = data['MATERIAL'] + '-' + component[0]
        data['floor_repeat'] = component[2]
    except:
        data['floor_color'] = data['color']
        data['floor_image'] = data['8']
        data['floor_repeat'] = data['repeat']

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
    data = prepare_wall_values(data)
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

def prepare_wall_values(data):
    values = (
        ('pool', 0, 'wall', 'MATERIAL'),
        ('pool', 1, 'tile', 'MATERIAL'),
        ('pool', 2, 'skirt', 'MATERIAL'),
        ('pool2', 0, 'wall2', 'MATERIAL2'),
        ('pool2', 1, 'tile2', 'MATERIAL2'),
        ('pool2', 2, 'skirt2', 'MATERIAL2'),
    )
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
    If set, MATERIAL attribute is alternative to MTL.
    """
    outstr = ''
    outstr += f'<a-entity id="{data["2"]}-{data["num"]}-object" \n'
    outstr += f'obj-model="obj: #{data["PARAM1"]}-obj; \n'
    if data['MATERIAL']:
        outstr += f'" material="src: #{data["8"]}; color: {data["color"]}" \n'
    else:
        outstr += f' mtl: #{data["PARAM1"]}-mtl" \n'
    outstr += f'scale="{fabs(data["41"])} {fabs(data["43"])} {fabs(data["42"])}"> \n'
    outstr += '</a-entity>'
    return outstr
