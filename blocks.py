"""Collection of functions for writing HTML of blocks.

Functions are referenced from architettura.aframe.make_block, a-block CAD blocks
have TYPE attribute that are essentially block names except for BIM blocks,
that use TYPE attribute for setting 'partition type'. Block appearance is
determined by MATERIAL attribute (multiple components may be used depending on
TYPE), other features depend on PARAM attributes. Some blocks may have
parameters of their own.
"""

from math import degrees, sqrt, pow, fabs, atan2
from random import random, gauss

def make_box(page, d):
    #center position for box like entity
    d['xg'] = d['yg'] = d['zg'] = 0
    d['animation'] = False
    if 'ATTRIBUTE' in d:
        if d['ATTRIBUTE'] == 'stalker' or d['ATTRIBUTE'] == 'checkpoint':
            d['zg'] = d['43']/2
        elif d['ATTRIBUTE'] == 'look-out':
            d['xg'] = d['41']/2
            d['yg'] = d['42']/2
            d['zg'] = d['43']/2
        else:
            d['animation'] = True
    else:
        d['ATTRIBUTE'] = False
        d['xg'] = d['41']/2
        d['yg'] = d['42']/2
        d['zg'] = d['43']/2

    outstr = ''
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-insert" \n'
    outstr += f'position="{d["10"]} {d["30"]} {d["20"]}" \n'
    outstr += f'rotation="{d["210"]} {d["50"]} {d["220"]}"> \n'
    if d['animation']:
        outstr += f'<a-entity id="{d["2"]}-{d["num"]}-animation" \n'
        outstr += f'position="{d["41"]/2} {d["43"]/2} {d["42"]/2}"> \n'
    elif d['ATTRIBUTE'] == 'stalker':
        outstr += f'<a-entity id="{d["2"]}-{d["num"]}-stalker" \n'
        outstr += 'look-at="#camera-foot" \n'
        outstr += f'position="{d["41"]/2} 0 {d["42"]/2}"> \n'
    elif d['ATTRIBUTE'] == 'checkpoint':
        outstr += f'<a-entity id="{d["2"]}-{d["num"]}-checkpoint" \n'
        outstr += 'checkpoint \n'
        outstr += f'position="{d["41"]/2} 0 {d["42"]/2}"> \n'
    #handle
    outstr += f'<a-entity id="{d["2"]}-{d["num"]}-handle" \n'
    outstr += f'position="{d["xg"]} {d["zg"]} {d["yg"]}" \n'
    if page.shadows:
        if data['2'] == 'a-curvedimage':
            outstr += 'shadow="receive: false; cast: false" \n'
        elif data['2'] == 'a-light':
            pass
        else:
            outstr += 'shadow="receive: true; cast: true" \n'
    if d['ATTRIBUTE'] == 'look-at':
        if d['TARGET']:
            outstr += f'look-at="#{d["ID"]}" \n'
        else:
            outstr += 'look-at="#camera" \n'
    outstr += '> \n'
    #finally make box
    values = (
        ('pool', 0, 'box', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    d['prefix'] = 'box'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    outstr += f'<a-box id="{d["2"]}-{d["num"]}" \n'
    outstr += f'scale="{d["rx"]} {d["43"]} {d["ry"]}" \n'
    outstr += object_material(d)
    outstr += '"> \n'
    outstr += '</a-box> \n'
    #make animations (is animation)
    if d['animation']:
        outstr += f'<a-animation attribute="{d["ATTRIBUTE"]}"\n'
        outstr += f'from="{d["FROM"]}"\n'
        outstr += f'to="{d["TO"]}"\n'
        outstr += f'begin="{d["BEGIN"]}"\n'
        outstr += f'direction="{d["DIRECTION"]}"\n'
        outstr += f'repeat="{d["REPEAT"]}"\n'
        outstr += f'dur="{d["DURATION"]}"\n'
        outstr += '></a-animation>\n'
    #make stalker balloon and link TODO
    if d['ATTRIBUTE'] == 'stalker':
        if d['TEXT']:
            length = len(d['TEXT'])
            if length <= 8:
                wrapcount = length+1
            elif length <= 30:
                wrapcount = 10
            else:
                wrapcount = length/3
            outstr += f'<a-entity id="{d["2"]}-{d["num"]}-balloon-ent" \n'
            outstr += f'position="0 {d["43"]/2+d["41"]/4+.1} 0" \n'
            outstr += f'text="width: {d["41"]*.9}; align: center; color: black; '
            outstr += f'value: {d["TEXT"]}; wrap-count: {wrapcount};"> \n'
            outstr += f'<a-cylinder id="{d["2"]}-{d["num"]}-balloon" \n'
            outstr += f'position="0 0 -0.01" \n'
            outstr += f'rotation="90 0 0" \n'
            outstr += f'scale="{fabs(d["41"])/1.5} 0 {fabs(d["41"])/3}"> \n'
            outstr += '</a-cylinder></a-entity>\n'
            outstr += f'<a-triangle id="{d["2"]}-{d["num"]}-triangle" \n'
            outstr += f'geometry="vertexA:0 {d["43"]/2+.1} 0.0005; \n'
            outstr += f'vertexB:0 {d["43"]/2-.05} 0.0005; \n'
            outstr += f'vertexC:{d["41"]/4} {d["43"]/2+.1} 0.0005"> \n'
            outstr += '</a-triangle> \n'
        if d['LINK']:
            outstr += f'<a-link id="{d["2"]}-{d["num"]}-link" \n'
            outstr += f'position="{d["41"]*.7} 0 0.02" \n'
            outstr += f'scale="{d["41"]*.35} {d["41"]*.35}"\n'
            try:
                if d['LINK'] == 'parent':
                    target = page.get_parent()
                elif d['LINK'] == 'child':
                    target = page.get_first_child()
                elif d['LINK'] == 'previous' or data['LINK'] == 'prev':
                    target = page.get_prev_sibling()
                elif d['LINK'] == 'next':
                    target = page.get_next_sibling()
            except:
                target = False
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
            outstr += '>\n'
            outstr += '</a-link>\n'

    outstr += '</a-entity> <!--close handle-->\n'
    if d['animation'] or d['ATTRIBUTE'] == 'stalker' or d['ATTRIBUTE'] == 'checkpoint':
        outstr += '</a-entity> <!--close animation-->\n'
    outstr += '</a-entity> <!--close insertion-->\n'
    return outstr

def make_table_01(data):
    """Table 01, default block (t01)

    A simple table with four legs. Gets dimensions from block scaling, except for
    leg diameter (5cm). Gets top material from first component and leg material
    from third component.
    """
    values = (
        ('pool', 0, 'top', 'MATERIAL'),
        ('pool', 2, 'leg', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)
    outstr = ''
    #table top
    data['prefix'] = 'top'
    data['rx'] = fabs(data["41"])
    data['ry'] = fabs(data["42"])
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-table-top" \n'
    outstr += f'position="0 {data["43"]-0.025*unit(data["43"])} 0" \n'
    outstr += f'scale="{data["rx"]} 0.05 {data["ry"]}" \n'
    outstr += object_material(data)
    outstr += '"></a-box>\n'
    #prepare legs
    data['prefix'] = 'leg'
    scale_x = data["41"]/2-0.05*unit(data["41"])
    scale_y = data["42"]/2-0.05*unit(data["42"])
    height = data["43"]-0.025*unit(data["43"])
    data['rx'] = 1
    data['ry'] = 1
    values = (
        (1, scale_x, scale_y),
        (2, scale_x, -scale_y),
        (3, -scale_x, scale_y),
        (4, -scale_x, -scale_y),
    )
    #make legs
    for v in values:
        outstr += f'<a-cylinder id="{data["2"]}-{data["num"]}-leg-{v[0]}" \n'
        outstr += f'position="{v[1]} {height/2} {v[2]}" \n'
        outstr += 'radius="0.025" \n'
        outstr += f'height="{height}" \n'
        outstr += object_material(data)
        outstr += '"></a-cylinder>\n'

    return outstr

def make_stalker(page, data):
    """Stalker, a look-at image / object with eventual balloon text and link.

    Stalker always looks towards camera. Plane / object dimension is set by
    block X and Z scaling. Image is set by MATERIAL, text is on PARAM3 (sorry,
    no è, à, ; etc.), link tree is on PARAM4 (allowed values: parent, child,
    next, previous). If using an object (obj-stalker), PARAM1 is the object file
    name, if PARAM2 is noscale object won't be scaled.
    """
    values = (
        ('pool', 0, 'stalker', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)
    outstr = ''
    data['prefix'] = 'stalker'
    data['rx'] = fabs(data["41"])
    data['ry'] = fabs(data["43"])
    if data['TYPE'] == 'obj-stalker':
        outstr += f'<a-entity id="stalker-{data["num"]}-object" \n'
        outstr += f'obj-model="obj: #{data["PARAM1"]}-obj; \n'
        outstr += f' mtl: #{data["PARAM1"]}-mtl" \n'
        if data['PARAM2'] == 'noscale':
            outstr += 'scale="1 1 1"> \n'
        else:
            outstr += f'scale="{data["rx"]} {data["ry"]} {fabs(data["42"])}"> \n'
        outstr += '</a-entity>'
    else:
        outstr += f'<a-plane id="{data["TYPE"]}-{data["num"]}" \n'
        outstr += f'position="0 {data["43"]/2} 0" \n'
        outstr += f'width="{data["rx"]}" height="{data["ry"]}" \n'
        outstr += object_material(data)
        outstr += '</a-plane>\n'

    if data['PARAM3']:
        length = len(data['PARAM3'])
        if length <= 8:
            wrapcount = length+1
        elif length <= 30:
            wrapcount = 10
        else:
            wrapcount = length/3
        outstr += f'<a-entity id="stalker-{data["num"]}-balloon-ent" \n'
        outstr += f'position="0 {data["43"]+data["41"]/4+.1} 0" \n'
        outstr += f'text="width: {data["41"]*.9}; align: center; color: black; '
        outstr += f'value: {data["PARAM3"]}; wrap-count: {wrapcount};"> \n'
        outstr += f'<a-cylinder id="stalker-{data["num"]}-balloon" \n'
        outstr += f'position="0 0 -0.01" \n'
        outstr += f'rotation="90 0 0" \n'
        outstr += f'scale="{fabs(data["41"])/1.5} 0 {fabs(data["41"])/3}"> \n'
        outstr += '</a-cylinder></a-entity>\n'
        outstr += f'<a-triangle id="stalker-{data["num"]}-triangle" \n'
        outstr += f'geometry="vertexA:0 {data["43"]+.1} 0.0005; \n'
        outstr += f'vertexB:0 {data["43"]-.05} 0.0005; \n'
        outstr += f'vertexC:{data["41"]/4} {data["43"]+.1} 0.0005"> \n'
        outstr += '</a-triangle> \n'
    if data['PARAM4']:
        try:
            outstr += f'<a-link id="stalker-link-{data["num"]}" \n'
            outstr += f'position="{data["41"]*.7} {data["43"]*.5} 0.02" \n'
            outstr += f'scale="{data["41"]*.35} {data["41"]*.35}"\n'
            if data['PARAM4'] == 'parent':
                target = page.get_parent()
            elif data['PARAM4'] == 'child':
                target = page.get_first_child()
            elif data['PARAM4'] == 'previous' or data['PARAM4'] == 'prev':
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
        ('pool', 0, 'panel', 'MATERIAL'),
        ('pool', 2, 'frame', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)

    outstr = ''
    data['prefix'] = 'frame'
    data['rx'] = 1
    data['ry'] = 1
    #left frame
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-left-frame" \n'
    outstr += f'position="{-0.049*unit(data["41"])} {(data["43"]+0.099*unit(data["43"]))/2} {-data["42"]/2}" \n'
    outstr += 'rotation="0 0 90" \n'
    outstr += f'scale="{fabs(data["43"])+0.099} 0.1 {fabs(data["42"])+0.02}" \n'
    outstr += object_material(data)
    outstr += '></a-box>\n'
    #right frame
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-right-frame" \n'
    outstr += f'position="{data["41"]+0.049*unit(data["41"])} {(data["43"]+0.099*unit(data["43"]))/2} {-data["42"]/2}" \n'
    outstr += 'rotation="0 0 90" \n'
    outstr += f'scale="{fabs(data["43"])+0.099} 0.1 {fabs(data["42"])+0.02}" \n'
    outstr += object_material(data)
    outstr += '></a-box>\n'
    #top frame
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-top-frame" \n'
    outstr += f'position="{data["41"]/2} {data["43"]+0.049*unit(data["43"])} {-data["42"]/2}" \n'
    outstr += f'scale="{fabs(data["41"])-0.002} 0.1 {fabs(data["42"])+0.02}" \n'
    outstr += object_material(data)
    outstr += '></a-box>\n'

    if data["TYPE"] == 'ghost':
        return outstr
    else:
        data['prefix'] = 'panel'
        if eval(data["DOUBLE"]):
            data['rx'] = fabs(data["41"])/2-0.002
        else:
            data['rx'] = fabs(data["41"])-0.002
        data['ry'] = data["43"]-0.001*unit(data["43"])
        if eval(data["SLIDING"]):
            if eval(data["DOUBLE"]):
                #animated slide 1
                outstr += f'<a-entity id="{data["2"]}-{data["num"]}-slide-1"> \n'
                outstr += f'<a-animation attribute="position" from="0 0 0" to="{-(data["41"])/2} 0 0" begin="click" repeat="1" direction="alternate"></a-animation>'
                #moving part 1
                outstr += f'<a-box id="{data["2"]}-{data["num"]}-moving-part-1" \n'
                outstr += f'position="{data["41"]/4} {(data["43"]-0.001*unit(data["43"]))/2} {-data["42"]/2}" \n'
                outstr += f'scale="{(fabs(data["41"]))/2-0.002} {data["43"]-0.001*unit(data["43"])} 0.05" \n'
                outstr += object_material(data)
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
                outstr += object_material(data)
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
                outstr += object_material(data)
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
                outstr += object_material(data)
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
                outstr += object_material(data)
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
                outstr += object_material(data)
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
        ('pool', 0, 'ceiling', 'MATERIAL'),
        ('pool', 2, 'floor', 'MATERIAL'),
    )
    data = prepare_material_values(values, data)
    outstr = ''
    data['prefix'] = 'floor'
    data['rx'] = fabs(data["41"])
    data['ry'] = fabs(data["42"])
    #floor
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-floor" \n'
    outstr += f'position="{data["41"]/2} {-0.005*unit(data["43"])} {-data["42"]/2}" \n'
    outstr += f'scale="{data["rx"]} 0.01 {data["ry"]}" \n'
    outstr += object_material(data)
    outstr += '"></a-box>\n'
    #ceiling
    data['prefix'] = 'ceiling'
    outstr += f'<a-box id="{data["2"]}-{data["num"]}-ceiling" \n'
    outstr += f'position="{data["41"]/2} {-data["43"]/2-0.005*unit(data["43"])} {-data["42"]/2}" \n'
    outstr += f'scale="{data["rx"]} {fabs(data["43"])-0.01} {data["ry"]}" \n'
    outstr += object_material(data)
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
            data['prefix'] = v[5]
            data['rx'] = fabs(data["41"])
            data['ry'] = v[0]
            outstr += f'<a-box id="{data["2"]}-{data["num"]}-{v[1]}" \n'
            outstr += f'position="{data["41"]/2} {v[2]*unit(data["43"])} {-v[3]+0.005*unit(data["42"])}" \n'
            outstr += f'scale="{data["rx"]} {v[0]} {v[4]-0.01}" \n'
            outstr += object_material(data)
            outstr += '"></a-box>\n'

    return outstr

def make_w_plane(data):
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
    data = prepare_material_values(values, data)
    #prepare height values
    wall_h = fabs(data['43'])
    tile_h = fabs(float(data['TILING']))
    skirt_h = fabs(float(data['SKIRTING']))
    if tile_h > wall_h:
        tile_h = wall_h
    if skirt_h > wall_h:
        skirt_h = wall_h
    if skirt_h > tile_h:
        tile_h = skirt_h
    wall_h = wall_h - tile_h
    tile_h = tile_h - skirt_h
    outstr = ''
    #open displacement entity
    if data['animation'] == False:
        outstr += f'<a-entity id="{data["2"]}-{data["num"]}-disp" \n'
        outstr += f'position="{data["41"]/2} 0 0"> \n'
    #prepare values for surfaces
    values = (
        (skirt_h, 'skirt', skirt_h/2,),
        (tile_h, 'tile', tile_h/2+skirt_h,),
        (wall_h, 'wall', wall_h/2+tile_h+skirt_h,),
    )
    #loop surfaces
    data['rx'] = fabs(data["41"])
    for v in values:
        if v[0]:
            data['prefix'] = v[1]
            data['ry'] = v[0]
            outstr += f'<a-plane id="{data["2"]}-{data["num"]}-{v[1]}" \n'
            outstr += f'position="0 {v[2]*unit(data["43"])} 0" \n'
            outstr += f'width="{data["rx"]}" height="{v[0]}" \n'
            outstr += object_material(data)
            outstr += '"></a-plane>\n'
    #close displacement entity
    if data['animation'] == False:
        outstr += '</a-entity> \n'
    return outstr

def unit(nounit):
    #returns positive/negative scaling
    if nounit == 0:
        return 0
    unit = fabs(nounit)/nounit
    return unit

def object_material(data):
    #returns object material
    outstr = ''
    if data['wireframe']:
        outstr += f'material="wireframe: true; wireframe-linewidth: {data["wf_width"]}; color: {data[data["prefix"]+"_color"]}; '
    else:
        outstr += f'material="src: #{data[data["prefix"]+"_image"]}; color: {data[data["prefix"]+"_color"]}'
        if data[data['prefix']+'_repeat']:
            outstr += f'; repeat:{data["rx"]} {data["ry"]}'
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
    """
    outstr = ''
    outstr += f'<a-entity id="{data["2"]}-{data["num"]}-object" \n'
    outstr += f'obj-model="obj: #{data["PARAM1"]}-obj; \n'
    outstr += f' mtl: #{data["PARAM1"]}-mtl" \n'
    if data['PARAM2'] == 'noscale':
        outstr += 'scale="1 1 1"> \n'
    else:
        outstr += f'scale="{fabs(data["41"])} {fabs(data["43"])} {fabs(data["42"])}"> \n'
    outstr += '</a-entity>'
    return outstr

def make_tree(data):
    """Tree block

    Gets dimensions from block scaling. Gets trunk material from first
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
    outstr = ''
    data['prefix'] = 'trunk'
    data['rx'] = fabs(data["41"])
    data['ry'] = lt
    outstr += f'<a-entity id="{data["TYPE"]}-{data["num"]}-trunk-ent" \n'
    outstr += f'position="0 0 0" \n'
    outstr += f'rotation="{ang} {rot} 0"> \n'
    #outstr += f'<a-animation attribute="rotation" from="{ang} {rot} 0" '
    #outstr += f'to="{ang*gauss(1, .1)} {rot} 0" dur="{int(5000*gauss(1, .5))}" repeat="indefinite" direction="alternate"></a-animation>'
    outstr += f'<a-cone id="{data["TYPE"]}-{data["num"]}-trunk" \n'
    outstr += f'position="0 {lt/2} 0" \n'
    outstr += f'geometry="height: {lt}; radius-bottom: {lt/8}; radius-top: {lt/12};" \n'
    outstr += object_material(data)
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
    outstr += make_branch('0', l0, lt, osc, rot0, data)
    outstr += make_branch('00', l00, l0, osc, rot00, data)
    outstr += make_branch('000', l000, l00, osc, rot000, data)
    outstr += make_leaves('000', l000, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('001', l001, l00, -osc, 180-rot000, data)
    outstr += make_leaves('001', l001, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('01', l01, l0, -osc, 180-rot00, data)
    outstr += make_branch('010', l010, l01, osc, rot010, data)
    outstr += make_leaves('010', l010, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('011', l011, l01, -osc, 180-rot010, data)
    outstr += make_leaves('011', l011, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('1', l1, lt, -osc, 180-rot0, data)
    outstr += make_branch('10', l10, l1, osc, rot10, data)
    outstr += make_branch('100', l100, l10, osc, rot100, data)
    outstr += make_leaves('100', l100, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('101', l101, l10, -osc, 180-rot100, data)
    outstr += make_leaves('101', l101, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += make_branch('11', l11, l1, -osc, 180-rot10, data)
    outstr += make_branch('110', l110, l11, osc, rot110, data)
    outstr += make_leaves('110', l110, data)
    outstr += '</a-entity> \n'
    outstr += make_branch('111', l111, l11, -osc, 180-rot110, data)
    outstr += make_leaves('111', l111, data)
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'
    outstr += '</a-entity> \n'

    outstr += '</a-entity> \n'
    return outstr

def make_branch(branch, lb, lp, angle, rotx, data):
    data['prefix'] = 'branch'
    data['rx'] = fabs(data["41"])
    data['ry'] = lb
    ang = gauss(angle, 10)
    rot = gauss(rotx, 20)
    outstr = f'<a-entity id="{data["TYPE"]}-{data["num"]}-branch-{branch}-ent" \n'
    outstr += f'position="0 {lp*.95-lp*fabs(gauss(0, .2))} 0" \n'
    outstr += f'rotation="{ang} {rot} 0"> \n'
    outstr += f'<a-cone id="{data["TYPE"]}-{data["num"]}-branch-{branch}" \n'
    outstr += f'position="0 {lb/2} 0" \n'
    outstr += f'geometry="height: {lb}; radius-bottom: {lb/12}; radius-top: {lb/14};" \n'
    outstr += object_material(data)
    outstr += '">\n'
    outstr += '</a-cone> \n'#close branch
    return outstr

def make_leaves(branch, lb, data):
    data['prefix'] = 'leaf'
    data['rx'] = lb
    data['ry'] = lb
    outstr = f'<a-sphere id="{data["TYPE"]}-{data["num"]}-leaves-{branch}" \n'
    outstr += f'position="0 {lb} 0" \n'
    outstr += f'geometry="radius: {gauss(lb, lb/5)};" \n'
    outstr += object_material(data)
    outstr += 'side: back;">\n'
    outstr += '</a-sphere> \n'#close branch
    return outstr

def make_poly(data):
    outstr = ''
    if data['39']:
        data['animation'] = False
        data['42'] = 0
        data['43'] = data['39']
        data['num1'] = data['num']
        for i in range(data['90']-1):
            data['num'] = str(data['num1']) + '-' + str(i)
            dx = data['vx'][i]-data['vx'][i+1]
            dy = data['vy'][i]-data['vy'][i+1]
            data['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            data['50'] = 180-degrees(atan2(dy, dx))
            outstr += f'<a-entity id="{data["2"]}-{data["num"]}-wall-ent" \n'
            outstr += f'position="{data["vx"][i]} 0 {data["vy"][i]}" \n'
            outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}"> \n'
            outstr += make_w_plane(data)
            outstr +='</a-entity>'
        if data['70']:
            data['num'] = str(data['num1']) + '-' + str(i+1)
            dx = data['vx'][i+1]-data['vx'][0]
            dy = data['vy'][i+1]-data['vy'][0]
            data['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            data['50'] = 180-degrees(atan2(dy, dx))
            outstr += f'<a-entity id="{data["2"]}-{data["num"]}-wall-ent" \n'
            outstr += f'position="{data["vx"][i+1]} {data["38"]} {data["vy"][i+1]}" \n'
            outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}"> \n'
            outstr += make_w_plane(data)
            outstr +='</a-entity>'
    else:
        outstr += f'<a-entity id="{data["2"]}-{data["num"]}" \n'
        outstr += f'line="start:{data["vx"][0]} {data["38"]} {data["vy"][0]}; \n'
        outstr += f'end:{data["vx"][1]} {data["38"]} {data["vy"][1]}; \n'
        outstr += f'color: {data["color"]}" \n'
        for i in range(1, data['90']-1):
            outstr += f'line__{i+1}="start:{data["vx"][i]} {data["38"]} {data["vy"][i]}; \n'
            outstr += f'end:{data["vx"][i+1]} {data["38"]} {data["vy"][i+1]}; \n'
            outstr += f'color: {data["color"]}" \n'
        if data['70']:
            outstr += f'line__{i+2}=start:{data["vx"][i+1]} {data["38"]} {data["vy"][i+1]}; \n'
            outstr += f'end:{data["vx"][0]} {data["38"]} {data["vy"][0]}; \n'
            outstr += f'color: {data["color"]}" \n'
        outstr += '></a-entity>'
    return outstr

def make_line(data):
    outstr = ''
    if data['39']:
        data['animation'] = False
        data['42'] = 0
        data['43'] = data['39']
        data['41'] = sqrt(pow(data['11'], 2) + pow(data['21'], 2))
        data['50'] = -degrees(atan2(data['21'], data['11']))
        outstr += f'<a-entity id="{data["2"]}-{data["num"]}-wall-ent" \n'
        outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}"> \n'
        outstr += make_w_plane(data)
        outstr +='</a-entity>'
    else:
        outstr = f'<a-entity id="{data["2"]}-{data["num"]}" \n'
        outstr += 'line="start:0 0 0; \n'
        outstr += f'end:{data["11"]} {data["31"]} {data["21"]}; \n'
        outstr += f'color: {data["color"]};"> \n'
        outstr += '</a-entity> \n'
    return outstr
