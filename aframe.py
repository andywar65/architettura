import os, html
from math import radians, sin, cos, asin, degrees, pi, sqrt, pow, fabs, atan2
from django.conf import settings

from architettura import blocks

def get_layer_list(page):
    """Gets layer list from DXF file.

    Skips some default layers. Returns a list.
    """
    path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', page.dxf_file.filename)
    dxf_f = open(path_to_dxf, encoding = 'utf-8')

    layer_list = []
    value = 'dummy'

    while value !='ENTITIES':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value == 'AcDbLayerTableRecord':#list of layer names
            key = dxf_f.readline().strip()
            layer_name = dxf_f.readline().strip()
            if layer_name == 'Defpoints' or layer_name == 'vectors' or layer_name == 'meshes' or layer_name == 'frustum' or layer_name == '3D':
                pass
            else:
                layer_list.append(layer_name)

        elif value=='EOF' or key=='':#security to avoid loops if file is corrupted
            dxf_f.close()
            return layer_list

    dxf_f.close()
    return layer_list

def get_object_dict(page):
    """Gets MTL (filename) of object blocks from DXF file.

    Scans file to see if object entities have PARAM1 attribute and collects
    material names into a dictionary, so no name will be repeated.
    """
    path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', page.dxf_file.filename)
    dxf_f = open(path_to_dxf, encoding = 'utf-8')

    object_dict = {}
    value = 'dummy'
    flag = False
    attr_value = ''

    while value !='ENTITIES':#skip up to ENTITIES section
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return collection

    while value !='ENDSEC':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return object_dict

        if flag == 'attrib':#stores values for attributes within block
            if key == '1':#attribute value
                attr_value = value
            elif key == '2':#attribute key
                if value == 'NAME':
                    if attr_value == 'obj-mtl':
                        flag = 'object'
        elif flag == 'object':#stores values for attributes within object block
            if key == '1':#attribute value
                attr_value = value
            elif key == '2':#attribute key
                if value == 'PARAM1':
                    if page.object_repository:
                        object_dict[attr_value] = page.object_repository
                    else:
                        object_dict[attr_value] = os.path.join(settings.MEDIA_URL, 'documents')
                    flag = False
        if key == '0' and flag != 'object':

            if value == 'ATTRIB':#start attribute
                flag = 'attrib'

    dxf_f.close()

    return object_dict

def get_entity_material(page):
    """Gets material dictionary from DXF file.

    Scans file to see if entities have MATERIAL attribute and collects material
    name into a dictionary, so no name will be repeated.
    """
    path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', page.dxf_file.filename)
    dxf_f = open(path_to_dxf, encoding = 'utf-8')

    material_dict = {}
    value = 'dummy'
    flag = False
    attr_value = ''

    while value !='ENTITIES':#skip up to ENTITIES section
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return collection

    while value !='ENDSEC':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return material_dict

        if flag == 'attrib':#stores values for attributes within block
            if key == '1':#attribute value
                attr_value = value
            elif key == '2':#attribute key
                if value == 'MATERIAL':
                    material_dict[attr_value] = 'path'
                flag = False
        if key == '0':


            if value == 'ATTRIB':#start attribute
                flag = 'attrib'

    dxf_f.close()
    return material_dict

