"""Collection of functions for writing HTML of entities and blocks.

Functions are referenced from architettura.aframe.make_html, a-block CAD blocks
have NAME attribute that are essentially block names, while BIM blocks use PART
attribute for setting 'partition type'. Block appearance is determined by
MATERIAL attribute (multiple components may be used depending on NAME), other
features depend on PARAM attributes.
"""

from math import degrees, sqrt, pow, fabs, atan2, sin, cos, radians
from random import random, gauss

def make_camera(page, d):
    oput = f'<a-entity id="camera-ent" position="{d["10"]} {d["30"]} {d["20"]}" \n'
    oput += f'rotation="{d["210"]} {d["50"]} {d["220"]}" \n'
    if page.mode == 'digkom':
        oput += 'movement-controls="controls: checkpoint" checkpoint-controls="mode: animate"> \n'
        oput += f'<a-camera id="camera" look-controls="pointerLockEnabled: true" wasd-controls="enabled: false" '
    else:
        oput += '> \n'
        oput += f'<a-camera id="camera" look-controls="pointerLockEnabled: true" wasd-controls="fly: {str(page.fly_camera).lower() }" '
    oput += f' position="0 {d["43"]*1.6} 0"> \n'
    oput += '<a-cursor color="#2E3A87"></a-cursor> \n'
    oput += f'<a-light type="point" distance="10" intensity="{d["LIGHT-INT"]}"></a-light> \n'
    oput += f'<a-entity position="0 {-d["43"]*1.6} 0" id="camera-foot"></a-entity> \n'
    oput += '</a-camera></a-entity> \n'
    return oput

def make_box(page, d):
    #d['prefix'] = 'box'
    #values = (
        #('pool', 0, d['prefix'], 'MATERIAL'),
    #)
    #d = prepare_material_values(values, d)

    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["43"])
    d['dx'] = d['41']/2
    d['dy'] = -d['42']/2
    d['dz'] = d['43']/2
    #d['tag'] = 'a-box'
    d['ide'] = 'box'
    identity = open_entity(page, d)
    geometry = f'primitive: {d["ide"]}; '
    geometry += f'width: {round(d["41"], 4)}; '
    geometry += f'height: {round(d["43"], 4)}; '
    geometry += f'depth: {round(d["42"], 4)}; '
    repeat=f'repeat: {round(d["rx"], 4)} {round(d["ry"], 4)}; '
    page.ent_dict[identity].update(geometry=geometry, layer=d['layer'],
        closing=close_entity(page, d), material=d['MATERIAL'], component=0,
        repeat=repeat, tag='a-entity')

    return

def make_block(page, d):

    d['dx'] = d['dy'] = 0
    d['dz'] = d['43']/2
    d['tag'] = 'a-entity'
    d['ide'] = 'block'
    oput = ''
    oput += open_entity(page, d)
    oput += '> \n'

    if d['NAME'] == 't01':
        oput += make_table_01(d)
    elif d['NAME'] == 'obj-mtl':
        oput += make_object(d)
    elif d['NAME'] == 'gltf':
        oput += make_object(d)
    elif d['NAME'] == 'tree':
        oput += make_tree(d)

    oput += close_entity(page, d)

    return oput

def make_bim_block(page, d):

    d['dx'] = d['41']/2
    d['dy'] = -d['42']/2
    if d['2'] == 'a-slab':
        d['dz'] = -d['43']/2
    else:
        d['dz'] = d['43']/2
    d['tag'] = 'a-entity'
    d['ide'] = 'block'
    oput = ''
    oput += open_entity(page, d)
    oput += '> \n'

    if d['2'] == 'a-wall':
        d['ide'] = 'wall'
        oput += make_wall(d)
    elif d['2'] == 'a-slab':
        oput += make_slab(d)
    elif d['2'] == 'a-door':
        oput += make_door(d)
    elif d['2'] == 'a-window':
        oput += make_window(d)
    elif d['2'] == 'a-stair':
        oput += make_stair(page, d)
    elif d['2'] == 'a-openwall':
        oput += make_openwall(d)

    oput += close_entity(page, d)

    return oput

def make_circular(page, d):
    #d['prefix'] = d['ide'] = d['2'].replace('a-', '')
    #values = (
        #('pool', 0, d['prefix'], 'MATERIAL'),
    #)
    #d = prepare_material_values(values, d)

    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    d['dx'] = 0
    d['dy'] = 0
    if d['2'] == 'a-sphere':
        d['dz'] = d['43']
    elif d['2'] == 'a-circle':
        d['dz'] = 0
    else:
        d['dz'] = d['43']/2
    #d['tag'] = d['2']
    d['ide'] = d['2'].replace('a-', '')
    identity = open_entity(page, d)
    geometry = f'primitive: {d["ide"]}; '
    if d['2'] == 'a-circle':
        geometry += f'radius: {fabs(d["41"])}; '
    else:
        geometry += f'width: {round(d["41"], 4)}; '
        geometry += f'height: {round(d["43"], 4)}; '
        geometry += f'depth: {round(d["42"], 4)}; '
    geometry += entity_geometry(d)
    repeat=f'repeat: {round(d["rx"], 4)} {round(d["ry"], 4)}; '
    page.ent_dict[identity].update(geometry=geometry, layer=d['layer'],
        closing=close_entity(page, d), material=d['MATERIAL'], component=0,
        repeat=repeat, tag='a-entity')

    return

def make_curvedimage(page, d):
    d['ide'] = 'curvedimage'
    d['rx'] = 1
    d['ry'] = 1
    d['dx'] = 0
    d['dy'] = 0
    d['dz'] = d['43']/2
    identity = open_entity(page, d)
    geometry = f'radius: {round(fabs(d["41"]), 4)*2}; '
    geometry += f'height: {round(d["43"], 4)}; '
    geometry += entity_geometry(d)
    repeat=f'repeat: {round(d["rx"], 4)} {round(d["ry"], 4)}; '
    page.ent_dict[identity].update(geometry=geometry, layer=d['layer'],
        closing=close_entity(page, d), material=d['MATERIAL'], component=0,
        repeat=repeat, tag='a-curvedimage')

    return

def make_plane(page, d):
    d['ide'] = 'plane'
    d['dx'] = d['41']/2
    d['dy'] = 0
    d['dz'] = d['43']/2
    d['tag'] = 'a-entity'
    identity = open_entity(page, d)
    page.ent_dict[identity].update(layer=d['layer'], closing=0, tag=d['tag'])
    d['closing'] = close_entity(page, d)
    make_w_plane(page, d)

    return

