"""Collection of functions for writing HTML of entities and blocks.

Functions are referenced from architettura.dxf.make_html, a-block CAD blocks
have NAME attribute that are essentially block names, while BIM blocks use PART
attribute for setting 'partition type'. Block appearance is determined by
MATERIAL attribute (multiple components may be used depending on NAME), other
features depend on PARAM attributes.
"""

from math import degrees, sqrt, pow, fabs, atan2, sin, cos, radians
from random import random, gauss
from architettura import blobs

def make_camera(page, d):
    #TODO different cameras to choose from
    pos = f'{round(d["10"], 4)} {round(d["30"], 4)} {round(d["20"], 4)}'
    rot = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
    blob = f'id=:camera-ent=;position=:{pos}=;rotation=:{rot}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
    page.ent_dict['camera-ent'] = blob

    pos = f'0 {round(d["43"]*1.6, 4)} 0'
    blob = f'id=:camera=;position=:{pos}=;look-controls=:pointerLockEnabled: true'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-camera=;closing=:0'
    page.ent_dict['camera'] = blob

    blob = f'id=:camera-light=;type=:point=;distance=:10=;intensity=:{d["LIGHT-INT"]}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-light=;closing=:1'
    page.ent_dict['camera-light'] = blob

    blob = f'id=:cursor=;layer=:{d["layer"]}=;tag=:a-cursor=;closing=:3'
    page.ent_dict['cursor'] = blob

    return

def make_box(page, d):

    d['rx'] = fabs(d["41"])
    d['ry'] = fabs(d["43"])
    d['dx'] = d['41']/2
    d['dy'] = -d['42']/2
    d['dz'] = d['43']/2
    d['ide'] = 'box'
    identity = open_entity(page, d)
    geometry = f'width: {round(d["41"], 4)}; height: {round(d["43"], 4)}; '
    geometry += f'depth: {round(d["42"], 4)}'
    blob = f'=;geometry=:{geometry}=;layer=:{d["layer"]}'
    blob += f'=;repeat=:{round(d["rx"], 4)} {round(d["ry"], 4)}'
    blob += f'=;material=:{d["MATERIAL"]}=;component=:0=;tag=:a-box'
    blob += f'=;closing=:{close_entity(page, d)}'
    page.ent_dict[identity] += blob

    return

def make_block(page, d):

    d['dx'] = d['dy'] = 0
    d['dz'] = d['43']/2
    d['tag'] = 'a-entity'
    d['ide'] = d['NAME']
    identity = open_entity(page, d)
    blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
    page.ent_dict[identity] += blob
    d['closing'] = close_entity(page, d)

    if d['NAME'] == 't01':
        make_table_01(page, d)
    elif d['NAME'] == 'obj-mtl' or d['NAME'] == 'gltf':
        make_object(page, d)
    elif d['NAME'] == 'grl':
        make_grl(page, d)
    #elif d['NAME'] == 'tree':
        #make_tree(page, d)

    return

def make_bim_block(page, d):

    d['dx'] = d['41']/2
    d['dy'] = -d['42']/2
    if d['2'] == 'a-slab':
        d['dz'] = -d['43']/2
    else:
        d['dz'] = d['43']/2
    d['tag'] = 'a-entity'
    #d['ide'] = 'BIM-block'

    if d['2'] == 'a-wall':
        d['ide'] = 'wall'
        identity = open_entity(page, d)
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        blob += f'=;survey=:{round(d["41"], 4)} {round(d["43"], 4)} '
        blob += f'{round(d["42"], 4)} Null Null=;partition=:{d["PART"]}'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_wall(page, d)
    elif d['2'] == 'a-slab':
        d['ide'] = 'slab'
        identity = open_entity(page, d)
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        blob += f'=;survey=:{round(d["41"], 4)} {round(d["42"], 4)} '
        blob += f'{round(d["43"], 4)} Null Null=;partition=:{d["PART"]}'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_slab(page, d)
    elif d['2'] == 'a-door':
        d['ide'] = 'door'
        identity = open_entity(page, d)
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        blob += f'=;survey=:{round(d["41"], 4)} {round(d["43"], 4)} 0 '
        blob += f'{d["DOUBLE"]} {d["SLIDING"]}'
        blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_door(page, d)
    elif d['2'] == 'a-window':
        d['ide'] = 'window'
        identity = open_entity(page, d)
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        blob += f'=;survey=:{round(d["41"], 4)} {round(d["43"] - float(d["SILL"]), 4)} 0 '
        blob += f'{d["DOUBLE"]} False'
        blob += f'=;material=:{d["WMATERIAL"]}=;component=:2'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_window(page, d)
    elif d['2'] == 'a-stair':
        d['ide'] = 'stair'
        identity = open_entity(page, d)
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_stair(page, d)
    elif d['2'] == 'a-openwall':
        d['ide'] = 'openwall'
        identity = open_entity(page, d)
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_openwall(page, d)

    return

def make_circular(page, d):

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

    d['ide'] = d['2'].replace('a-', '')
    d['tag'] = d['2']
    identity = open_entity(page, d)
    #geometry = f'primitive: {d["ide"]}; '
    if d['2'] == 'a-circle':
        blob = f'=;radius=:{round(fabs(d["41"]), 4)};'
    else:
        blob = f'=;scale=:{round(d["41"], 4)} {round(d["43"], 4)} '
        blob += f'{round(d["42"], 4)}'
    blob += entity_geometry(d)
    blob += f'=;repeat=:{round(d["rx"], 4)} {round(d["ry"], 4)}'
    blob += f'=;layer=:{d["layer"]}'
    blob += f'=;material=:{d["MATERIAL"]}=;component=:0=;tag=:{d["tag"]}'
    blob += f'=;closing=:{close_entity(page, d)}'
    page.ent_dict[identity] += blob

    return