def parse_dxf(page, material_dict, layer_dict):
    """Collects entities from DXF file.

    This function does too many things and maybe should be cut down. Scans
    file for 3Dfaces, lines, polylines and blocks. Assigns values to each
    entity, including geometric and appearance values plus functional
    attributes. Returns a nested dictionary.
    """
    path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', page.dxf_file.filename)
    dxf_f = open(path_to_dxf, encoding = 'utf-8')

    collection = {}
    flag = False
    x = 0
    value = 'dummy'

    while value !='ENTITIES':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value == 'AcDbLayerTableRecord':#dict of layer names and colors
            key = dxf_f.readline().strip()
            layer_name = dxf_f.readline().strip()
            key = dxf_f.readline().strip()
            value = dxf_f.readline().strip()
            key = dxf_f.readline().strip()
            if layer_name in layer_dict:
                layer_dict[layer_name].append(cad2hex(dxf_f.readline().strip()))
            else:
                value = dxf_f.readline().strip()

        elif value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return collection

    while value !='ENDSEC':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return collection

        if flag == 'ent':#stores values for all entities (with arbitrary axis algorithm)
            d = store_entity_values(d, key, value)

        elif flag == 'attrib':#stores values for attributes within block
            if key == '1':#attribute value
                attr_value = html.escape(value, quote=True)
            elif key == '2':#attribute key
                d[value] = attr_value
                flag = 'ent'#restore block modality

        if key == '0':

            if value == 'ATTRIB':#start attribute within block
                attr_value = ''
                flag = 'attrib'

            elif flag == 'ent':#close all other entities
                layer = layer_dict[d['layer']]
                invisible = layer[1]
                if invisible:
                    flag = False
                else:
                    d['wireframe'] = layer[2]
                    d['wf_width'] = layer[3]
                    d['color'] = d.get('color', layer[4])
                    d['8'] = d['image'] = layer[0]
                    d['repeat'] = False#TO DELETE?
                    d['MATERIAL'] = d.get('MATERIAL', layer[0])
                    d['pool'] = {}
                    if d['MATERIAL'] == '':
                        d['MATERIAL'] = layer[0]
                    if d['MATERIAL'] != 'default':
                        component_pool = material_dict[d['MATERIAL']]
                        if component_pool:
                            d['pool'] = component_pool

                    if d['ent'] == 'a-triangle':
                        d['2'] = 'a-triangle'#TO DELETE

                        d['num'] = x
                        collection[x] = d

                        if d['12']!=d['13'] or d['22']!=d['23'] or d['32']!=d['33']:
                            d2 = d.copy()
                            d2['11'] = d['12']
                            d2['12'] = d['13']
                            d2['21'] = d['22']
                            d2['22'] = d['23']
                            d2['31'] = d['32']
                            d2['32'] = d['33']
                            x += 1
                            d2['num'] = x
                            collection[x] = d2

                        flag = False

                    elif d['ent'] == 'a-poly':#close polyline
                        d['2'] = 'a-poly'
                        d['10'] = d['vx'][0]
                        d['20'] = d['vy'][0]
                        d['30'] = d['38']
                        print(d['vx'], d['vy'], d['10'], d['30'], d['20'])
                        d['num'] = x
                        collection[x] = d
                        flag = False

                    elif d['ent'] == 'a-line':#close line
                        d['2'] = 'a-line'
                        d['num'] = x
                        collection[x] = d
                        flag = False

                    elif d['ent'] == 'a-block':
                        if d['2'] == 'a-wall':
                            if d['MATERIAL2']:
                                d['pool2'] = material_dict[d['MATERIAL2']]
                            else:
                                d['MATERIAL2'] = d['MATERIAL']
                                d['pool2'] = d['pool']
                                d['TILING2'] = d['TILING']
                                d['SKIRTING2'] = d['SKIRTING']

                        d['num'] = x
                        collection[x] = d

                        flag = False

            if value == '3DFACE':#start 3D face
                d = {'ID': '', '50': 0, '210': 0, '220': 0, '230': 1,
                'ATTRIBUTE': False, 'animation': False,}#default values
                flag = 'ent'
                d['ent'] = 'a-triangle'
                x += 1

            elif value == 'INSERT':#start block
                d = {'ID': '', '41': 1, '42': 1, '43': 1, '50': 0, '210': 0, '220': 0,
                 '230': 1,'repeat': False, 'TYPE': '','NAME': '',
                 'animation': False, 'ATTRIBUTE': False,}#default values
                flag = 'ent'
                d['ent'] = 'a-block'
                x += 1

            elif value == 'LINE':#start line
                d = {'ID': '', '30': 0, '31': 0, '39': 0, '41': 1, '42': 1, '43': 1,
                '50': 0, '210': 0, '220': 0, '230': 1,
                'ATTRIBUTE': False, 'animation': False, 'repeat': False,
                'TYPE': '', 'TILING': 0, 'SKIRTING': 0}
                flag = 'ent'
                d['ent'] = 'a-line'
                x += 1

            elif value == 'LWPOLYLINE':#start polyline
                #default values
                d = {'ID': '', '38': 0,  '39': 0, '41': 1, '42': 1,
                '43': 1, '50': 0, '70': False, '210': 0, '220': 0, '230': 1,
                'vx': [], 'vy': [], 'ATTRIBUTE': False,
                'animation': False, 'repeat': False,
                'TYPE': '', 'TILING': 0, 'SKIRTING': 0}
                flag = 'ent'
                d['ent'] = 'a-poly'
                x += 1

    return collection