def make_w_plane(page, d):
    """Wall plane default BIM block.

    A vertical surface. Gets dimensions from plane scaling, TILING and
    SKIRTING height from respective attributes. Gets MATERIAL with 3 components,
    first for wall, second for tiling and third for skirting.
    """
    #prepare values for materials
    #values = (
        #('pool', 0, 'plaster', 'MATERIAL'),
        #('pool', 1, 'tile', 'MATERIAL'),
        #('pool', 2, 'skirt', 'MATERIAL'),
    #)
    #d = prepare_material_values(values, d)
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

    #prepare values for surfaces
    values = (
        (skirt_h, 'skirt', skirt_h/2, 2),
        (tile_h, 'tile', tile_h/2+skirt_h, 1),
        (wall_h, 'plaster', wall_h/2+tile_h+skirt_h, 0),
    )
    #loop surfaces
    d['rx'] = fabs(d["41"])

    for v in values:
        if v[0]:
            d['ry'] = v[0]
            identity = f'{page.id}-{d["ide"]}-{d["num"]}-{v[1]}'
            geometry = 'primitive: plane; '
            geometry += f'width: {round(d["rx"], 4)}; height: {v[0]}; '
            repeat = f'repeat: {round(d["rx"], 4)} {v[0]}; '
            position=f'0 {round(v[2]*unit(d["43"])-d["43"]/2, 4)} 0'
            page.ent_dict[identity]={'position': position, 'geometry': geometry,
                'material': d['MATERIAL'], 'repeat': repeat, 'component': v[0],
                'closing': 1, 'layer': d['layer'], 'tag': 'a-entity'}
    #last one closes all
    page.ent_dict[identity].update(closing=d['closing']+1)

    return

def survey_w_plane(d):
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
    values = (
        (wall_h, 'plaster', d['MATERIAL'], d['pool'], 0),
        (tile_h, 'tile', d['MATERIAL'], d['pool'], 1),
        (skirt_h, 'skirt', d['MATERIAL'], d['pool'], 2),
    )
    for v in values:
        if v[0]:
            oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
            try:
                component = v[3][v[4]]
                name = component[0]
            except:
                name = 'Null'
            oput += f'<td>{d["ide"]}-{v[1]}</td><td>{v[2]}</td><td>{name}</td>'
            oput += f'<td>{round(fabs(d["41"]), 4)}</td>'
            oput += f'<td>{round(v[0], 4)}</td>'
            oput += f'<td>-</td><td>-</td><td>-</td>'
            oput += '<td>-</td><td>-</td></tr> \n'
    return oput

def survey_line(d):
    oput = ''
    if d['39']:
        d['43'] = d['39']
        d['41'] = sqrt( pow(d['10'] - d['11'], 2) + pow(d['20'] - d['21'], 2))
        oput += survey_w_plane(d)
    return oput

def survey_poly(d):
    oput = ''
    if d['39']:
        d['43'] = d['39']
        d['num1'] = d['num']
        for i in range(d['90']-1):
            d['num'] = str(d['num1']) + '-' + str(i)
            dx = d['vx'][i]-d['vx'][i+1]
            dy = d['vy'][i]-d['vy'][i+1]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            oput += survey_w_plane(d)
        if d['70']:
            d['num'] = str(d['num1']) + '-' + str(i+1)
            dx = d['vx'][i+1]-d['vx'][0]
            dy = d['vy'][i+1]-d['vy'][0]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            oput += survey_w_plane(d)
    return oput

def make_triangle(page, d):
    d['10b'] = d['10']
    d['20b'] = d['20']
    d['30b'] = d['30']
    d['10'] = (d['10b']+d['11']+d['12'])/3
    d['20'] = (d['20b']+d['21']+d['22'])/3
    d['30'] = (d['30b']+d['31']+d['32'])/3
    dict = {'10':('10b', '11', '12'), '20':('20b', '21', '22'), '30':('30b', '31', '32')}
    for key, value in dict.items():
        d[value[0]] = d[value[0]] - d[key]
        d[value[1]] = d[value[1]] - d[key]
        d[value[2]] = d[value[2]] - d[key]
    d['ide'] = 'triangle'
    d['rx'] = 1
    d['ry'] = 1
    d['dx'] = d['dy'] = d['dz'] = 0
    identity = open_entity(page, d)
    geometry = f'vertexA:{round(d["10b"], 4)} {round(d["30b"], 4)} {round(d["20b"], 4)}; '
    geometry += f'vertexB:{round(d["11"], 4)} {round(d["31"], 4)} {round(d["21"], 4)}; '
    geometry += f'vertexC:{round(d["12"], 4)} {round(d["32"], 4)} {round(d["22"], 4)}'
    material = d.get('MATERIAL', '')
    page.ent_dict[identity].update(geometry=geometry, layer=d['layer'],
        closing=close_entity(page, d), material=material, component=0,
        tag='a-triangle')

    return

def make_line(page, d):
    d['10b'] = d['10']
    d['20b'] = d['20']
    d['30b'] = d['30']
    d['10'] = (d['10b']+d['11'])/2
    d['20'] = (d['20b']+d['21'])/2
    d['30'] = (d['30b']+d['31'])/2
    #normalize vertices
    dict = {'10':('10b', '11'), '20':('20b', '21'), '30':('30b', '31')}
    for key, value in dict.items():
        d[value[0]] = d[value[0]] - d[key]
        d[value[1]] = d[value[1]] - d[key]
    if d['39']:
        d['30'] = d['30'] + d['39']/2
    d['dx'] = d['dy'] = d['dz'] = 0
    d['prefix'] = d['ide'] = 'line'
    d['tag'] = 'a-entity'
    oput = ''
    oput += open_entity(page, d)
    if d['39']:
        oput += '> \n'
        d['42'] = 0
        d['43'] = d['39']
        d['41'] = sqrt(pow(d['11'], 2) + pow(d['21'], 2))*2
        d['50'] = -degrees(atan2(d['21'], d['11']))
        oput += f'<a-entity id="{d["prefix"]}-{d["num"]}-wall-ent" \n'
        oput += f'rotation="0 {round(d["50"], 4)} 0"> \n'
        oput += make_w_plane(page, d)
        oput +='</a-entity><!--close wall--> \n'
    else:
        oput += f'line="start:{round(d["10b"], 4)} {round(d["30b"], 4)} {round(d["20b"], 4)}; \n'
        oput += f'end:{round(d["11"], 4)} {round(d["31"], 4)} {round(d["21"], 4)}; \n'
        oput += f'color: {d["color"]};"> \n'
    oput += close_entity(page, d)

    return oput