def make_curvedimage(page, d):
    d['ide'] = 'curvedimage'
    d['rx'] = 1
    d['ry'] = 1
    d['dx'] = 0
    d['dy'] = 0
    d['dz'] = d['43']/2
    identity = open_entity(page, d)
    blob = f'=;radius=:{round(fabs(d["41"])*2, 4)}'
    blob += f'=;height=:{round(d["43"], 4)}'
    blob += entity_geometry(d)
    blob += f'=;repeat=:{round(d["rx"], 4)} {round(d["ry"], 4)}'
    blob += f'=;layer=:{d["layer"]}'
    blob += f'=;material=:{d["MATERIAL"]}=;component=:0=;tag=:{d["2"]}'
    blob += f'=;closing=:{close_entity(page, d)}'
    page.ent_dict[identity] += blob

    return

def make_plane(page, d):
    d['ide'] = 'plane'
    d['dx'] = d['41']/2
    d['dy'] = 0
    d['dz'] = d['43']/2
    d['tag'] = 'a-entity'
    identity = open_entity(page, d)
    blob = f'=;layer=:{d["layer"]}=;closing=:0=;tag=:{d["tag"]}'
    page.ent_dict[identity] += blob
    d['closing'] = close_entity(page, d)
    make_w_plane(page, d)

    return