def store_entity_values(d, key, value):
    if key == '2':#block name
        d[key] =  html.escape(value, quote=True)
    if key == '8':#layer name
        d['layer'] = d[key] =  html.escape(value, quote=True)
    elif key == '10':#X position
        if d['ent'] == 'a-poly':
            d['vx'].append(float(value))
        else:
            d[key] = float(value)
    elif key == '20':#mirror Y position
        if d['ent'] == 'a-poly':
            d['vy'].append(-float(value))
        else:
            d[key] = -float(value)
    elif key == '11' or key == '12' or key == '13':#X position
        d[key] = float(value)
    elif key == '21' or key == '22' or key == '23':#mirror Y position
        d[key] = -float(value)
    elif key == '30' or key == '31' or key == '32' or key == '33':#Z position
        d[key] = float(value)
    elif key == '38' or  key == '39':#elevation and thickness
        d[key] = float(value)
    elif key == '41' or key == '42' or key == '43':#scale values
        d[key] = float(value)
    elif key == '50':#Z rotation
        d[key] = float(value)
    elif key == '62':#color
        d['color'] = cad2hex(value)
    elif key == '70' and value == '1':#closed
        d['70'] = True
    elif key == '90':#vertex num
        d[key] = int(value)
    elif key == '210':#X of OCS unitary vector
        d['Az_1'] = float(value)
        if d['ent'] == 'a-poly':
            d['10'] = d['vx'][0]
        d['P_x'] = d['10']
    elif key == '220':#Y of OCS unitary vector
        d['Az_2'] = float(value)
        if d['ent'] == 'a-poly':
            d['20'] = -d['vy'][0]
        d['P_y'] = -d['20']#reset original value
    elif key == '230':#Z of OCS unitary vector
        Az_3 = float(value)
        if d['ent'] == 'a-poly':
            d['30'] = d.get('38', 0)
        P_z = d['30']
        #arbitrary axis algorithm
        #see if OCS z vector is close to world Z axis
        if fabs(d['Az_1']) < (1/64) and fabs(d['Az_2']) < (1/64):
            W = ('Y', 0, 1, 0)
        else:
            W = ('Z', 0, 0, 1)
        #cross product for OCS x arbitrary vector, normalized
        Ax_1 = W[2]*Az_3-W[3]*d['Az_2']
        Ax_2 = W[3]*d['Az_1']-W[1]*Az_3
        Ax_3 = W[1]*d['Az_2']-W[2]*d['Az_1']
        Norm = sqrt(pow(Ax_1, 2)+pow(Ax_2, 2)+pow(Ax_3, 2))
        Ax_1 = Ax_1/Norm
        Ax_2 = Ax_2/Norm
        Ax_3 = Ax_3/Norm
        #cross product for OCS y arbitrary vector, normalized
        Ay_1 = d['Az_2']*Ax_3-Az_3*Ax_2
        Ay_2 = Az_3*Ax_1-d['Az_1']*Ax_3
        Ay_3 = d['Az_1']*Ax_2-d['Az_2']*Ax_1
        Norm = sqrt(pow(Ay_1, 2)+pow(Ay_2, 2)+pow(Ay_3, 2))
        Ay_1 = Ay_1/Norm
        Ay_2 = Ay_2/Norm
        Ay_3 = Ay_3/Norm
        #insertion world coordinates from OCS
        d['10'] = d['P_x']*Ax_1+d['P_y']*Ay_1+P_z*d['Az_1']
        d['20'] = d['P_x']*Ax_2+d['P_y']*Ay_2+P_z*d['Az_2']
        d['30'] = d['P_x']*Ax_3+d['P_y']*Ay_3+P_z*Az_3
        #OCS X vector translated into WCS
        Ax_1 = ((d['P_x']+cos(radians(d['50'])))*Ax_1+(d['P_y']+sin(radians(d['50'])))*Ay_1+P_z*d['Az_1'])-d['10']
        Ax_2 = ((d['P_x']+cos(radians(d['50'])))*Ax_2+(d['P_y']+sin(radians(d['50'])))*Ay_2+P_z*d['Az_2'])-d['20']
        Ax_3 = ((d['P_x']+cos(radians(d['50'])))*Ax_3+(d['P_y']+sin(radians(d['50'])))*Ay_3+P_z*Az_3)-d['30']
        #cross product for OCS y vector, normalized
        Ay_1 = d['Az_2']*Ax_3-Az_3*Ax_2
        Ay_2 = Az_3*Ax_1-d['Az_1']*Ax_3
        Ay_3 = d['Az_1']*Ax_2-d['Az_2']*Ax_1
        Norm = sqrt(pow(Ay_1, 2)+pow(Ay_2, 2)+pow(Ay_3, 2))
        Ay_1 = Ay_1/Norm
        Ay_2 = Ay_2/Norm
        Ay_3 = Ay_3/Norm

        #A-Frame rotation order is Yaw(Z), Pitch(X) and Roll(Y)
        #thanks for help Marilena Vendittelli and https://www.geometrictools.com/
        if Ay_3<1:
            if Ay_3>-1:
                pitch = asin(Ay_3)
                yaw = atan2(-Ay_1, Ay_2)
                roll = atan2(-Ax_3, Az_3)
            else:
                pitch = -pi/2
                yaw = -atan2(d['Az_1'], Ax_1)
                roll = 0
        else:
            pitch = pi/2
            yaw = atan2(d['Az_1'], Ax_1)
            roll = 0

        #Y position, mirrored
        d['20'] = -d['20']
        #rotations from radians to degrees
        d['210'] = degrees(pitch)
        d['50'] = degrees(yaw)
        d['220'] = -degrees(roll)
    return d