def make_poly(page, d):
    #normalize vertices relative to first
    for i in range(1, d['90']):
        d['vx'][i] = d['vx'][i]-d['vx'][0]
        d['vy'][i] = d['vy'][i]-d['vy'][0]
    d['vx'][0] = 0
    d['vy'][0] = 0
    #find gravity center
    xmax = xmin = 0
    ymax = ymin = 0
    for i in range(d['90']):
        if d['vx'][i] < xmin:
            xmin = d['vx'][i]
        elif d['vx'][i] > xmax:
            xmax = d['vx'][i]
        if d['vy'][i] < ymin:
            ymin = d['vy'][i]
        elif d['vy'][i] > ymax:
            ymax = d['vy'][i]
    d['dx'] = (xmax + xmin)/2
    d['dy'] = (ymax + ymin)/2
    d['39'] = d.get('39', 0)
    d['dz'] = d['39']/2

    #normalize vertices to gravity center
    for i in range(d['90']):
        d['vx'][i] = d['vx'][i]-d['dx']
        d['vy'][i] = d['vy'][i]-d['dy']
    d['prefix'] = d['ide'] = 'poly'
    d['tag'] = 'a-entity'
    d['num1'] = d['num']
    oput = ''
    oput += open_entity(page, d)
    if d['39']:
        oput += '> \n'
        d['42'] = 0
        d['43'] = d['39']
        for i in range(d['90']-1):
            d['num'] = str(d['num1']) + '-' + str(i)
            dx = d['vx'][i]-d['vx'][i+1]
            dy = d['vy'][i]-d['vy'][i+1]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            oput += f'<a-entity id="{d["ide"]}-{d["num"]}-wall-ent" \n'
            oput += f'position="{round(d["vx"][i]-dx/2, 4)} 0 {round(d["vy"][i]-dy/2, 4)}" \n'
            oput += f'rotation="0 {round(d["50"], 4)} 0"> \n'
            oput += make_w_plane(page, d)
            oput +='</a-entity>'
        if d['70']:
            d['num'] = str(d['num1']) + '-' + str(i+1)
            dx = d['vx'][i+1]-d['vx'][0]
            dy = d['vy'][i+1]-d['vy'][0]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            oput += f'<a-entity id="{d["ide"]}-{d["num"]}-wall-ent" \n'
            oput += f'position="{round(d["vx"][i+1]-dx/2, 4)} 0 {round(d["vy"][i+1]-dy/2, 4)}" \n'
            oput += f'rotation="0 {round(d["50"], 4)} 0"> \n'
            oput += make_w_plane(page, d)
            oput +='</a-entity>'
        d['num'] = d['num1']
    else:
        for i in range(d['90']-1):
            oput += f'line__{i+1}="start:{round(d["vx"][i], 4)} 0 {round(d["vy"][i], 4)}; \n'
            oput += f'end:{round(d["vx"][i+1], 4)} 0 {round(d["vy"][i+1], 4)}; \n'
            oput += f'color: {d["color"]}" \n'
        if d['70']:
            oput += f'line__{i+2}="start:{round(d["vx"][i+1], 4)} 0 {round(d["vy"][i+1], 4)}; \n'
            oput += f'end:{round(d["vx"][0], 4)} 0 {round(d["vy"][0], 4)}; \n'
            oput += f'color: {d["color"]}" \n'
        oput += '>'
    oput += close_entity(page, d)
    return oput