def make_w_plane(page, d):
    """Wall plane default BIM block.

    A vertical surface. Gets dimensions from plane scaling, TILING and
    SKIRTING height from respective attributes. Gets MATERIAL with 3 components,
    first for wall, second for tiling and third for skirting.
    """
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
            blob = f'id=:{identity}'
            blob += f'=;width=:{round(d["rx"], 4)}=;height=:{round(v[0], 4)}'
            blob += f'=;repeat=:{round(d["rx"], 4)} {v[0]}'
            blob += f'=;position=:0 {round(v[2]*unit(d["43"])-d["43"]/2, 4)} 0'
            material = d.get('MATERIAL', '')
            blob += f'=;material=:{material}=;component=:{v[3]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-plane=;closing=:1'
            blob += f'=;survey=:{round(d["rx"], 4)} {v[0]} 0 Null Null'
            page.ent_dict[identity] = blob
    #last one closes all
    closing = d['closing']+1
    page.ent_dict[identity] = blob.replace('closing=:1', f'closing=:{closing}')

    return

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
    blob = f'=;vertex-a=:{round(d["10b"], 4)} {round(d["30b"], 4)} {round(d["20b"], 4)}'
    blob += f'=;vertex-b=:{round(d["11"], 4)} {round(d["31"], 4)} {round(d["21"], 4)}'
    blob += f'=;vertex-c=:{round(d["12"], 4)} {round(d["32"], 4)} {round(d["22"], 4)}'
    material = d.get('MATERIAL', '')
    blob += f'=;material=:{material}=;component=:0'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-triangle=;closing=:{close_entity(page, d)}'
    page.ent_dict[identity] += blob

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
    d['ide'] = 'line'
    d['tag'] = 'a-entity'
    identity = open_entity(page, d)
    if d['39']:
        d['42'] = 0
        d['43'] = d['39']
        d['41'] = sqrt(pow(d['11'], 2) + pow(d['21'], 2))*2
        d['50'] = -degrees(atan2(d['21'], d['11']))
        blob = f'=;rotation=:0 {round(d["50"], 4)} 0'
        blob += f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        page.ent_dict[identity] += blob
        d['closing'] = close_entity(page, d)
        make_w_plane(page, d)
    else:
        blob = f'=;line=:start:{round(d["10b"], 4)} '
        blob += f'{round(d["30b"], 4)} {round(d["20b"], 4)}; '
        blob += f'end:{round(d["11"], 4)} '
        blob += f'{round(d["31"], 4)} {round(d["21"], 4)}; '
        color = d.get('COLOR', '')
        blob += f'=;layer=:{d["layer"]}'
        blob += f'=;color=:{color}=;tag=:{d["tag"]}'
        blob += f'=;closing=:{close_entity(page, d)}'
        page.ent_dict[identity] += blob

    return

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
    d['ide'] = 'poly'
    d['tag'] = 'a-entity'
    d['num1'] = d['num']
    identity = open_entity(page, d)
    if d['39']:
        blob = f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
        page.ent_dict[identity] += blob
        d['42'] = 0
        d['43'] = d['39']
        stop = d['90']-2
        for i in range(d['90']-1):
            d['num'] = str(d['num1']) + '-' + str(i)
            dx = d['vx'][i]-d['vx'][i+1]
            dy = d['vy'][i]-d['vy'][i+1]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            identity = f'{page.id}-{d["ide"]}-{d["num"]}'
            position = f'{round(d["vx"][i]-dx/2, 4)} 0 {round(d["vy"][i]-dy/2, 4)}'
            rotation = f'0 {round(d["50"], 4)} 0'
            blob = f'id=:{identity}=;position=:{position}=;rotation=:{rotation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
            page.ent_dict[identity] = blob
            if d['70']:
                d['closing'] = 1
            else:
                if i == stop:
                    d['closing'] = close_entity(page, d) + 1
                else:
                    d['closing'] = 1
            make_w_plane(page, d)
        if d['70']:
            d['num'] = str(d['num1']) + '-' + str(i+1)
            dx = d['vx'][i+1]-d['vx'][0]
            dy = d['vy'][i+1]-d['vy'][0]
            d['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
            d['50'] = 180-degrees(atan2(dy, dx))
            identity = f'{page.id}-{d["ide"]}-{d["num"]}'
            position = f'{round(d["vx"][i+1]-dx/2, 4)} 0 {round(d["vy"][i+1]-dy/2, 4)}'
            rotation = f'0 {round(d["50"], 4)} 0'
            blob = f'id=:{identity}=;position=:{position}=;rotation=:{rotation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:0'
            page.ent_dict[identity] = blob
            d['closing'] = close_entity(page, d) + 1
            make_w_plane(page, d)
        d['num'] = d['num1']
    else:
        blob = ''
        for i in range(d['90']-1):
            if i==0:
                blob += '=;line'
            else:
                blob += f'=;line__{i+1}'
            blob += f'=:start:{round(d["vx"][i], 4)} 0 {round(d["vy"][i], 4)}; '
            blob += f'end:{round(d["vx"][i+1], 4)} 0 {round(d["vy"][i+1], 4)}; '
        if d['70']:
            blob += f'=;line__{i+2}=:start:{round(d["vx"][i+1], 4)} 0 '
            blob += f'{round(d["vy"][i+1], 4)}; '
            blob += f'end:{round(d["vx"][0], 4)} 0 {round(d["vy"][0], 4)}; '
        color = d.get('COLOR', '')
        blob += f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;color=:{color}'
        blob += f'=;closing=:{close_entity(page, d)}'
        page.ent_dict[identity] += blob
    return

def make_table_01(page, d):
    """Table 01, default block (t01)

    A simple table with four legs. Gets dimensions from block scaling, except for
    leg diameter (5cm). Gets top material from first component and leg material
    from third component.
    """

    #table top
    d['rx'] = round(fabs(d["41"]), 4)
    d['ry'] = round(fabs(d["42"]), 4)
    identity = f'{page.id}-table01-{d["num"]}-top'
    position = f'0 {round(d["43"]/2-0.025*unit(d["43"]), 4)} 0'
    geometry = f'width: {d["rx"]}; height: 0.05; depth: {d["ry"]};'
    material = d.get('MATERIAL', '')
    blob = f'id=:{identity}=;position=:{position}=;geometry=:{geometry}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
    blob += f'=;material=:{material}=;component=:2'
    page.ent_dict[identity] = blob
    #prepare legs
    d['prefix'] = 'leg'
    scale_x = round(d["41"]/2-0.05*unit(d["41"]), 4)
    scale_y = round(d["42"]/2-0.05*unit(d["42"]), 4)
    height = round(d["43"]-0.025*unit(d["43"]), 4)
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
        identity = f'{page.id}-table01-{d["num"]}-leg-{v[0]}'
        position = f'{v[1]} {(height-round(d["43"], 4))/2} {v[2]}'
        geometry = f'radius: 0.025; height: {height}; '
        blob = f'id=:{identity}=;position=:{position}=;geometry=:{geometry}'
        blob += f'=;layer=:{d["layer"]}=;tag=:a-cylinder=;closing=:1'
        blob += f'=;material=:{material}=;component=:1'
        page.ent_dict[identity] = blob
    #last one closes all
    closing = d['closing']+1
    page.ent_dict[identity] = blob.replace('closing=:1', f'closing=:{closing}')

    return

def make_door(page, d):
    """Door default BIM block.

    A simple framed door. Gets dimensions from block scaling, except for frame
    dimension. PART sets door features. If set to 'ghost' door will not be
    rendered. SLIDING and DOUBLE are boolean. Gets panel material from first
    component and frame material from third component.
    """

    if d["PART"] == 'ghost':
        return

    d['rx'] = 1
    d['ry'] = 1
    #door frame
    values = (('left', round(-0.049*unit(d["41"])-d["41"]/2, 4),
        round(0.099*unit(d["43"])/2, 4), '0 0 90', round(fabs(d["43"])+0.099, 4),
        round(fabs(d["42"])+0.02, 4)),
        ('right', round(d["41"]/2+0.049*unit(d["41"]), 4),
        round(0.099*unit(d["43"])/2, 4), '0 0 90', round(fabs(d["43"])+0.099, 4),
        round(fabs(d["42"])+0.02, 4)),
        ('top', 0, round(d["43"]/2+0.049*unit(d["43"]), 4), '0 0 0',
        round(fabs(d["41"])-0.002, 4), round(fabs(d["42"])+0.02, 4))
        )
    for v in values:
        identity = f'{page.id}-door-{d["num"]}-{v[0]}-frame'
        position = f'{v[1]} {v[2]} 0'
        rotation = v[3]
        geometry = f'width: {v[4]}; height: 0.1; depth: {v[5]};'
        blob = f'id=:{identity}=;position=:{position}=;rotation=:{rotation}'
        blob += f'=;geometry=:{geometry}=;material=:{d["MATERIAL"]}=;component=:2'
        blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
        blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
        page.ent_dict[identity] = blob

    if eval(d["DOUBLE"]):
        d['rx'] = round(fabs(d["41"])/2-0.002, 4)
    else:
        d['rx'] = round(fabs(d["41"])-0.002, 4)
    d['ry'] = round(d["43"]-0.001*unit(d["43"]), 4)
    if eval(d["SLIDING"]):
        if eval(d["DOUBLE"]):
            #animated slide 1
            identity = f'{page.id}-door-{d["num"]}-slide-1'
            pos = f'{-d["41"]/2} {-d["43"]/2} 0'
            animation = 'property: position; easing: easeInOutQuad; '
            animation += f'from:{-d["41"]/2} {-d["43"]/2} 0; '
            animation += f'to:{-d["41"]+0.01} {-d["43"]/2} 0; startEvents: click; '
            animation += 'loop: 1; dir: alternate;'
            blob = f'id=:{identity}=;position=:{pos}=;animation=:{animation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
            page.ent_dict[identity] = blob
            #moving part 1
            identity = f'{page.id}-door-{d["num"]}-moving-part-1'
            pos = f'{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} 0'
            geometry = f'width: {(fabs(d["41"]))/2-0.002}; height: {d["43"]-0.001*unit(d["43"])}; depth: 0.05;'
            blob = f'id=:{identity}=;position=:{pos}=;geometry=:{geometry}'
            blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
            blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:2'
            page.ent_dict[identity] = blob
            #animated slide 2
            identity = f'{page.id}-door-{d["num"]}-slide-2'
            pos = f'{d["41"]/2} {-d["43"]/2} 0'
            animation = 'property: position; easing: easeInOutQuad; '
            animation += f'from:{d["41"]/2} {-d["43"]/2} 0; '
            animation += f'to:{d["41"]-0.01} {-d["43"]/2} 0; startEvents: click; '
            animation += 'loop: 1; dir: alternate;'
            blob = f'id=:{identity}=;position=:{pos}=;animation=:{animation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
            page.ent_dict[identity] = blob
            #moving part 2
            identity = f'{page.id}-door-{d["num"]}-moving-part-2'
            pos = f'{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} 0'
            geometry = f'width: {(fabs(d["41"]))/2-0.002}; height: {d["43"]-0.001*unit(d["43"])}; depth: 0.05;'
            blob = f'id=:{identity}=;position=:{pos}=;geometry=:{geometry}'
            blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
            blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:{d["closing"]+2}'
            page.ent_dict[identity] = blob
            return
        else:#single
            #animated slide
            identity = f'{page.id}-door-{d["num"]}-slide'
            pos = f'{-d["41"]/2} {-d["43"]/2} 0'
            animation = 'property: position; easing: easeInOutQuad; '
            animation += f'from:{-d["41"]/2} {-d["43"]/2} 0; '
            animation += f'to:{-d["41"]*3/2+0.01} {-d["43"]/2} 0; startEvents: click; '
            animation += 'loop: 1; dir: alternate;'
            blob = f'id=:{identity}=;position=:{pos}=;animation=:{animation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
            page.ent_dict[identity] = blob
            #moving part
            identity = f'{page.id}-door-{d["num"]}-moving-part'
            pos = f'{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} 0'
            geometry = f'width: {fabs(d["41"])-0.002}; height: {d["43"]-0.001*unit(d["43"])}; depth: 0.05;'
            blob = f'id=:{identity}=;position=:{pos}=;geometry=:{geometry}'
            blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
            blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:{d["closing"]+2}'
            page.ent_dict[identity] = blob
            return
    else:#hinged
        if eval(d["DOUBLE"]):
            #animated hinge 1
            identity = f'{page.id}-door-{d["num"]}-hinge-1'
            pos = f'{-d["41"]/2} {-d["43"]/2} {d["42"]/2}'
            animation = 'property: rotation; easing: easeInOutQuad; '
            animation += f'from:0 0 0; '
            animation += f'to:0 {-90*unit(d["41"])*unit(d["42"])} 0; startEvents: click; '
            animation += 'loop: 1; dir: alternate;'
            blob = f'id=:{identity}=;position=:{pos}=;animation=:{animation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
            page.ent_dict[identity] = blob
            #moving part 1
            identity = f'{page.id}-door-{d["num"]}-moving-part-1'
            pos = f'{d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}'
            geometry = f'width: {(fabs(d["41"]))/2-0.002}; height: {d["43"]-0.001*unit(d["43"])}; depth: 0.05;'
            blob = f'id=:{identity}=;position=:{pos}=;geometry=:{geometry}'
            blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
            blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:2'
            page.ent_dict[identity] = blob
            #animated hinge 2
            identity = f'{page.id}-door-{d["num"]}-hinge-2'
            pos = f'{d["41"]/2} {-d["43"]/2} {d["42"]/2}'
            animation = 'property: rotation; easing: easeInOutQuad; '
            animation += f'from:0 0 0; '
            animation += f'to:0 {90*unit(d["41"])*unit(d["42"])} 0; startEvents: click; '
            animation += 'loop: 1; dir: alternate;'
            blob = f'id=:{identity}=;position=:{pos}=;animation=:{animation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
            page.ent_dict[identity] = blob
            #moving part 2
            identity = f'{page.id}-door-{d["num"]}-moving-part-2'
            pos = f'{-d["41"]/4} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}'
            geometry = f'width: {(fabs(d["41"]))/2-0.002}; height: {d["43"]-0.001*unit(d["43"])}; depth: 0.05;'
            blob = f'id=:{identity}=;position=:{pos}=;geometry=:{geometry}'
            blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
            blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:{d["closing"]+2}'
            page.ent_dict[identity] = blob
            return
        else:#single
            #animated hinge
            identity = f'{page.id}-door-{d["num"]}-hinge'
            pos = f'{-d["41"]/2} {-d["43"]/2} {d["42"]/2}'
            animation = 'property: rotation; easing: easeInOutQuad; '
            animation += f'from:0 0 0; '
            animation += f'to:0 {-90*unit(d["41"])*unit(d["42"])} 0; startEvents: click; '
            animation += 'loop: 1; dir: alternate;'
            blob = f'id=:{identity}=;position=:{pos}=;animation=:{animation}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
            page.ent_dict[identity] = blob
            #moving part
            identity = f'{page.id}-door-{d["num"]}-moving-part'
            pos = f'{d["41"]/2} {(d["43"]-0.001*unit(d["43"]))/2} {-0.025*unit(d["42"])}'
            geometry = f'width: {fabs(d["41"])-0.002}; height: {d["43"]-0.001*unit(d["43"])}; depth: 0.05;'
            blob = f'id=:{identity}=;position=:{pos}=;geometry=:{geometry}'
            blob += f'=;material=:{d["MATERIAL"]}=;component=:0'
            blob += f'=;partition=:{d["PART"]}=;repeat=:{d["rx"]} {d["ry"]}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:{d["closing"]+2}'
            page.ent_dict[identity] = blob
            return

def make_slab(page, d):
    """Slab default BIM block.

    An horizontal partition. Gets dimensions from block scaling. PART sets
    partition type (TODO). Gets ceiling material from first component and
    floor material from third component.
    """
    d['rx'] = round(fabs(d["41"]), 4)
    d['ry'] = round(fabs(d["42"]), 4)
    #floor
    identity = f'{page.id}-slab-{d["num"]}-floor'
    position = f'0 {round(-0.005*unit(d["43"])+d["43"]/2, 4)} 0'
    geometry = f'width: {d["rx"]}; height: 0.01; depth: {d["ry"]};'
    blob = f'id=:{identity}=;position=:{position}'
    blob += f'=;geometry=:{geometry}=;material=:{d["MATERIAL"]}=;component=:2'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
    blob += f'=;repeat=:{d["rx"]} {d["ry"]}'
    blob += f'=;survey=:{d["rx"]} {d["ry"]} 0 Null Null'
    page.ent_dict[identity] = blob

    #ceiling
    identity = f'{page.id}-slab-{d["num"]}-ceiling'
    position = f'0 {round(-0.005*unit(d["43"]), 4)} 0'
    geometry = f'width: {d["rx"]}; height: {round(fabs(d["43"])-0.01, 4)}; '
    geometry += f'depth: {d["ry"]};'
    blob = f'id=:{identity}=;position=:{position}'
    blob += f'=;geometry=:{geometry}=;material=:{d["MATERIAL"]}=;component=:0'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:{d["closing"]+1}'
    blob += f'=;repeat=:{d["rx"]} {d["ry"]}'
    blob += f'=;survey=:{d["rx"]} {d["ry"]} 0 Null Null'
    page.ent_dict[identity] = blob

    return

def make_wall(page, d):
    """Wall default BIM block.

    A vertical partition. Gets dimensions from block scaling, TILING and
    SKIRTING height from respective attributes. PART sets partition type
    (TODO). Gets two different MATERIALs for internal and external surface, and
    respectively first component for wall, second for tiling and third for
    skirting.
    """
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
        (skirt_h, 'int-skirt', skirt_h/2, d["42"]/2, fabs(d["42"]), 'MATERIAL',
            2),
        (tile_h, 'int-tile', tile_h/2+skirt_h, d["42"]/2, fabs(d["42"]),
            'MATERIAL', 1),
        (wall_h, 'int-plaster', wall_h/2+tile_h+skirt_h, d["42"]/2,
            fabs(d["42"]), 'MATERIAL', 0),
        (skirt2_h, 'ext-skirt', skirt2_h/2, d["42"], 0.02, 'MATERIAL2', 2),
        (tile2_h, 'ext-tile', tile2_h/2+skirt2_h, d["42"], 0.02, 'MATERIAL2', 1),
        (wall2_h, 'ext-plaster', wall2_h/2+tile2_h+skirt2_h, d["42"], 0.02,
            'MATERIAL2', 0),
    )
    for v in values:
        if v[0]:
            #d['prefix'] = v[5]
            d['rx'] = fabs(d["41"])
            d['ry'] = v[0]
            identity = f'{page.id}-{d["ide"]}-{d["num"]}-{v[1]}'
            position = f'0 {round(v[2]*unit(d["43"])-d["43"]/2, 4)} '
            position += f'{round(-v[3]+0.005*unit(d["42"])+d["42"]/2, 4)}'
            geometry = f'width: {d["rx"]}; height: {v[0]}; depth: {v[4]-0.01}; '
            blob = f'id=:{identity}=;position=:{position}=;geometry=:{geometry}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
            blob += f'=;material=:{d[v[5]]}=;component=:{v[6]}'
            blob += f'=;survey=:{d["rx"]} {v[0]} 0 Null Null'
            blob += f'=;repeat=:{d["rx"]} {v[0]}'
            page.ent_dict[identity] = blob
    #last one closes all (we control if entity exists)
    if identity:
        closing = d['closing']+1
        page.ent_dict[identity] = blob.replace('closing=:1',
            f'closing=:{closing}')
    return