def reference_openings(collection):
    """Compares each door entity with each wall.

    Has two helper functions, straight case and tilted case, but latter has not
    been implemented yet. Returns modified entity collection.
    """
    collection2 = collection.copy()
    for x, d in collection.items():
        if d['2'] == 'a-door':
            collection[x] = d
            for x2, d2 in collection2.items():
                if d2['2'] == 'a-wall':
                    flag = True
                    values = [d['210'], d['220'], d2['210'], d2['220']]
                    for v in values:
                        if fabs(v)>1:
                            flag = False
                    if flag:
                        d2 = door_straight_case(d, d2)
                    else:
                        d2 = door_tilted_case(d, d2)
                    collection[x2] = d2

    return collection

def door_straight_case(d, d2):
    """Cheks if door bounding box is inside wall bounding box.

    Works if both blocks are not rotated on X and Y axis and if insertion point
    is on the same plane. Returns modified wall info.
    """
    flag = False
    if fabs(d['50'] - d2['50'])<1:
        flag = True
        back = 1
    elif fabs(d['50'] - 180 - d2['50'])<1:
        flag = True
        back = -1
    elif fabs(d['50'] + 180 - d2['50'])<1:
        flag = True
        back = -1
    if fabs(d['30'] - d2['30'])>.01:
        flag = False
    if d['43']<0 or d2['43']<0:
        flag = False
    if flag:
        #translation
        xt = d['10']-d2['10']
        zt = d['20']-d2['20']
        #rotation
        alfa = radians(d2['50'])
        xd = xt*cos(alfa)-zt*sin(alfa)
        zd = (xt*sin(alfa)+zt*cos(alfa))*back*fabs(d2['42'])/d2['42']*fabs(d['42'])/d['42']
        xde = xd + d['41']*back
        zde = zd + d['42']*back
        xwe = d2['41']
        zwe = d2['42']
        if xde > xd:
            xdmax = xde
            xdmin = xd
        else:
            xdmax = xd
            xdmin = xde
        if zde > zd:
            zdmax = zde
            zdmin = zd
        else:
            zdmax = zd
            zdmin = zde
        if xwe > 0:
            xwmax = xwe
            xwmin = 0
        else:
            xwmax = 0
            xwmin = xwe
        if zwe > 0:
            zwmax = zwe
            zwmin = 0
        else:
            zwmax = 0
            zwmin = zwe
        if xdmin - xwmin < -0.01:
            flag = False
        elif zdmin -zwmin < -0.01:
            flag = False
        elif xwmax - xdmax < -0.01:
            flag = False
        elif zwmax - zdmax < -0.01:
            flag = False
        if flag:
            d2['door'] = d['num']
            d2['2'] = 'a-openwall'
            if d['43']>d2['43']:
                d2['door_height'] = d2['43']
            else:
                d2['door_height'] = d['43']
            if d2['41']>0:
                d2['door_off_1'] = xdmin
                d2['door_off_2'] = xdmax
            else:
                d2['door_off_1'] = xdmax - xwmax
                d2['door_off_2'] = xdmin - xwmax

    return d2

def door_tilted_case(d, d2):
    """Not working yet.
    """
    d210 = d['210']*fabs(d['41'])/d['41']
    d220 = d['220']*fabs(d['42'])/d['42']
    d50 = d['50']*fabs(d['43'])/d['43']
    w210 = d2['210']*fabs(d2['41'])/d2['41']
    w220 = d2['220']*fabs(d2['42'])/d2['42']
    w50 = d2['50']*fabs(d2['43'])/d2['43']
    return d2

def reference_animations(collection):
    """Assigns animations and masons.

    Controls if animation / checkpoint / mason block shares insertion point with
    other blocks. Animation / checkpoint / mason attributes will be appended to
    selected block. Returns nested dictionary.
    """
    collection2 = collection.copy()
    for x, d in collection.items():
        if d['2'] == 'a-animation' or d['2'] == 'a-mason':
            for x2, d2 in collection2.items():
                if x == x2:
                    pass
                else:
                    dx = fabs(d['10']-d2['10'])
                    dy = fabs(d['20']-d2['20'])
                    dz = fabs(d['30']-d2['30'])
                    if dx < 0.01 and dy < 0.01 and dz < 0.01:
                        if d['2'] == 'a-mason':
                            d2['MATERIAL'] = d['MATERIAL']
                            d2['pool'] = d['pool']
                            d2['TILING'] = d['TILING']
                            d2['SKIRTING'] = d['SKIRTING']

                        elif d['2'] == 'a-animation':
                            d2['animation'] = True
                            if d['ATTRIBUTE'] == 'stalker':
                                d2['animation'] = False
                            elif d['ATTRIBUTE'] == 'look-at':
                                d2['animation'] = False
                            elif d['ATTRIBUTE'] == 'checkpoint':
                                d2['animation'] = False
                            d2['ATTRIBUTE'] = d['ATTRIBUTE']
                            d2['FROM'] = d['FROM']
                            d2['TO'] = d['TO']
                            d2['BEGIN'] = d['BEGIN']
                            d2['DIRECTION'] = d['DIRECTION']
                            d2['REPEAT'] = d['REPEAT']
                            d2['DURATION'] = d['DURATION']
                            d2['TARGET'] = d['TARGET']
                            d2['TEXT'] = d['TEXT']
                            d2['LINK'] = d['LINK']
                            d2['RIG'] = d['RIG']

                        collection[x2] = d2
    return collection