def make_table_01(d):
    """Table 01, default block (t01)

    A simple table with four legs. Gets dimensions from block scaling, except for
    leg diameter (5cm). Gets top material from first component and leg material
    from third component.
    """
    values = (
        ('pool', 2, 'top', 'MATERIAL'),
        ('pool', 1, 'leg', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    oput = ''

    #table top
    d['prefix'] = 'top'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    oput += f'<a-box id="table01-{d["num"]}-top" \n'
    oput += f'position="0 {d["43"]/2-0.025*unit(d["43"])} 0" \n'
    oput += f'scale="{d["rx"]} 0.05 {d["ry"]}" \n'
    oput += entity_material(d)
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
        oput += f'<a-cylinder id="table01-{d["num"]}-leg-{v[0]}" \n'
        oput += f'position="{v[1]} {(height-d["43"])/2} {v[2]}" \n'
        oput += 'radius="0.025" \n'
        oput += f'height="{height}" \n'
        oput += entity_material(d)
        oput += '"></a-cylinder>\n'

    return oput

def make_door(d):
    """Door default BIM block.

    A simple framed door. Gets dimensions from block scaling, except for frame
    dimension. PART sets door features. If set to 'ghost' panel will not be
    rendered. SLIDING and DOUBLE are boolean. Gets panel material from first
    component and frame material from third component.
    """
    values = (
        ('pool', 0, 'panel', 'MATERIAL'),
        ('pool', 2, 'frame', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)

    oput = ''
    if d["PART"] == 'ghost':
        return oput

    d['prefix'] = 'frame'
    d['rx'] = 1
    d['ry'] = 1
    #left frame
    oput += f'<a-box id="door-{d["num"]}-left-frame" \n'
    oput += f'position="{-0.049*unit(d["41"])-d["41"]/2} {0.099*unit(d["43"])/2} 0" \n'
    oput += 'rotation="0 0 90" \n'
    oput += f'scale="{fabs(d["43"])+0.099} 0.1 {fabs(d["42"])+0.02}" \n'
    oput += entity_material(d)
    oput += '"></a-box>\n'
    #right frame
    oput += f'<a-box id="door-{d["num"]}-right-frame" \n'
    oput += f'position="{d["41"]/2+0.049*unit(d["41"])} {0.099*unit(d["43"])/2} 0" \n'
    oput += 'rotation="0 0 90" \n'
    oput += f'scale="{fabs(d["43"])+0.099} 0.1 {fabs(d["42"])+0.02}" \n'
    oput += entity_material(d)
    oput += '"></a-box>\n'
    #top frame
    oput += f'<a-box id="door-{d["num"]}-top-frame" \n'
    oput += f'position="0 {d["43"]/2+0.049*unit(d["43"])} 0" \n'
    oput += f'scale="{fabs(d["41"])-0.002} 0.1 {fabs(d["42"])+0.02}" \n'
    oput += entity_material(d)
    oput += '"></a-box>\n'

    d['prefix'] = 'panel'
    if eval(d["DOUBLE"]):
        d['rx'] = fabs(d["41"])/2-0.002
    else:
        d['rx'] = fabs(d["41"])-0.002
    d['ry'] = d["43"]-0.001*unit(d["43"])
    if eval(d["SLIDING"]):
        if eval(d["DOUBLE"]):
            #animated slide 1
            oput += f'<a-entity id="door-{d["num"]}-slide-1" \n'
            oput += f'position="{-d["41"]/2} {-d["43"]/2} 0" \n'
            oput += f'animation="property: position; easing: easeInOutQuad; from:{-d["41"]/2} {-d["43"]/2} 0; to:{-d["41"]+0.01} {-d["43"]/2} 0; startEvents: click; loop: 1; dir: alternate;"> \n'
            #moving part 1
            oput += f'<a-box id="door-{d["num"]}-moving-part-1" \n'
            oput += f'position="{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} 0" \n'
            oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'
            oput += '</a-entity>\n'
            #animated slide 2
            oput += f'<a-entity id="door-{d["num"]}-slide-2" \n'
            oput += f'position="{d["41"]/2} {-d["43"]/2} 0" \n'
            oput += f'animation="property: position; easing: easeInOutQuad; from:{d["41"]/2} {-d["43"]/2} 0; to:{d["41"]-0.01} {-d["43"]/2} 0; startEvents: click; loop: 1; dir: alternate;"> \n'
            #moving part 2
            oput += f'<a-box id="door-{d["num"]}-moving-part-2" \n'
            oput += f'position="{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} 0" \n'
            oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'
            oput += '</a-entity>\n'
            return oput
        else:#single
            #animated slide
            oput += f'<a-entity id="door-{d["num"]}-slide" \n'
            oput += f'position="{-d["41"]/2} {-d["43"]/2} 0" \n'
            oput += f'animation="property: position; easing: easeInOutQuad; from:{-d["41"]/2} {-d["43"]/2} 0; to:{-d["41"]*3/2+0.01} {-d["43"]/2} 0; startEvents: click; loop: 1; dir: alternate;"> \n'
            #moving part
            oput += f'<a-box id="door-{d["num"]}-moving-part" \n'
            oput += f'position="{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} 0" \n'
            oput += f'scale="{fabs(d["41"])-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'
            oput += '</a-entity>\n'
            return oput
    else:#hinged
        if eval(d["DOUBLE"]):
            #animated hinge 1
            oput += f'<a-entity id="door-{d["num"]}-hinge-1" \n'
            oput += f'position="{-d["41"]/2} {-d["43"]/2} {d["42"]/2}" \n'
            oput += f'animation="property: rotation; easing: easeInOutQuad; from:0 0 0; to:0 {-90*unit(d["41"])*unit(d["42"])} 0; startEvents: click; loop: 1; dir: alternate;"> \n'
            #moving part 1
            oput += f'<a-box id="door-{d["num"]}-moving-part-1" \n'
            oput += f'position="{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
            oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'
            oput += '</a-entity>\n'
            #animated hinge 2
            oput += f'<a-entity id="door-{d["num"]}-hinge-2" '
            oput += f'position="{d["41"]/2} {-d["43"]/2} {d["42"]/2}" \n'
            oput += f'animation="property: rotation; easing: easeInOutQuad; from:0 0 0; to:0 {90*unit(d["41"])*unit(d["42"])} 0; startEvents: click; loop: 1; dir: alternate;"> \n'
            #moving part 2
            oput += f'<a-box id="door-{d["num"]}-moving-part-2" \n'
            oput += f'position="{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
            oput += f'scale="{(fabs(d["41"]))/2-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'
            oput += '</a-entity>\n'
            return oput
        else:#single
            #animated hinge
            oput += f'<a-entity id="door-{d["num"]}-hinge" \n'
            oput += f'position="{-d["41"]/2} {-d["43"]/2} {d["42"]/2}" \n'
            oput += f'animation="property: rotation; easing: easeInOutQuad; from:0 0 0; to:0 {-90*unit(d["41"])*unit(d["42"])} 0; startEvents: click; loop: 1; dir: alternate;"> \n'
            #moving part
            oput += f'<a-box id="door-{d["num"]}-moving-part" \n'
            oput += f'position="{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}" \n'
            oput += f'scale="{fabs(d["41"])-0.002} {d["43"]-0.001*unit(d["43"])} 0.05" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'
            oput += '</a-entity>\n'
            return oput

def make_slab(d):
    """Slab default BIM block.

    An horizontal partition. Gets dimensions from block scaling. PART sets
    partition type (TODO). Gets ceiling material from first component and
    floor material from third component.
    """
    values = (
        ('pool', 0, 'ceiling', 'MATERIAL'),
        ('pool', 2, 'floor', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    oput = ''

    d['prefix'] = 'floor'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    #floor
    oput += f'<a-box id="slab-{d["num"]}-floor" \n'
    oput += f'position="0 {-0.005*unit(d["43"])+d["43"]/2} 0" \n'
    oput += f'scale="{d["rx"]} 0.01 {d["ry"]}" \n'
    oput += entity_material(d)
    oput += '"></a-box>\n'
    #ceiling
    d['prefix'] = 'ceiling'
    oput += f'<a-box id="slab-{d["num"]}-ceiling" \n'
    oput += f'position="0 {-0.005*unit(d["43"])} 0" \n'
    oput += f'scale="{d["rx"]} {fabs(d["43"])-0.01} {d["ry"]}" \n'
    oput += entity_material(d)
    oput += '"></a-box>\n'

    return oput

def survey_slab(d):
    #partitions
    #this part equal to survey_wall except 42-43, output unit_weight
    unit_weight = 0
    if d['p-pool']:
        total_thickness = 0
        var_thickness = -1
        for x, component in d['p-pool'].items():
            thickness = float(component[1]/1000)
            weight = float(component[2])
            if thickness == 0:
                var_thickness = x
            total_thickness = total_thickness + thickness
            unit_weight = unit_weight + weight*thickness
        if total_thickness == d['43']:
            unit_weight = round(unit_weight*d['41']*d['42']*d['43'], 4)
        elif total_thickness > d['43']:
            unit_weight = 'Thin'
        elif total_thickness < d['43'] and var_thickness > -1:
            component = d['p-pool'][var_thickness]
            thickness = d['43'] - total_thickness
            weight = float(component[2])
            unit_weight = unit_weight + weight*thickness
            unit_weight = round(unit_weight*d['41']*d['42']*d['43'], 4)
        else:
            unit_weight = 'Thick'
    #next part is identical in survey wall
    oput = ''
    oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
    oput += f'<td>{d["ide"]}</td><td>-</td><td>-</td>'
    oput += f'<td>{round(fabs(d["41"]), 4)}</td>'
    oput += f'<td>{round(fabs(d["43"]), 4)}</td>'
    oput += f'<td>{round(fabs(d["42"]), 4)}</td>'
    oput += f'<td>{d["PART"]}</td><td>{unit_weight}</td>'
    oput += '<td>-</td><td>-</td></tr> \n'

    values = (
        (0, 'floor', d['MATERIAL'], d['pool'], 2),
        (0, 'ceiling', d['MATERIAL'], d['pool'], 0),
    )
    for v in values:
        oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
        try:
            component = v[3][v[4]]
            name = component[0]
        except:
            name = 'Null'
        oput += f'<td>{d["ide"]}-{v[1]}</td><td>{v[2]}</td><td>{name}</td>'
        oput += f'<td>{round(fabs(d["41"]), 4)}</td><td>-</td>'
        oput += f'<td>{round(fabs(d["42"]), 4)}</td>'
        oput += '<td>-</td><td>-</td><td>-</td><td>-</td></tr> \n'

    return oput

def make_wall(d):
    """Wall default BIM block.

    A vertical partition. Gets dimensions from block scaling, TILING and
    SKIRTING height from respective attributes. PART sets partition type
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
    if d['ide'] == 'openwall-above':
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
    values = (
        (skirt_h, 'int-skirt', skirt_h/2, d["42"]/2, fabs(d["42"]), 'skirt'),
        (tile_h, 'int-tile', tile_h/2+skirt_h, d["42"]/2, fabs(d["42"]), 'tile'),
        (wall_h, 'int-plaster', wall_h/2+tile_h+skirt_h, d["42"]/2, fabs(d["42"]), 'wall'),
        (skirt2_h, 'ext-skirt', skirt2_h/2, d["42"], 0.02, 'skirt2'),
        (tile2_h, 'ext-tile', tile2_h/2+skirt2_h, d["42"], 0.02, 'tile2'),
        (wall2_h, 'ext-plaster', wall2_h/2+tile2_h+skirt2_h, d["42"], 0.02, 'wall2'),
    )
    for v in values:
        if v[0]:
            d['prefix'] = v[5]
            d['rx'] = fabs(d["41"])
            d['ry'] = v[0]
            oput += f'<a-box id="{d["ide"]}-{d["num"]}-{v[1]}" \n'
            oput += f'position="0 {v[2]*unit(d["43"])-d["43"]/2} {-v[3]+0.005*unit(d["42"])+d["42"]/2}" \n'
            oput += f'scale="{d["rx"]} {v[0]} {v[4]-0.01}" \n'
            oput += entity_material(d)
            oput += '"></a-box>\n'

    return oput

def survey_door(d):
    oput = ''
    values = (
        (0, 'panel', d['MATERIAL'], d['pool'], 0),
        (0, 'frame', d['MATERIAL'], d['pool'], 2),
    )

    for v in values:
        oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
        try:
            component = v[3][v[4]]
            name = component[0]
        except:
            name = 'Null'
        oput += f'<td>{d["ide"]}-{v[1]}</td><td>{v[2]}</td><td>{name}</td>'
        oput += f'<td>{round(fabs(d["41"]), 4)}</td>'
        oput += f'<td>{round(fabs(d["43"]), 4)}</td>'
        oput += f'<td>-</td><td>{d["PART"]}</td><td>-</td>'
        oput += f'<td>{d["DOUBLE"]}</td><td>{d["SLIDING"]}</td></tr> \n'
    return oput

def survey_window(d):
    oput = ''
    if d['SILL'] == '':
        d['SILL'] = 0
    else:
        d['SILL'] = float(d['SILL'])
    oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
    try:
        component = d['wpool'][2]
        name = component[0]
    except:
        name = 'Null'
    oput += f'<td>{d["ide"]}-frame</td><td>{d["WMATERIAL"]}</td><td>{name}</td>'
    oput += f'<td>{round(fabs(d["41"]), 4)}</td>'
    oput += f'<td>{round(fabs(d["43"]) - fabs(d["SILL"]), 4)}</td>'
    oput += f'<td>-</td><td>{d["PART"]}</td><td>-</td>'
    oput += f'<td>{d["DOUBLE"]}</td><td>-</td></tr> \n'
    if d['SILL']:
        d['43'] = d['SILL']
        d['ide'] = 'window-under'
        oput += survey_wall(d)

    return oput

def survey_wall(d):
    #partitions
    unit_weight = 0
    if d['p-pool']:
        total_thickness = 0
        var_thickness = -1
        for x, component in d['p-pool'].items():
            thickness = float(component[1]/1000)
            weight = float(component[2])
            if thickness == 0:
                var_thickness = x
            total_thickness = total_thickness + thickness
            unit_weight = unit_weight + weight*thickness
        if total_thickness == d['42']:
            unit_weight = round(unit_weight*d['41']*d['42']*d['43'], 4)
        elif total_thickness > d['42']:
            unit_weight = 'Thin'
        elif total_thickness < d['42'] and var_thickness > -1:
            component = d['p-pool'][var_thickness]
            thickness = d['42'] - total_thickness
            weight = float(component[2])
            unit_weight = unit_weight + weight*thickness
            unit_weight = round(unit_weight*d['41']*d['42']*d['43'], 4)
        else:
            unit_weight = 'Thick'

    #materials
    wall_h = wall2_h = fabs(d['43'])
    tile_h = fabs(float(d['TILING']))
    skirt_h = fabs(float(d['SKIRTING']))
    tile2_h = fabs(float(d['TILING2']))
    skirt2_h = fabs(float(d['SKIRTING2']))
    if d['ide'] == 'openwall-above':
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
    oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
    oput += f'<td>{d["ide"]}</td><td>-</td><td>-</td>'
    oput += f'<td>{round(fabs(d["41"]), 4)}</td>'
    oput += f'<td>{round(fabs(d["43"]), 4)}</td>'
    oput += f'<td>{round(fabs(d["42"]), 4)}</td>'
    oput += f'<td>{d["PART"]}</td><td>{unit_weight}</td>'
    oput += '<td>-</td><td>-</td></tr> \n'
    values = (
        (wall_h, 'int-plaster', d['MATERIAL'], d['pool'], 0),
        (tile_h, 'int-tile', d['MATERIAL'], d['pool'], 1),
        (skirt_h, 'int-skirt', d['MATERIAL'], d['pool'], 2),
        (wall2_h, 'ext-plaster', d['MATERIAL2'], d['pool2'], 0),
        (tile2_h, 'ext-tile', d['MATERIAL2'], d['pool2'], 1),
        (skirt2_h, 'ext-skirt', d['MATERIAL2'], d['pool2'], 2),
    )
    for v in values:
        if v[0]:
            oput += f'<tr><td>{d["num"]}</td><td>{d["layer"]}</td>'
            try:
                component = v[3][v[4]]
                name = component[0]
            except:
                name = 'Null'
            oput += f'<td>{d["ide"]}-{v[1]}</td><td>{v[2]}</td><td>{name}</td>'
            oput += f'<td>{round(fabs(d["41"]), 4)}</td>'
            oput += f'<td>{round(v[0], 4)}</td>'
            oput += f'<td>-</td><td>-</td><td>-</td>'
            oput += '<td>-</td><td>-</td></tr> \n'

    return oput

def make_stair(page, d):
    values = (
        ('pool', 0, 'steps', 'MATERIAL'),
        ('pool', 2, 'railings', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    oput = ''
    d['prefix'] = 'steps'
    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["42"])
    if d['STEPS']:
        na = int(d['STEPS'])
        np = na-1
    else:
        #attempts to find the 2a+p=63 relationship
        na = d['43'] / 0.05
        if int(na) != na:
            na = int(na) + 1
        flag = False
        while na > 1:
            np = na-1
            diff = (2*d["43"]/na+d["42"]/np)-.63
            if fabs(diff) <= 0.01:
                flag = True
            else:
                na -= 1
        if flag == False:
            #if previous attempt failed
            na = d['43'] / 0.16
            if int(na) != na:
                na = int(na) + 1
            np = na-1
    for i in range(int(np)):
        posz = round((d["43"]/na-0.015*unit(d["43"])+i*d["43"]/na)-d["43"]/2, 4)
        posy = round(-d["42"]/np/2-i*d["42"]/np+d["42"]/2, 4)
        oput += f'<a-box id="stair-{d["num"]}-step-{i}" \n'
        oput += f'position="0 {posz} {posy}" \n'
        oput += f'rotation="0 90 0" \n'
        oput += f'scale="{round(d["42"]/np, 4)} 0.03 {round(d["41"]-0.1, 4)}" \n'
        oput += entity_material(d)
        oput += '"></a-box>\n'
    d['prefix'] = 'railings'
    d['rx'] = 1
    d['ry'] = 1
    xtup = (-d["41"]/2, d["41"]/2-0.05)
    a = round(d['43'] / na, 4)
    d['42'] = round(d['42'], 4)
    d['43'] = round(d['43'], 4)
    faces = [
        (3, 2, 1),
        (3, 1, 0),
        (2, 5, 1),
        (2, 6, 5),
        (7, 3, 0),
        (7, 0, 4),
        (7, 6, 2),
        (7, 2, 3),
        (0, 1, 5),
        (0, 5, 4),
        (6, 7, 4),
        (6, 4, 5),
    ]
    for xpos in xtup:
        x = round(xpos, 4)
        vertices = [
            (x, d['42']/2, a-d['43']/2),
            (x+0.05, d['42']/2, a-d['43']/2),
            (x+0.05, d['42']/2, -0.03-d['43']/2),
            (x, d['42']/2, -0.03-d['43']/2),
            (x, -d['42']/2, d['43']/2),
            (x+0.05, -d['42']/2, d['43']/2),
            (x+0.05, -d['42']/2, d['43']/2-a-0.03),
            (x, -d['42']/2, d['43']/2-a-0.03),
        ]
        for i in range(12):
            f = faces[i]
            va = vertices[f[0]]
            vb = vertices[f[1]]
            vc = vertices[f[2]]
            oput += '<a-triangle '
            oput += f'geometry="vertexA:{round(va[0], 4)} {round(va[2], 4)} {round(va[1], 4)}; \n'
            oput += f'vertexB:{round(vb[0], 4)} {round(vb[2], 4)} {round(vb[1], 4)}; \n'
            oput += f'vertexC:{round(vc[0], 4)} {round(vc[2], 4)} {round(vc[1], 4)}" \n'
            oput += entity_material(d)
            if page.double_face:
                oput += 'side: double; '
            oput += '"></a-triangle> \n'
    return oput

def make_openwall(d):
    oput = ''
    tot = d['41']

    d2 = d.copy()
    #make left wall
    d2['41'] = d2['door_off_1']
    d2['ide'] = 'openwall-left'
    oput += f'<a-entity id="{d2["ide"]}-{d2["num"]}-ent" \n'
    xpos = round((d2['door_off_1']-tot)/2, 4)
    oput += f'position="{xpos} 0 0"> \n'
    oput += make_wall(d2)
    oput += '</a-entity> \n'
    #make part above door
    d2['41'] = d2['door_off_2'] - d2['door_off_1']
    d2['ide'] = 'openwall-above'
    oput += f'<a-entity id="{d2["ide"]}-{d2["num"]}-ent" \n'
    xpos = round((d2['door_off_2']+d2['door_off_1']-tot)/2, 4)
    zpos = round(d2['door_height'], 4)
    oput += f'position="{xpos} {zpos} 0"> \n'
    oput += make_wall(d2)
    oput += '</a-entity> \n'
    #make right wall
    d2['41'] = tot - d2['door_off_2']
    d2['ide'] = 'openwall-right'
    oput += f'<a-entity id="{d2["ide"]}-{d2["num"]}-ent" \n'
    xpos = round((-d2['41']+tot)/2, 4)
    oput += f'position="{xpos} 0 0"> \n'
    oput += make_wall(d2)
    oput += '</a-entity> \n'

    return oput

def survey_openwall(d):
    oput = ''
    tot = d['41']

    d2 = d.copy()
    #survey left wall
    d2['41'] = d2['door_off_1']
    d2['ide'] = 'openwall-left'
    oput += survey_wall(d2)
    #survey part above door
    d2['41'] = d2['door_off_2'] - d2['door_off_1']
    d2['ide'] = 'openwall-above'
    oput += survey_wall(d2)
    #survey right wall
    d2['41'] = tot - d2['door_off_2']
    d2['ide'] = 'openwall-right'
    oput += survey_wall(d2)

    return oput

def make_window(d):
    if d['SILL'] == '':
        d['SILL'] = 0
    else:
        d['SILL'] = float(d['SILL'])
    oput = ''
    #make wall under sill
    d2 = d.copy()
    d2['43'] = d2['SILL']
    d2['ide'] = 'window-under'
    oput += f'<a-entity id="{d2["ide"]}-{d2["num"]}-ent" \n'
    zpos = round((d2['SILL']-d['43'])/2, 4)
    oput += f'position="0 {zpos} 0"> \n'
    oput += make_wall(d2)
    oput += '</a-entity> \n'
    #make sill
    oput += f'<a-box id="{d["ide"]}-{d["num"]}-sill" \n'
    zpos = round(d['SILL']-d['43']/2-0.014, 4)
    oput += f'position="0 {zpos} 0" \n'
    sillw = round(d['41']+0.04, 4)
    silld = round(d['42']+0.04, 4)
    oput += f'scale="{sillw} 0.03 {silld}"> \n'
    oput += '</a-box> \n'
    #make frame
    values = (
        ('pool', 2, 'frame', 'MATERIAL'),
    )
    d = prepare_material_values(values, d)
    values = (
        #(xpos, zpos, rot, prefix, rx, rz, piece, depth, ypos),
        (d['41']/2-0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL'], 'frame-right', 0.06, 0),
        (-d['41']/2+0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL'], 'frame-left', 0.06, 0),
        (0, -d['43']/2+d['SILL']+0.025, 90, '', 0.05, d['41']-0.1, 'frame-bottom', 0.06, 0),
        (0, d['43']/2-0.025, 90, '', 0.05, d['41']-0.1, 'frame-top', 0.06, 0),
    )
    d['prefix'] = 'frame'
    d['ide'] = 'window'
    for v in values:
        oput += make_window_frame(v, d)
    #animated hinge 1
    xpos = round(-d["41"]/2+0.05*unit(d["41"]), 4)
    oput += f'<a-entity id="{d["ide"]}-{d["num"]}-hinge-1" \n'
    oput += f'position="{xpos} 0 0.025" \n'
    oput += 'animation="property: rotation; easing: easeInOutQuad; '
    oput += f'from:0 0 0; to:0 {-90*unit(d["41"])*unit(d["42"])} 0; '
    oput += 'startEvents: click; loop: 1; dir: alternate;"> \n'
    if eval(d["DOUBLE"]):
        #moving part 1
        values = (
            #(xpos, zpos, rot, prefix, rx, rz, piece, depth, ypos),
            (d['41']/2-0.075, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-1-right', 0.07, -0.01),
            (0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-1-left', 0.07, -0.01),
            (d['41']/4-0.025, -d['43']/2+d['SILL']+0.075, 90, '', 0.05, d['41']/2-0.15, 'moving-1-bottom', 0.07, -0.01),
            (d['41']/4-0.025, d['43']/2-0.075, 90, '', 0.05, d['41']/2-0.15, 'moving-1-top', 0.07, -0.01),
        )
        for v in values:
            oput += make_window_frame(v, d)
        oput += '</a-entity> \n'
        #animated hinge 2
        xpos = round(d["41"]/2-0.05*unit(d["41"]), 4)
        oput += f'<a-entity id="{d["ide"]}-{d["num"]}-hinge-1" \n'
        oput += f'position="{xpos} 0 0.025" \n'
        oput += 'animation="property: rotation; easing: easeInOutQuad; '
        oput += f'from:0 0 0; to:0 {90*unit(d["41"])*unit(d["42"])} 0; '
        oput += 'startEvents: click; loop: 1; dir: alternate;"> \n'
        #moving part 2
        values = (
            #(xpos, zpos, rot, prefix, rx, rz, piece, depth, ypos),
            (-d['41']/2+0.075, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-2-left', 0.07, -0.01),
            (-0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-2-right', 0.07, -0.01),
            (-d['41']/4+0.025, -d['43']/2+d['SILL']+0.075, 90, '', 0.05, d['41']/2-0.15, 'moving-2-bottom', 0.07, -0.01),
            (-d['41']/4+0.025, d['43']/2-0.075, 90, '', 0.05, d['41']/2-0.15, 'moving-2-top', 0.07, -0.01),
        )
        for v in values:
            oput += make_window_frame(v, d)
        oput += '</a-entity> \n'
    else:
        #moving part 1
        values = (
            #(xpos, zpos, rot, prefix, rx, rz, piece, depth, ypos),
            (d['41']-0.125, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-1-right', 0.07, -0.01),
            (0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-1-left', 0.07, -0.01),
            (d['41']/2-0.05, -d['43']/2+d['SILL']+0.075, 90, '', 0.05, d['41']-0.2, 'moving-1-bottom', 0.07, -0.01),
            (d['41']/2-0.05, d['43']/2-0.075, 90, '', 0.05, d['41']-0.2, 'moving-1-top', 0.07, -0.01),
        )
        for v in values:
            oput += make_window_frame(v, d)
        oput += '</a-entity> \n'

    return oput

def make_window_frame(v, d):
    oput = ''
    d['rx'] = v[4]
    d['ry'] = v[5]
    oput += f'<a-box id="{d["ide"]}-{d["num"]}-{v[6]}" \n'
    oput += f'position="{round(v[0], 4)} {round(v[1], 4)} {v[8]}" \n'
    oput += f'rotation="0 0 {v[2]}" \n'
    oput += f'scale="{round(v[4], 4)} {round(v[5], 4)} {v[7]}" \n'
    oput += entity_material(d)
    oput += '"></a-box> \n'
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
    d['prefix'] = d['ide'] = 'light'

    d['dx'] = d['dy'] = d['dz'] = 0
    d['tag'] = 'a-entity'
    oput = ''
    oput += open_entity(page, d)

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

    oput += close_entity(page, d)
    return oput

def make_light_target(d):
    oput = f'target: #light-{d["num"]}-target;"> \n'
    oput += f'<a-entity id="light-{d["num"]}-target" position="0 -1 0"> </a-entity> \n'
    return oput

def make_text(page, d):
    d['prefix'] = d['ide'] = 'text'
    values = (
        ('pool', 0, d['prefix'], 'MATERIAL'),
    )
    d = prepare_material_values(values, d)

    d['dx'] = d['dy'] = d['dz'] = 0
    d['tag'] = 'a-entity'

    if d["WRAP-COUNT"]:
        wrapcount =  d["WRAP-COUNT"]
    else:
        length = len(d['TEXT'])
        if length <= 8:
            wrapcount = length+1
        elif length <= 30:
            wrapcount = 10
        else:
            wrapcount = length/3
    oput = ''
    oput += open_entity(page, d)
    oput += f'text="width: {d["41"]}; align: {d["ALIGN"]}; color: {d["text_color"]}; '
    oput += f'value: {d["TEXT"]}; wrap-count: {wrapcount}; '
    oput += '">\n'
    oput += close_entity(page, d)
    return oput

def make_link(page, d):
    d['prefix'] = d['ide'] = 'link'

    d['dx'] = d['dy'] = d['dz'] = 0
    d['tag'] = 'a-link'

    oput = ''
    oput += open_entity(page, d)
    oput += f'scale="{d["41"]} {d["43"]} {d["42"]}"\n'
    oput += add_link_part(page, d)
    oput += '>\n'
    oput += close_entity(page, d)
    return oput

def make_object(d):
    """Object block

    Block loads a Object Model (Wavefront) along with it's *.mtl file. PARAM1
    must be equal to *.obj and *.mtl filename (use lowercase extension). Files
    must share same filename and must be loaded in the media/document folder.
    If PARAM2 is set to 'scale', object will be scaled.
    """
    oput = ''

    oput += f'<a-entity id="model-{d["num"]}" \n'
    oput += f'position="0 {-d["43"]/2} 0" \n'
    if d['NAME'] == 'obj-mtl':
        oput += f'obj-model="obj: #{d["PARAM1"]}.obj; \n'
        oput += f' mtl: #{d["PARAM1"]}.mtl" \n'
    elif d['NAME'] == 'gltf':
        oput += f'gltf-model="#{d["PARAM1"]}.gltf" animation-mixer \n'
    if d['PARAM2'] == 'scale':
        oput += f'scale="{fabs(d["41"])} {fabs(d["43"])} {fabs(d["42"])}" \n'
    oput += '></a-entity><!--close object--> \n'

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

    d['prefix'] = 'trunk'
    d['rx'] = fabs(d["41"])
    d['ry'] = lt
    oput += f'<a-entity id="{d["NAME"]}-{d["num"]}-trunk-ent" \n'
    oput += f'position="0 {-d["43"]/2} 0" \n'
    oput += f'rotation="{ang} {rot} 0"> \n'
    oput += f'<a-cone id="{d["NAME"]}-{d["num"]}-trunk" \n'
    oput += f'position="0 {lt/2} 0" \n'
    oput += f'geometry="height: {lt}; radius-bottom: {lt/8}; radius-top: {lt/12};" \n'
    oput += entity_material(d)
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

    return oput

def make_branch(branch, lb, lp, angle, rotx, d):
    d['prefix'] = 'branch'
    d['rx'] = fabs(d["41"])
    d['ry'] = lb
    ang = gauss(angle, 10)
    rot = gauss(rotx, 20)
    oput = f'<a-entity id="{d["NAME"]}-{d["num"]}-branch-{branch}-ent" \n'
    oput += f'position="0 {lp*.95-lp*fabs(gauss(0, .2))} 0" \n'
    oput += f'rotation="{ang} {rot} 0"> \n'
    oput += f'<a-cone id="{d["NAME"]}-{d["num"]}-branch-{branch}" \n'
    oput += f'position="0 {lb/2} 0" \n'
    oput += f'geometry="height: {lb}; radius-bottom: {lb/12}; radius-top: {lb/14};" \n'
    oput += entity_material(d)
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
    oput += entity_material(d)
    oput += 'side: back;">\n'
    oput += '</a-sphere> \n'#close leaves
    return oput

def open_entity(page, d):
    oput = ''
    if d['animation']:
        if d['RIG']:
            identity = f'{page.id}-{d["ide"]}-{d["num"]}-rig'
            position = make_position(d)
            rotation = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
            page.ent_dict[identity]={'position': position, 'rotation': rotation,
                'closing': 0, 'layer': d['layer'], 'tag': 'a-entity'}
            if d['PROPERTY'] == 'orbit':
                identity = f'{page.id}-{d["ide"]}-{d["num"]}-leash'
                l = d['TO'].split()
                d['FROM'] = '0 0 0'
                d['TO'] = '0 360 0'
                d['START_EVENTS'] = d['DIRECTION'] = ''
                d['LOOP'] = 'true; autoplay: true; easing: linear'
                animation = add_animation(d)
                page.ent_dict[identity]={'animation': animation,
                    'closing': 0,  'layer': d['layer'], 'tag': 'a-entity'}

                identity = make_insertion(page, d)
                position = f'{l[0]} {l[1]} {l[2]}'
                page.ent_dict[identity].update(position=position)
            else:
                identity = make_insertion(page, d)
                animation = add_animation(d)
                page.ent_dict[identity].update(animation=animation)
        else:
            if d['PROPERTY'] == 'rotation':
                identity = f'{page.id}-{d["ide"]}-{d["num"]}-rig'
                position = make_position(d)
                animation = add_animation(d)
                page.ent_dict[identity]={'position': position,
                    'animation': animation, 'closing': 0, 'layer': d['layer'],
                     'tag': 'a-entity'}

                identity = make_insertion(page, d)
                rotation = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
                page.ent_dict[identity].update(rotation=rotation)
            elif d['PROPERTY'] == 'orbit':
                identity = f'{page.id}-{d["ide"]}-{d["num"]}-rig'
                position = make_position(d)
                rotation = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
                l = d['TO'].split()
                d['FROM'] = '0 0 0'
                d['TO'] = '0 360 0'
                d['START_EVENTS'] = d['DIRECTION'] = ''
                d['LOOP'] = 'true; autoplay: true; easing: linear'
                animation = add_animation(d)
                page.ent_dict[identity]={'position': position,
                    'rotation': rotation, 'animation': animation,
                    'closing': 0, 'layer': d['layer'], 'tag': 'a-entity'}

                identity = make_insertion(page, d)
                position = f'{l[0]} {l[1]} {l[2]}'
                page.ent_dict[identity].update(position=position)
            else:
                identity = make_insertion(page, d)
                position = make_position(d)
                rotation = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
                animation = add_animation(d)
                page.ent_dict[identity].update(position=position,
                    rotation=rotation, animation=animation)
    else:
        identity = make_insertion(page, d)
        position = make_position(d)
        rotation = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
        page.ent_dict[identity].update(position=position, rotation=rotation, )

    return identity

def make_insertion(page, d):

    if d['ID']:
        identity = f'{page.id}-{d["ID"]}'
    else:
        identity = f'{page.id}-{d["ide"]}-{d["num"]}'
    page.ent_dict[identity]={}
    if d['PROPERTY'] == 'checkpoint':
        page.ent_dict[identity]={'animator': 'checkpoint,checkpoint', }
    elif d['PROPERTY'] == 'look-at':
        if d['TARGET']:
            page.ent_dict[identity]={'animator': f'look-at,#{d["TARGET"]}', }
        else:
            page.ent_dict[identity]={'animator': 'look-at,#camera', }
    elif d['PROPERTY'] == 'stalker':
        page.ent_dict[identity]={'animator': 'look-at,#camera', }
    elif d['PROPERTY'] == 'event':
        page.ent_dict[identity]={'animator':
            f'event-proxy,listen: {d["START_EVENTS"]}; emit: {d["ID"]}; target: #{d["TARGET"]}', }

    return identity

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
    d['30'] = d['30'] +         (-cx*sy)*d['dx'] +     (sx)*d['dy'] +           (cx*cy)*d['dz']

    position = f'{round(d["10"], 4)} {round(d["30"], 4)} {round(d["20"], 4)}'

    return position

def close_entity(page, d):

    if d['PROPERTY'] == 'stalker':
        pass #oput += add_stalker(page, d)
    closing = 1
    if d['animation']:
        if d['RIG']:
            if d['PROPERTY'] == 'orbit':
                closing += 2
            else:
                closing += 1
        else:
            if d['PROPERTY'] == 'rotation' or d['PROPERTY'] == 'orbit':
                closing += 1
    return closing

def entity_geometry(d):
    attr_dict = {
        'a-cone': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-cylinder': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-circle': ('SEGMENTS', 'THETA-LENGTH', 'THETA-START', ),
        'a-curvedimage': ('THETA-LENGTH', 'THETA-START', ),
        'a-sphere': ('PHI-LENGTH', 'PHI-START', 'SEGMENTS-HEIGHT', 'SEGMENTS-WIDTH', 'THETA-LENGTH', 'THETA-START', ),
    }
    attributes = attr_dict[d['2']]
    oput = ''
    for attribute in attributes:
        try:
            if d[attribute]:
                oput += f'{attribute.lower()}: {d[attribute]};'
        except:
            pass

    return oput

def add_animation(d):
    oput = ''
    #oput += 'animation=" \n'
    oput += 'easing: easeInOutQuad; '
    if d['PROPERTY'] == 'orbit':
        oput += f'property: rotation; '
    else:
        oput += f'property: {d["PROPERTY"]}; '
    if d['RIG'] == False:
        if d['PROPERTY'] == 'rotation':
            oput += f'from: {d["FROM"]}; '
            oput += f'to: {d["TO"]}; '
        elif d['PROPERTY'] == 'orbit':
            l = d['FROM'].split()
            oput += f'from:{round(d["210"]+float(l[0]), 4)} '
            oput += f'{round(d["50"]+float(l[1]), 4)} '
            oput += f'{round(d["220"]+float(l[2]), 4)}; '
            l = d['TO'].split()
            oput += f'to:{round(d["210"]+float(l[0]), 4)} '
            oput += f'{round(d["50"]+float(l[1]), 4)} '
            oput += f'{round(d["220"]+float(l[2]), 4)}; '
        elif d['PROPERTY'] == 'position':
            l = d['FROM'].split()
            oput += f'from:{round(d["10"]+float(l[0]), 4)} '
            oput += f'{round(d["30"]+float(l[1]), 4)} '
            oput += f'{round(d["20"]+float(l[2]), 4)}; '
            l = d['TO'].split()
            oput += f'to:{round(d["10"]+float(l[0]), 4)} '
            oput += f'{round(d["30"]+float(l[1]), 4)} '
            oput += f'{round(d["20"]+float(l[2]), 4)}; '
    else:
        oput += f'from: {d["FROM"]}; '
        oput += f'to: {d["TO"]}; '
    oput += f'startEvents: {d["START_EVENTS"]}; '
    oput += f'dir: {d["DIRECTION"]}; '
    oput += f'loop: {d["LOOP"]}; '
    oput += f'dur: {d["DURATION"]}; '
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
        oput += f'<a-entity id="{d["ide"]}-{d["num"]}-balloon-ent" \n'
        oput += f'position="0 {d["43"]/2+d["41"]/4+.1} 0" \n'
        oput += f'text="width: {d["41"]*.9}; align: center; color: black; '
        oput += f'value: {d["TEXT"]}; wrap-count: {wrapcount};"> \n'
        oput += f'<a-cylinder id="{d["ide"]}-{d["num"]}-balloon" \n'
        oput += f'position="0 0 -0.01" \n'
        oput += f'rotation="90 0 0" \n'
        oput += f'scale="{fabs(d["41"])/1.5} 0 {fabs(d["41"])/3}"> \n'
        oput += '</a-cylinder></a-entity>\n'
        oput += f'<a-triangle id="{d["ide"]}-{d["num"]}-triangle" \n'
        oput += f'geometry="vertexA:0 {d["43"]/2+.1} 0.0005; \n'
        oput += f'vertexB:0 {d["43"]/2-.05} 0.0005; \n'
        oput += f'vertexC:{d["41"]/4} {d["43"]/2+.1} 0.0005"> \n'
        oput += '</a-triangle> \n'
    if d['LINK']:
        oput += f'<a-link id="{d["ide"]}-{d["num"]}-link" \n'
        oput += f'position="{d["41"]*.7} 0 0.02" \n'
        oput += f'scale="{d["41"]*.35} {d["41"]*.35}"\n'
        oput += add_link_part(page, d)
        oput += '>\n'
        oput += '</a-link>\n'
    return oput

def add_link_part(page, d):
    oput = ''
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
        oput += f'title="{target.title}" \n'
        try:
            eq_image = target.specific.equirectangular_image
            if eq_image:
                oput += f'image="{eq_image.file.url}"'
        except:
            oput += 'image="#default-sky"'
    else:
        oput += f'href="{d["LINK"]}" \n'
        if d['TITLE']:
            oput += f'title="{d["TITLE"]}" \n'
        else:
            oput += 'title="Sorry, no title" \n'
        oput += 'image="#default-sky"'
    return oput

def unit(nounit):
    #returns positive/negative scaling
    if nounit == 0:
        return 0
    unit = fabs(nounit)/nounit
    return unit

def rfloat(string):
    return round(float(string), 4)

def entity_material(d):
    #returns object material
    oput = ''
    if d['wireframe']:
        oput += f'material="wireframe: true; color: {d[d["prefix"]+"_color"]}; '
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