def make_stair(page, d):

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
                break
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
        identity = f'{page.id}-stair-{d["num"]}-step-{i}'
        position = f'0 {posz} {posy}'
        rotation = f'0 90 0'
        scale = f'{round(d["42"]/np, 4)} 0.03 {round(d["41"]-0.1, 4)}'
        material = d.get('MATERIAL', '')
        blob = f'id=:{identity}=;position=:{position}=;rotation=:{rotation}'
        blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
        blob += f'=;material=:{material}=;component=:0=;scale=:{scale}'
        page.ent_dict[identity] = blob

    #d['prefix'] = 'railings'
    d['rx'] = 1
    d['ry'] = 1
    xdict = {'left': -d["41"]/2, 'right': d["41"]/2-0.05}
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
    for side, xpos in xdict.items():
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
            identity = f'{page.id}-stair-{d["num"]}-{side}-beam-{i}'
            geometry = f'vertexA:{round(va[0], 4)} {round(va[2], 4)} {round(va[1], 4)}; '
            geometry += f'vertexB:{round(vb[0], 4)} {round(vb[2], 4)} {round(vb[1], 4)}; '
            geometry += f'vertexC:{round(vc[0], 4)} {round(vc[2], 4)} {round(vc[1], 4)}'
            material = d.get('MATERIAL', '')
            blob = f'id=:{identity}=;geometry=:{geometry}'
            blob += f'=;layer=:{d["layer"]}=;tag=:a-triangle=;closing=:1'
            blob += f'=;material=:{material}=;component=:2'
            page.ent_dict[identity] = blob
    closing = d['closing']+1
    page.ent_dict[identity] = blob.replace('closing=:1',
        f'closing=:{closing}')
    return