def make_html(page, collection, mode):
    entities_dict = {}
    if mode == 'ar':
        no_camera = False
    else:
        no_camera = True
    for x, d in collection.items():

        if d['2'] == 'a-camera' and no_camera:
            no_camera = False
            entities_dict[x] = make_camera(page, d, mode)
        elif d['2'] == 'a-box':
            entities_dict[x] = blocks.make_box(page, d)
        elif d['2'] == 'a-cone' or d['2'] == 'a-cylinder' or d['2'] == 'a-circle' or d['2'] == 'a-sphere':
            entities_dict[x] = blocks.make_circular(page, d)
        elif d['2'] == 'a-curvedimage':
            entities_dict[x] = blocks.make_curvedimage(page, d)
        elif d['2'] == 'a-plane':
            entities_dict[x] = blocks.make_plane(page, d)
        elif d['2'] == 'a-triangle':
            entities_dict[x] = blocks.make_triangle(page, d)
        elif d['2'] == 'a-line':
            entities_dict[x] = blocks.make_line(page, d)
        elif d['2'] == 'a-poly':
            entities_dict[x] = blocks.make_poly(page, d)
        elif d['2'] == 'a-wall':
            entities_dict[x] = blocks.make_bim_block(page, d)
        elif d['2'] == 'a-door':
            entities_dict[x] = blocks.make_bim_block(page, d)
        elif d['2'] == 'a-slab':
            entities_dict[x] = blocks.make_bim_block(page, d)
        elif d['2'] == 'a-openwall':
            entities_dict[x] = blocks.make_bim_block(page, d)
        elif d['2'] == 'a-block':
            d['NAME'] = d.get('NAME', 't01')
            entities_dict[x] = blocks.make_block(page, d)

        elif d['2'] == 'a-animation' or d['2'] == 'a-mason':
            pass
        else:
            entities_dict[x] = make_entities(page, d)

    if no_camera:
        x += 1
        d = {
        '10': 0, '20': 0, '30': 0, '210': 0, '50': 0, '220': 0,  '43': 1,
        'LIGHT-INT': 1,
        }
        entities_dict[x] = make_camera(page, d, mode)

    return entities_dict

def make_entities(page, d):

    oput = ''

    d = prepare_coordinates(d)

    oput += prepare_insertion(page, d)

    if d['2'] == 'a-light':
        oput += blocks.make_light(page, d)
    elif d['2'] == 'a-link':
        oput += blocks.make_link(page, d)
    elif d['2'] == 'a-text':
        oput += blocks.make_text(d)
    #make animations (is animation)
    if d['animation']:
        oput += add_animation(d)
    #make stalker balloon and link
    if d['ATTRIBUTE'] == 'stalker':
        oput += add_stalker(page, d)

    oput += '</a-entity> <!--close handle-->\n'
    if d['animation'] or d['ATTRIBUTE'] == 'stalker' or d['ATTRIBUTE'] == 'checkpoint':
        oput += '</a-entity> <!--close animation rig-->\n'
    oput += '</a-entity> <!--close insertion-->\n'
    return oput

def prepare_coordinates(d):
    insertion = {'a-box': 'v', 'a-cone': 'c', 'a-cylinder': 'c', 'a-line': 'l',
    'a-circle': '0', 'a-curvedimage': 'c', 'a-sphere': 'c2', 'a-triangle': 't',
    'a-poly': 'p', 'a-block': 'c', 'a-wall': 'v', 'a-door': 'v', 'a-slab': 'v2',
    'a-openwall': 'v', 'a-plane': 'pl', 'a-light': '0', 'a-link': '0', 'a-text': '0',
    }
    d['xg'] = d['yg'] = d['zg'] = 0
    d['xs'] = d['ys'] = d['zs'] = 0
    #position of gravity center from insertion point
    if insertion[d['2']] == 'v':
        d['xg'] = d['41']/2
        d['yg'] = -d['42']/2
        d['zg'] = d['43']/2
    elif insertion[d['2']] == 'v2':
        d['xg'] = d['41']/2
        d['yg'] = -d['42']/2
        d['zg'] = -d['43']/2
    elif insertion[d['2']] == 'pl':
        d['xg'] = d['41']/2
        d['zg'] = d['43']/2
    elif insertion[d['2']] == 'c':
        d['zg'] = d['43']/2
    elif insertion[d['2']] == 'c2':
        d['zg'] = d['43']
    elif insertion[d['2']] == 'l':
        d['xg'] = d['11']/2
        d['yg'] = d['21']/2
        d['39'] = d.get('39', 0)
        if d['39']:#it has thickness?
            d['zg'] = d['39']/2
        else:
            d['zg'] = d['31']/2
    elif insertion[d['2']] == 't':
        d['xg'] = (d['11'] + d['12'])/3
        d['yg'] = (d['21'] + d['22'])/3
        d['zg'] = (d['31'] + d['32'])/3
    elif insertion[d['2']] == 'p':
        xmax = xmin = 0
        ymax = ymin = 0
        for i in range(1, d['90']):
            if d['vx'][i] < xmin:
                xmin = d['vx'][i]
            elif d['vx'][i] > xmax:
                xmax = d['vx'][i]
            if d['vy'][i] < ymin:
                ymin = d['vy'][i]
            elif d['vy'][i] > ymax:
                ymax = d['vy'][i]

        d['xg'] = (xmax + xmin)/2
        d['yg'] = (ymax + ymin)/2
        d['39'] = d.get('39', 0)
        if d['39']:#it has thickness?
            d['zg'] = d['39']/2

    if 'ATTRIBUTE' in d:
        if d['ATTRIBUTE'] == 'stalker' or d['ATTRIBUTE'] == 'checkpoint':
            d['xs'] = d['xg']
            d['ys'] = d['yg']
            d['xg'] = d['yg'] = 0
        elif d['ATTRIBUTE'] == 'look-at':
            pass
        else:
            d['xs'] = d['xg']
            d['ys'] = d['yg']
            d['zs'] = d['zg']
            d['xg'] = d['yg'] = d['zg'] = 0
    else:
        d['ATTRIBUTE'] = False

    return d

def prepare_insertion(page, d):
    oput = ''
    oput += f'<a-entity id="{d["2"]}-{d["num"]}-insert" \n'
    oput += f'position="{d["10"]} {d["30"]} {d["20"]}" \n'
    oput += f'rotation="{d["210"]} {d["50"]} {d["220"]}"> \n'
    if d['animation']:
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-animation-rig" \n'
        oput += f'position="{d["xs"]} {d["zs"]} {d["ys"]}"> \n'
    elif d['ATTRIBUTE'] == 'stalker':
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-stalker" \n'
        oput += 'look-at="#camera-foot" \n'
        oput += f'position="{d["xs"]} 0 {d["ys"]}"> \n'
    elif d['ATTRIBUTE'] == 'checkpoint':
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-checkpoint" \n'
        oput += 'checkpoint \n'
        oput += f'position="{d["xs"]} 0 {d["ys"]}"> \n'
    #handle
    if d['ID']:
        oput += f'<a-entity id="{d["ID"]}" \n'
    else:
        oput += f'<a-entity id="{d["2"]}-{d["num"]}-handle" \n'
    oput += f'position="{d["xg"]} {d["zg"]} {d["yg"]}" \n'
    if page.shadows:
        if d['2'] == 'a-curvedimage':
            oput += 'shadow="receive: false; cast: false" \n'
        elif d['2'] == 'a-light':
            pass
        else:
            oput += 'shadow="receive: true; cast: true" \n'
    if d['ATTRIBUTE'] == 'look-at':
        if d['TARGET']:
            oput += f'look-at="#{d["TARGET"]}" \n'
        else:
            oput += 'look-at="#camera" \n'
    oput += '> \n'
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

def make_block(page, d):
    oput = ''
    if d['NAME'] == 'obj-mtl':
        oput += blocks.make_object(d)
    if d['NAME'] == 't01':
        oput += blocks.make_table_01(d)
    if d['NAME'] == 'tree':
        oput += blocks.make_tree(d)
    return oput

def make_camera(page, d, mode):
    oput = f'<a-entity id="camera-ent" position="{d["10"]} {d["30"]} {d["20"]}" \n'
    oput += f'rotation="{d["210"]} {d["50"]} {d["220"]}" \n'
    if mode == 'digkom':
        oput += 'movement-controls="controls: checkpoint" checkpoint-controls="mode: animate"> \n'
        oput += f'<a-camera id="camera" look-controls="pointerLockEnabled: true" wasd-controls="enabled: true" '
        oput += f' position="0 {d["43"]*1.6} 0"> \n'
        oput += '<a-cursor color="black"></a-cursor> \n'
    else:
        oput += '> \n'
        oput += f'<a-camera id="camera" wasd-controls="fly: {str(page.fly_camera).lower() }" '
        oput += f' position="0 {d["43"]*1.6} 0"> \n'
        oput += '<a-cursor color="#2E3A87"></a-cursor> \n'

    oput += f'<a-light type="point" distance="10" intensity="{d["LIGHT-INT"]}"></a-light> \n'
    oput += f'<a-entity position="0 {-d["43"]*1.6} 0" id="camera-foot"></a-entity> \n'
    oput += '</a-camera></a-entity> \n'
    return oput