def make_openwall(page, d):

    tot = d['41']
    d2 = d.copy()
    #make left wall
    d2['41'] = d2['door_off_1']
    d2['ide'] = 'openwall-left'
    identity = f'{page.id}-{d2["ide"]}-{d2["num"]}-ent'
    xpos = round((d2['door_off_1']-tot)/2, 4)
    position =f'{xpos} 0 0'
    blob = f'id=:{identity}=;position=:{position}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
    blob += f'=;survey=:{round(d2["41"], 4)} {round(d2["42"], 4)} '
    blob += f'{round(d2["43"], 4)} Null Null=;partition=:{d2["PART"]}'
    page.ent_dict[identity] = blob
    d2['closing'] = 1
    make_wall(page, d2)

    #make part above door
    d2['41'] = d2['door_off_2'] - d2['door_off_1']
    d2['ide'] = 'openwall-above'
    identity = f'{page.id}-{d2["ide"]}-{d2["num"]}-ent'
    xpos = round((d2['door_off_2']+d2['door_off_1']-tot)/2, 4)
    zpos = round(d2['door_height'], 4)
    position= f'{xpos} {zpos} 0'
    blob = f'id=:{identity}=;position=:{position}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
    blob += f'=;survey=:{round(d2["41"], 4)} {round(d2["42"], 4)} '
    blob += f'{round(d2["43"], 4)} Null Null=;partition=:{d2["PART"]}'
    page.ent_dict[identity] = blob
    d2['closing'] = 1
    make_wall(page, d2)

    #make right wall
    d2['41'] = tot - d2['door_off_2']
    d2['ide'] = 'openwall-right'
    identity = f'{page.id}-{d2["ide"]}-{d2["num"]}-ent'
    xpos = round((-d2['41']+tot)/2, 4)
    position=f'{xpos} 0 0'
    blob = f'id=:{identity}=;position=:{position}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
    blob += f'=;survey=:{round(d2["41"], 4)} {round(d2["42"], 4)} '
    blob += f'{round(d2["43"], 4)} Null Null=;partition=:{d2["PART"]}'
    page.ent_dict[identity] = blob
    d2['closing'] = d['closing']+1
    make_wall(page, d2)

    return