def cad2hex(cad_color):
    cad_color = abs(int(cad_color))
    if cad_color<0 or cad_color>255:
        return '#ffffff'
    else:
        RGB_list = (
        		 (0, 0, 0),
        		 (255, 0, 0),
        		 (255, 255, 0),
        		 (0, 255, 0),
        		 (0, 255, 255),
        		 (0, 0, 255),
        		 (255, 0, 255),
        		 (255, 255, 255),
        		 (128, 128, 128),
        		 (192, 192, 192),
        		 (255, 0, 0),
        		 (255, 127, 127),
        		 (165, 0, 0),
        		 (165, 82, 82),
        		 (127, 0, 0),
        		 (127, 63, 63),
        		 (76, 0, 0),
        		 (76, 38, 38),
        		 (38, 0, 0),
        		 (38, 19, 19),
        		 (255, 63, 0),
        		 (255, 159, 127),
        		 (165, 41, 0),
        		 (165, 103, 82),
        		 (127, 31, 0),
        		 (127, 79, 63),
        		 (76, 19, 0),
        		 (76, 47, 38),
        		 (38, 9, 0),
        		 (38, 23, 19),
        		 (255, 127, 0),
        		 (255, 191, 127),
        		 (165, 82, 0),
        		 (165, 124, 82),
        		 (127, 63, 0),
        		 (127, 95, 63),
        		 (76, 38, 0),
        		 (76, 57, 38),
        		 (38, 19, 0),
        		 (38, 28, 19),
        		 (255, 191, 0),
        		 (255, 223, 127),
        		 (165, 124, 0),
        		 (165, 145, 82),
        		 (127, 95, 0),
        		 (127, 111, 63),
        		 (76, 57, 0),
        		 (76, 66, 38),
        		 (38, 28, 0),
        		 (38, 33, 19),
        		 (255, 255, 0),
        		 (255, 255, 127),
        		 (165, 165, 0),
        		 (165, 165, 82),
        		 (127, 127, 0),
        		 (127, 127, 63),
        		 (76, 76, 0),
        		 (76, 76, 38),
        		 (38, 38, 0),
        		 (38, 38, 19),
        		 (191, 255, 0),
        		 (223, 255, 127),
        		 (124, 165, 0),
        		 (145, 165, 82),
        		 (95, 127, 0),
        		 (111, 127, 63),
        		 (57, 76, 0),
        		 (66, 76, 38),
        		 (28, 38, 0),
        		 (33, 38, 19),
        		 (127, 255, 0),
        		 (191, 255, 127),
        		 (82, 165, 0),
        		 (124, 165, 82),
        		 (63, 127, 0),
        		 (95, 127, 63),
        		 (38, 76, 0),
        		 (57, 76, 38),
        		 (19, 38, 0),
        		 (28, 38, 19),
        		 (63, 255, 0),
        		 (159, 255, 127),
        		 (41, 165, 0),
        		 (103, 165, 82),
        		 (31, 127, 0),
        		 (79, 127, 63),
        		 (19, 76, 0),
        		 (47, 76, 38),
        		 (9, 38, 0),
        		 (23, 38, 19),
        		 (0, 255, 0),
        		 (127, 255, 127),
        		 (0, 165, 0),
        		 (82, 165, 82),
        		 (0, 127, 0),
        		 (63, 127, 63),
        		 (0, 76, 0),
        		 (38, 76, 38),
        		 (0, 38, 0),
        		 (19, 38, 19),
        		 (0, 255, 63),
        		 (127, 255, 159),
        		 (0, 165, 41),
        		 (82, 165, 103),
        		 (0, 127, 31),
        		 (63, 127, 79),
        		 (0, 76, 19),
        		 (38, 76, 47),
        		 (0, 38, 9),
        		 (19, 38, 23),
        		 (0, 255, 127),
        		 (127, 255, 191),
        		 (0, 165, 82),
        		 (82, 165, 124),
        		 (0, 127, 63),
        		 (63, 127, 95),
        		 (0, 76, 38),
        		 (38, 76, 57),
        		 (0, 38, 19),
        		 (19, 38, 28),
        		 (0, 255, 191),
        		 (127, 255, 223),
        		 (0, 165, 124),
        		 (82, 165, 145),
        		 (0, 127, 95),
        		 (63, 127, 111),
        		 (0, 76, 57),
        		 (38, 76, 66),
        		 (0, 38, 28),
        		 (19, 38, 33),
        		 (0, 255, 255),
        		 (127, 255, 255),
        		 (0, 165, 165),
        		 (82, 165, 165),
        		 (0, 127, 127),
        		 (63, 127, 127),
        		 (0, 76, 76),
        		 (38, 76, 76),
        		 (0, 38, 38),
        		 (19, 38, 38),
        		 (0, 191, 255),
        		 (127, 223, 255),
        		 (0, 124, 165),
        		 (82, 145, 165),
        		 (0, 95, 127),
        		 (63, 111, 127),
        		 (0, 57, 76),
        		 (38, 66, 76),
        		 (0, 28, 38),
        		 (19, 33, 38),
        		 (0, 127, 255),
        		 (127, 191, 255),
        		 (0, 82, 165),
        		 (82, 124, 165),
        		 (0, 63, 127),
        		 (63, 95, 127),
        		 (0, 38, 76),
        		 (38, 57, 76),
        		 (0, 19, 38),
        		 (19, 28, 38),
        		 (0, 63, 255),
        		 (127, 159, 255),
        		 (0, 41, 165),
        		 (82, 103, 165),
        		 (0, 31, 127),
        		 (63, 79, 127),
        		 (0, 19, 76),
        		 (38, 47, 76),
        		 (0, 9, 38),
        		 (19, 23, 38),
        		 (0, 0, 255),
        		 (127, 127, 255),
        		 (0, 0, 165),
        		 (82, 82, 165),
        		 (0, 0, 127),
        		 (63, 63, 127),
        		 (0, 0, 76),
        		 (38, 38, 76),
        		 (0, 0, 38),
        		 (19, 19, 38),
        		 (63, 0, 255),
        		 (159, 127, 255),
        		 (41, 0, 165),
        		 (103, 82, 165),
        		 (31, 0, 127),
        		 (79, 63, 127),
        		 (19, 0, 76),
        		 (47, 38, 76),
        		 (9, 0, 38),
        		 (23, 19, 38),
        		 (127, 0, 255),
        		 (191, 127, 255),
        		 (82, 0, 165),
        		 (124, 82, 165),
        		 (63, 0, 127),
        		 (95, 63, 127),
        		 (38, 0, 76),
        		 (57, 38, 76),
        		 (19, 0, 38),
        		 (28, 19, 38),
        		 (191, 0, 255),
        		 (223, 127, 255),
        		 (124, 0, 165),
        		 (145, 82, 165),
        		 (95, 0, 127),
        		 (111, 63, 127),
        		 (57, 0, 76),
        		 (66, 38, 76),
        		 (28, 0, 38),
        		 (33, 19, 38),
        		 (255, 0, 255),
        		 (255, 127, 255),
        		 (165, 0, 165),
        		 (165, 82, 165),
        		 (127, 0, 127),
        		 (127, 63, 127),
        		 (76, 0, 76),
        		 (76, 38, 76),
        		 (38, 0, 38),
        		 (38, 19, 38),
        		 (255, 0, 191),
        		 (255, 127, 223),
        		 (165, 0, 124),
        		 (165, 82, 145),
        		 (127, 0, 95),
        		 (127, 63, 111),
        		 (76, 0, 57),
        		 (76, 38, 66),
        		 (38, 0, 28),
        		 (38, 19, 33),
        		 (255, 0, 127),
        		 (255, 127, 191),
        		 (165, 0, 82),
        		 (165, 82, 124),
        		 (127, 0, 63),
        		 (127, 63, 95),
        		 (76, 0, 38),
        		 (76, 38, 57),
        		 (38, 0, 19),
        		 (38, 19, 28),
        		 (255, 0, 63),
        		 (255, 127, 159),
        		 (165, 0, 41),
        		 (165, 82, 103),
        		 (127, 0, 31),
        		 (127, 63, 79),
        		 (76, 0, 19),
        		 (76, 38, 47),
        		 (38, 0, 9),
        		 (38, 19, 23),
        		 (0, 0, 0),
        		 (51, 51, 51),
        		 (102, 102, 102),
        		 (153, 153, 153),
        		 (204, 204, 204),
        		 (255, 255, 255),
        		)
        r = RGB_list[cad_color][0]
        g = RGB_list[cad_color][1]
        b = RGB_list[cad_color][2]
        hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
        return hex

def prepare_new_coordinates(d):
    sx = sin(radians(-d['210']))
    cx = cos(radians(-d['210']))
    sy = sin(radians(-d['220']))
    cy = cos(radians(-d['220']))
    sz = sin(radians(-d['50']))
    cz = cos(radians(-d['50']))
    dx = d['41']/2
    dy = -d['42']/2
    dz = d['43']/2
    #Euler angles, yaw (Z), pitch (X), roll (Y)
    d['10'] = d['10'] + (cy*cz-sx*sy*sz)*dx + (-cx*sz)*dy +  (cz*sy+cy*sx*sz)*dz
    d['20'] = d['20'] + (cz*sx*sy+cy*sz)*dx +  (cx*cz)*dy + (-cy*cz*sx+sy*sz)*dz
    d['30'] = d['30'] +         (-cx*sy)*dx +     (sx)*dy+            (cx*cy)*dz

    return d