def make_window(page, d):
    if d['SILL'] == '':
        d['SILL'] = 0
    else:
        d['SILL'] = float(d['SILL'])
    oput = ''
    #make wall under sill
    d2 = d.copy()
    d2['43'] = d2['SILL']
    d2['ide'] = 'window-under'
    identity = f'{page.id}-{d2["ide"]}-{d2["num"]}-ent'
    zpos = round((d2['SILL']-d['43'])/2, 4)
    position = f'0 {zpos} 0'
    blob = f'id=:{identity}=;position=:{position}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
    blob += f'=;survey=:{round(d["41"], 4)} {round(d2["43"], 4)} '
    blob += f'{round(d["42"], 4)} Null Null=;partition=:{d["PART"]}'
    page.ent_dict[identity] = blob
    d2['closing'] = 1
    make_wall(page, d2)

    #make sill TODO assign material
    identity = f'{page.id}-window-{d["num"]}-sill'
    zpos = round(d['SILL']-d['43']/2-0.014, 4)
    position = f'0 {zpos} 0'
    sillw = round(d['41']+0.04, 4)
    silld = round(d['42']+0.04, 4)
    scale = f'{sillw} 0.03 {silld}'
    blob = f'id=:{identity}=;position=:{position}=;scale=:{scale}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
    page.ent_dict[identity] = blob

    if d["PART"] == 'ghost':
        closing = d['closing']+1
        page.ent_dict[identity] = blob.replace('closing=:1',
            f'closing=:{closing}')
        return

    #make frame
    values = (
        #(xpos, zpos, rot, prefix, rx, rz, piece, depth, ypos),
        (d['41']/2-0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL'], 'frame-right', 0.06, 0),
        (-d['41']/2+0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL'], 'frame-left', 0.06, 0),
        (0, -d['43']/2+d['SILL']+0.025, 90, '', 0.05, d['41']-0.1, 'frame-bottom', 0.06, 0),
        (0, d['43']/2-0.025, 90, '', 0.05, d['41']-0.1, 'frame-top', 0.06, 0),
    )
    d['ide'] = 'window'
    for v in values:
        identity = make_window_frame(page, v, d)

    #animated hinge 1
    xpos = round(-d["41"]/2+0.05*unit(d["41"]), 4)
    identity = f'{page.id}-{d["ide"]}-{d["num"]}-hinge-1'
    position = f'{xpos} 0 0.025'
    anime = 'property: rotation; easing: easeInOutQuad; '
    anime += f'from:0 0 0; to:0 {-90*unit(d["41"])*unit(d["42"])} 0; '
    anime += 'startEvents: click; loop: 1; dir: alternate; '
    blob = f'id=:{identity}=;position=:{position}=;animation=:{anime}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
    page.ent_dict[identity] = blob
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
            identity = make_window_frame(page, v, d)

        #animated hinge 2
        xpos = round(d["41"]/2-0.05*unit(d["41"]), 4)
        identity = f'{page.id}-{d["ide"]}-{d["num"]}-hinge-2'
        position = f'{xpos} 0 0.025'
        anime = 'property: rotation; easing: easeInOutQuad; '
        anime += f'from:0 0 0; to:0 {90*unit(d["41"])*unit(d["42"])} 0; '
        anime += 'startEvents: click; loop: 1; dir: alternate; '
        blob = f'id=:{identity}=;position=:{position}=;animation=:{anime}'
        blob += f'=;layer=:{d["layer"]}=;tag=:a-entity=;closing=:0'
        page.ent_dict[identity] = blob
        #moving part 2
        values = (
            #(xpos, zpos, rot, prefix, rx, rz, piece, depth, ypos),
            (-d['41']/2+0.075, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-2-left', 0.07, -0.01),
            (-0.025, d['SILL']/2, 0, '', 0.05, d['43']-d['SILL']-0.1, 'moving-2-right', 0.07, -0.01),
            (-d['41']/4+0.025, -d['43']/2+d['SILL']+0.075, 90, '', 0.05, d['41']/2-0.15, 'moving-2-bottom', 0.07, -0.01),
            (-d['41']/4+0.025, d['43']/2-0.075, 90, '', 0.05, d['41']/2-0.15, 'moving-2-top', 0.07, -0.01),
        )
        for v in values:
            id_blob = make_window_frame(page, v, d)
        closing = d['closing']+2
        page.ent_dict[id_blob[0]] = id_blob[1].replace('closing=:1',
            f'closing=:{closing}')

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
            id_blob = make_window_frame(page, v, d)
        closing = d['closing']+2
        page.ent_dict[id_blob[0]] = id_blob[1].replace('closing=:1',
            f'closing=:{closing}')

    return

def make_window_frame(page, v, d):
    d['rx'] = v[4]
    d['ry'] = v[5]
    identity = f'{page.id}-{d["ide"]}-{d["num"]}-{v[6]}'
    position = f'{round(v[0], 4)} {round(v[1], 4)} {v[8]}'
    rotation = f'0 0 {v[2]}'
    scale = f'{round(v[4], 4)} {round(v[5], 4)} {v[7]}'
    blob = f'id=:{identity}=;position=:{position}=;rotation=:{rotation}'
    blob += f'=;layer=:{d["layer"]}=;tag=:a-box=;closing=:1'
    blob += f'=;material=:{d["WMATERIAL"]}=;component=:2'
    blob += f'=;partition=:{d["PART"]}=;scale=:{scale}'
    page.ent_dict[identity] = blob

    return identity, blob

def make_light(page, d):
    #set defaults
    if d['TYPE'] == '':
        d['TYPE'] = 'point'
        d['INTENSITY'] = 0.75
        d['DISTANCE'] = 50
        d['DECAY'] = 2
    d['ide'] = 'light'

    d['dx'] = d['dy'] = d['dz'] = 0
    d['tag'] = 'a-entity'

    identity = open_entity(page, d)

    light = f'type: {d["TYPE"]}; intensity: {d["INTENSITY"]}; '
    if d['TYPE'] == 'point':
        light += f'decay: {d["DECAY"]}; distance: {d["DISTANCE"]}; '
    elif d['TYPE'] == 'spot':
        light += f'decay: {d["DECAY"]}; distance: {d["DISTANCE"]}; '
        light += f'angle: {d["ANGLE"]}; penumbra: {d["PENUMBRA"]}; '
    elif d['TYPE'] == 'directional':
        light += f'shadowCameraBottom: {-5*fabs(d["42"])}; '
        light += f'shadowCameraLeft: {-5*fabs(d["41"])}; '
        light += f'shadowCameraTop: {5*fabs(d["42"])}; '
        light += f'shadowCameraRight: {5*fabs(d["41"])}; '

    color = d.get('COLOR', '')

    if d['TYPE'] == 'directional' or d['TYPE'] == 'spot':
        light += f'target: #{identity}-target; '
        blob = f'=;light=:{light}=;tag=:a-entity=;color=:{color}'
        blob += f'=;layer=:{d["layer"]}=;closing=:0'
        page.ent_dict[identity] += blob
        blob = f'id=:{identity + "-target"}=;position=:0 -1 0=;tag=:a-entity'
        blob += f'=;layer=:{d["layer"]}=;closing=:{close_entity(page, d)+1}'
        page.ent_dict[identity + '-target'] = blob

    else:
        blob = f'=;light=:{light}=;tag=:a-entity=;color=:{color}'
        blob += f'=;layer=:{d["layer"]}=;closing=:{close_entity(page, d)}'
        page.ent_dict[identity] += blob

    return

def make_text(page, d):
    d['ide'] = 'text'
    d['dx'] = d['dy'] = d['dz'] = 0

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
    identity = open_entity(page, d)
    text = f'width: {d["41"]}; align: {d["ALIGN"]}; '
    text += f'value: {d["TEXT"]}; wrap-count: {wrapcount}; '
    color = d.get('COLOR', '')
    blob = f'=;text=:{text}=;color=:{color}=;tag=:a-entity'
    blob += f'=;layer=:{d["layer"]}=;closing=:{close_entity(page, d)}'
    page.ent_dict[identity] += blob
    return

def make_link(page, d):
    d['ide'] = 'link'

    d['dx'] = d['dy'] = d['dz'] = 0
    d['tag'] = 'a-link'
    #make sure entity is not rigged
    d['animation'] = False

    identity = open_entity(page, d)
    scale = f'{round(d["41"], 4)} {round(d["43"], 4)} 0'
    link = add_link_part(page, d)
    blob = f'=;scale=:{scale}=;href=:{link[0]}=;tag=:a-link'
    blob += f'=;title=:{link[1]}=;image=:{link[2]}'
    blob += f'=;layer=:{d["layer"]}=;closing=:1'
    page.ent_dict[identity] += blob
    return

def make_object(page, d):
    """Object block

    Block loads a Object Model (Wavefront) along with it's *.mtl file. PARAM1
    must be equal to *.obj and *.mtl filename (use lowercase extension). Files
    must share same filename and must be loaded in the media/document folder.
    If PARAM2 is set to 'scale', object will be scaled.
    """
    identity = f'{page.id}-model-{d["num"]}'
    position = f'0 {round(-d["43"]/2, 4)} 0'
    blob = f'id=:{identity}=;position=:{position}'
    if d['PARAM2'] == 'scale':
        blob += f'=;scale=:{round(fabs(d["41"]), 4)} {round(fabs(d["43"]), 4)} '
        blob += f'{round(fabs(d["42"]), 4)}'
    if d['NAME'] == 'obj-mtl':
        blob += f'=;obj-model=:{d["PARAM1"]}'
    elif d['NAME'] == 'gltf':
        blob += f'=;gltf-model=:{d["PARAM1"]}'
    blob += f'=;layer=:{d["layer"]}=;tag=:{d["tag"]}=;closing=:{d["closing"]+1}'
    page.ent_dict[identity] = blob

    return

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

    return oput#TODO

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
    return oput#TODO

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
    return oput#TODO

def make_grl(page, d):
    lines = blobs.get_grl_blob().splitlines()
    for line in lines:
        line.replace('id:=', f'id:={page.id}-grl-{d["num"]}-')
        pairs = line.split(';=')
        couple = pairs[0].split(':=')
        identity = couple[1]
        page.ent_dict[identity] = line
    closing = d['closing']+1
    page.ent_dict[identity] = line.replace('closing=:1',
        f'closing=:{closing}')
    return

def open_entity(page, d):

    if d['animation']:
        if d['RIG']:
            identity = f'{page.id}-{d["ide"]}-{d["num"]}-rig'
            pos = make_position(d)
            rot = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
            blob = f'id:={identity}=;position=:{pos}=;rotation=:{rot}'
            blob += '=;closing:=0=;tag=:a-entity'
            page.ent_dict[identity] = blob
            if d['PROPERTY'] == 'orbit':
                identity = f'{page.id}-{d["ide"]}-{d["num"]}-leash'
                l = d['TO'].split()
                d['FROM'] = '0 0 0'
                d['TO'] = '0 360 0'
                d['START_EVENTS'] = d['DIRECTION'] = ''
                d['LOOP'] = 'true; autoplay: true; easing: linear'
                anime = add_animation(page, d)
                blob = f'id:={identity}=;animation=:{anime}'
                blob += '=;closing:=0=;tag=:a-entity'
                page.ent_dict[identity] = blob

                identity = make_insertion(page, d)
                pos = f'{l[0]} {l[1]} {l[2]}'
                page.ent_dict[identity] += f'=;position=:{pos}'
            else:
                identity = make_insertion(page, d)
                anime = add_animation(page, d)
                page.ent_dict[identity] += f'=;animation=:{anime}'
        else:
            if d['PROPERTY'] == 'rotation':
                identity = f'{page.id}-{d["ide"]}-{d["num"]}-rig'
                pos = make_position(d)
                anime = add_animation(page, d)
                blob = f'id:={identity}=;position=:{pos}=;animation=:{anime}'
                blob += '=;closing:=0=;tag=:a-entity'
                page.ent_dict[identity] = blob

                identity = make_insertion(page, d)
                rot = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
                page.ent_dict[identity] += f'=;rotation=:{rot}'
            elif d['PROPERTY'] == 'orbit':
                identity = f'{page.id}-{d["ide"]}-{d["num"]}-rig'
                pos = make_position(d)
                rot = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
                l = d['TO'].split()
                d['FROM'] = '0 0 0'
                d['TO'] = '0 360 0'
                d['START_EVENTS'] = d['DIRECTION'] = ''
                d['LOOP'] = 'true; autoplay: true; easing: linear'
                anime = add_animation(page, d)
                blob = f'id:={identity}=;position=:{pos}=;rotation=:{rot}'
                blob += f'=;animation=:{anime}=;closing:=0=;tag=:a-entity'
                page.ent_dict[identity] = blob

                identity = make_insertion(page, d)
                pos = f'{l[0]} {l[1]} {l[2]}'
                page.ent_dict[identity] += f'=;position=:{pos}'
            else:
                identity = make_insertion(page, d)
                pos = make_position(d)
                rot = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
                anime = add_animation(page, d)
                blob = f'=;position=:{pos}=;rotation=:{rot}=;animation=:{anime}'
                blob += f'=;closing:=0=;tag=:a-entity'
                page.ent_dict[identity] += blob
    else:
        identity = make_insertion(page, d)
        pos = make_position(d)
        rot = f'{round(d["210"], 4)} {round(d["50"], 4)} {round(d["220"], 4)}'
        blob = f'=;position=:{pos}=;rotation=:{rot}'
        page.ent_dict[identity] += blob

    return identity

def make_insertion(page, d):

    if d['ID']:
        identity = f'{page.id}-{d["ID"]}'
    else:
        identity = f'{page.id}-{d["ide"]}-{d["num"]}'
    page.ent_dict[identity] = f'id=:{identity}'
    if d['PROPERTY'] == 'checkpoint':
        page.ent_dict[identity] += f'=;extras=:checkpoint'
    elif d['PROPERTY'] == 'look-at':
        if d['TARGET']:
            page.ent_dict[identity] += f'=;look-at:=#{page.id}-{d["TARGET"]}'
        else:
            page.ent_dict[identity] += '=;look-at:=#camera'
    elif d['PROPERTY'] == 'stalker':
        page.ent_dict[identity] += '=;look-at:=#camera'
    elif d['PROPERTY'] == 'event':
        blob = f'=;event-proxy=:listen: {d["START_EVENTS"]}; '
        blob += f'emit: {page.id}-{d["ID"]}; '
        blob += f'target: #{page.id}-{d["TARGET"]}; '
        page.ent_dict[identity] += blob

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

    #if d['PROPERTY'] == 'stalker':
        #oput += add_stalker(page, d)
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
    return closing#lacks stalker part

def entity_geometry(d):
    attr_dict = {
        'a-cone': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-cylinder': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-circle': ('SEGMENTS', 'THETA-LENGTH', 'THETA-START', ),
        'a-curvedimage': ('THETA-LENGTH', 'THETA-START', ),
        'a-sphere': ('PHI-LENGTH', 'PHI-START', 'SEGMENTS-HEIGHT', 'SEGMENTS-WIDTH', 'THETA-LENGTH', 'THETA-START', ),
    }
    attributes = attr_dict[d['2']]
    blob = ''
    for attribute in attributes:
        try:
            if d[attribute]:
                blob += f'=;{attribute.lower()}=:{d[attribute]}'
        except:
            pass

    return blob

def add_animation(page, d):
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
    if d['START_EVENTS'] == 'click':
        oput += f'startEvents: {d["START_EVENTS"]}; '
    else:
        oput += f'startEvents: {page.id}-{d["START_EVENTS"]}; '
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
    return oput#TODO

def add_link_part(page, d):
    #since we are still in dxf page, tree links are just placeholders
    if (d['LINK'] == 'parent' or d['LINK'] == 'child' or
        d['LINK'] == 'previous' or d['LINK'] == 'prev' or d['LINK'] == 'next'):
        link = f'#{d["LINK"]}'
    else:
        link = f'{d["LINK"]}'
    if d['TITLE']:
        title = f'{d["TITLE"]}'
    else:
        title = 'Title'
    image = '#default-sky'
    return link, title, image

def unit(nounit):
    #returns positive/negative scaling
    if nounit == 0:
        return 0
    unit = fabs(nounit)/nounit
    return unit

def entity_material(d):#should be eliminated, only called in make_tree
    #returns object material
    oput = ''
    if d['wireframe']:
        oput += f'material="wireframe: true; color: {d[d["prefix"]+"_color"]}; '
    else:
        oput += f'material="src: #{d[d["prefix"]+"_image"]}; color: {d[d["prefix"]+"_color"]};'
        if d[d['prefix']+'_repeat']:
            oput += f' repeat:{d["rx"]} {d["ry"]};'
    return oput

def prepare_material_values(values, d):#should be eliminated, only called in make_tree

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
