import os, html
from math import radians, sin, cos, asin, acos, degrees, pi, sqrt, pow, fabs, atan2
from django.conf import settings

from architettura import entities

def get_layer_list(page):
    """Gets layer list from DXF file.

    Skips some default layers. Returns a list.
    """
    dxf_f = open(page.path_to_dxf, encoding = 'utf-8')

    page.layer_dict = {}
    value = 'dummy'

    while value !='ENTITIES':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value == 'AcDbLayerTableRecord':#list of layer names
            key = dxf_f.readline().strip()
            name = dxf_f.readline().strip()
            key = dxf_f.readline().strip()
            value = dxf_f.readline().strip()
            key = dxf_f.readline().strip()
            if (name == 'Defpoints' or name == 'vectors' or name == 'meshes' or
                name == 'frustum' or name == '3D'):
                value = dxf_f.readline().strip()
            else:
                page.layer_dict[name] = ['default', False, False, False,
                    cad2hex(dxf_f.readline().strip()), 'default']
        #security to avoid loops if file is corrupted
        elif value=='EOF' or key=='':
            dxf_f.close()
            return

    dxf_f.close()
    return

def get_object_dict(page):
    """Gets MTL (filename) of object blocks from DXF file.

    Scans file to see if object entities have PARAM1 attribute and collects
    material names into a dictionary, so no name will be repeated.
    """
    dxf_f = open(page.path_to_dxf, encoding = 'utf-8')

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
                        flag = 'obj'
                    elif attr_value == 'gltf':
                        flag = 'gltf'
        elif flag == 'obj' or flag == 'gltf':#stores values for attributes within object block
            if key == '1':#attribute value
                attr_value = value
            elif key == '2':#attribute key
                if value == 'PARAM1':
                    if page.object_repository:
                        path = page.object_repository
                    else:
                        path = os.path.join(settings.MEDIA_URL, 'documents')
                    if flag == 'obj':
                        object_dict[attr_value + '.' + 'obj'] = path
                        object_dict[attr_value + '.' + 'mtl'] = path
                    else:
                        object_dict[attr_value + '.' + 'gltf'] = path
                    flag = False
        if key == '0':
            if flag != 'obj' and flag != 'gltf':
                if value == 'ATTRIB':#start attribute
                    flag = 'attrib'

    dxf_f.close()
    return object_dict

def get_entity_material(page):
    """Gets material dictionary from DXF file.

    Scans file to see if entities have MATERIAL attribute and collects material
    name into a dictionary, so no name will be repeated.
    """
    dxf_f = open(page.path_to_dxf, encoding = 'utf-8')

    page.material_dict = {}
    page.part_dict = {}
    value = 'dummy'
    flag = False
    attr_value = ''

    while value !='ENTITIES':#skip up to ENTITIES section
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return #material_dict, part_dict

    while value !='ENDSEC':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return #material_dict, part_dict

        if flag == 'attrib':#stores values for attributes within block
            if key == '1':#attribute value
                attr_value = value
            elif key == '2':#attribute key
                if value == 'MATERIAL':
                    page.material_dict[attr_value] = 'dummy'
                elif value == 'PART':
                    page.part_dict[attr_value] = 'dummy'
                flag = False
        if key == '0':


            if value == 'ATTRIB':#start attribute
                flag = 'attrib'

    dxf_f.close()
    return #material_dict, part_dict

def parse_dxf(page, material_dict, layer_dict):
    """Collects entities from DXF file.

    This function does too many things and maybe should be cut down. Scans
    file for 3Dfaces, lines, polylines and blocks. Assigns values to each
    entity, including geometric and appearance values plus functional
    attributes. Returns a nested dictionary.
    """
    dxf_f = open(page.path_to_dxf, encoding = 'utf-8')

    collection = {}
    flag = False
    x = 0
    value = 'dummy'

    while value !='ENTITIES':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        #if value == 'AcDbLayerTableRecord':#dict of layer names and colors
            #key = dxf_f.readline().strip()
            #layer_name = dxf_f.readline().strip()
            #key = dxf_f.readline().strip()
            #value = dxf_f.readline().strip()
            #key = dxf_f.readline().strip()
            #if layer_name in layer_dict:
                #layer_dict[layer_name].append(cad2hex(dxf_f.readline().strip()))
            #else:
                #value = dxf_f.readline().strip()

        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
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
                    d['no_shadows'] = layer[3]
                    d['color'] = d.get('color', layer[4])
                    d['8'] = d['image'] = layer[0]
                    d['repeat'] = False#TO DELETE?
                    d['MATERIAL'] = d.get('MATERIAL', layer[0])
                    d['pool'] = {}
                    if d['MATERIAL'] == '':
                        d['MATERIAL'] = layer[0]
                    if d['MATERIAL'] != 'default':
                        try:
                            component_pool = material_dict[d['MATERIAL']]
                            if component_pool:
                                d['pool'] = component_pool
                        except:
                            pass

                    if d['ent'] == '3df':
                        d['2'] = 'a-triangle'

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

                    elif d['ent'] == 'poly':#close polyline
                        d['2'] = 'a-poly'
                        if d['210'] == 0 and d['220'] == 0:
                            d['10'] = d['vx'][0]
                            d['20'] = d['vy'][0]
                            d['30'] = d['38']
                        d['num'] = x
                        collection[x] = d
                        flag = False

                    elif d['ent'] == 'line':#close line
                        d['2'] = 'a-line'
                        d['num'] = x
                        collection[x] = d
                        flag = False

                    elif d['ent'] == 'insert':
                        if d['2'] == 'a-window':
                            d['WMATERIAL'] = d['MATERIAL2'] = d['MATERIAL']
                            d['wpool'] = d['pool2'] = d['pool']
                            d['TILING2'] = d['TILING'] = 0
                            d['SKIRTING2'] = d['SKIRTING'] = 0
                        elif d['2'] == 'a-wall' or d['2'] == 'a-mason':
                            if d['MATERIAL2']:
                                try:
                                    d['pool2'] = material_dict[d['MATERIAL2']]
                                except:
                                    d['pool2'] = d['pool']
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
                'PROPERTY': False, 'animation': False, 'RIG': False,}#default values
                flag = 'ent'
                d['ent'] = '3df'
                x += 1

            elif value == 'INSERT':#start block
                d = {'ID': '', '41': 1, '42': 1, '43': 1, '50': 0, '210': 0, '220': 0,
                 '230': 1,'repeat': False, 'TYPE': '','NAME': '', 'RIG': False,
                 'animation': False, 'PROPERTY': False, 'PART': '',}#default values
                flag = 'ent'
                d['ent'] = 'insert'
                x += 1

            elif value == 'LINE':#start line
                d = {'ID': '', '30': 0, '31': 0, '39': 0, '41': 1, '42': 1, '43': 1,
                '50': 0, '210': 0, '220': 0, '230': 1, 'RIG': False,
                'PROPERTY': False, 'animation': False, 'repeat': False,
                'PART': '', 'TILING': 0, 'SKIRTING': 0}
                flag = 'ent'
                d['ent'] = 'line'
                x += 1

            elif value == 'LWPOLYLINE':#start polyline
                #default values
                d = {'ID': '', '38': 0,  '39': 0, '41': 1, '42': 1,
                '43': 1, '50': 0, '70': False, '210': 0, '220': 0, '230': 1,
                'vx': [], 'vy': [], 'PROPERTY': False, 'RIG': False,
                'animation': False, 'repeat': False,
                'PART': '', 'TILING': 0, 'SKIRTING': 0}
                flag = 'ent'
                d['ent'] = 'poly'
                x += 1

    return collection

def store_entity_values(d, key, value):
    if key == '2':#block name
        d[key] =  html.escape(value, quote=True)
    if key == '8':#layer name
        d['layer'] = d[key] =  html.escape(value, quote=True)
    elif key == '10':#X position
        if d['ent'] == 'poly':
            d['vx'].append(float(value))
        else:
            d[key] = float(value)
    elif key == '20':#mirror Y position
        if d['ent'] == 'poly':
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
        if d['ent'] == 'poly':
            d['10'] = d['vx'][0]
        d['P_x'] = d['10']
    elif key == '220':#Y of OCS unitary vector
        d['Az_2'] = float(value)
        if d['ent'] == 'poly':
            d['20'] = d['vy'][0]
        d['P_y'] = -d['20']#reset original value
    elif key == '230':#Z of OCS unitary vector
        d['Az_3'] = float(value)
        if d['ent'] == 'poly':
            d['30'] = d.get('38', 0)
            d['50'] = 0
        d['P_z'] = d['30']
        d = arbitrary_axis_algorithm(d)

    return d

def arbitrary_axis_algorithm(d):
    #see if OCS z vector is close to world Z axis
    if fabs(d['Az_1']) < (1/64) and fabs(d['Az_2']) < (1/64):
        W = ('Y', 0, 1, 0)
    else:
        W = ('Z', 0, 0, 1)
    #cross product for OCS x arbitrary vector, normalized
    Ax_1 = W[2]*d['Az_3']-W[3]*d['Az_2']
    Ax_2 = W[3]*d['Az_1']-W[1]*d['Az_3']
    Ax_3 = W[1]*d['Az_2']-W[2]*d['Az_1']
    Norm = sqrt(pow(Ax_1, 2)+pow(Ax_2, 2)+pow(Ax_3, 2))
    Ax_1 = Ax_1/Norm
    Ax_2 = Ax_2/Norm
    Ax_3 = Ax_3/Norm
    #cross product for OCS y arbitrary vector, normalized
    Ay_1 = d['Az_2']*Ax_3-d['Az_3']*Ax_2
    Ay_2 = d['Az_3']*Ax_1-d['Az_1']*Ax_3
    Ay_3 = d['Az_1']*Ax_2-d['Az_2']*Ax_1
    Norm = sqrt(pow(Ay_1, 2)+pow(Ay_2, 2)+pow(Ay_3, 2))
    Ay_1 = Ay_1/Norm
    Ay_2 = Ay_2/Norm
    Ay_3 = Ay_3/Norm
    #insertion world coordinates from OCS
    d['10'] = d['P_x']*Ax_1+d['P_y']*Ay_1+d['P_z']*d['Az_1']
    d['20'] = d['P_x']*Ax_2+d['P_y']*Ay_2+d['P_z']*d['Az_2']
    d['30'] = d['P_x']*Ax_3+d['P_y']*Ay_3+d['P_z']*d['Az_3']

    #OCS X vector translated into WCS
    Ax_1 = ((d['P_x']+cos(radians(d['50'])))*Ax_1+(d['P_y']+sin(radians(d['50'])))*Ay_1+d['P_z']*d['Az_1'])-d['10']
    Ax_2 = ((d['P_x']+cos(radians(d['50'])))*Ax_2+(d['P_y']+sin(radians(d['50'])))*Ay_2+d['P_z']*d['Az_2'])-d['20']
    Ax_3 = ((d['P_x']+cos(radians(d['50'])))*Ax_3+(d['P_y']+sin(radians(d['50'])))*Ay_3+d['P_z']*d['Az_3'])-d['30']
    #cross product for OCS y vector, normalized
    Ay_1 = d['Az_2']*Ax_3-d['Az_3']*Ax_2
    Ay_2 = d['Az_3']*Ax_1-d['Az_1']*Ax_3
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
            roll = atan2(-Ax_3, d['Az_3'])
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

    Has helper functions that calculates the bounding boxes. Window inherits
    wall materials. Returns modified entity collection.
    """
    collection2 = collection.copy()
    for x, d in collection.items():
        if d['2'] == 'a-door' or d['2'] == 'a-window':
            collection[x] = d
            for x2, d2 in collection2.items():
                if d2['2'] == 'a-wall':
                    flag = 0
                    if fabs(d['210']) - fabs(d2['210'])<1:
                        flag += 1
                    if fabs(d['220']) - fabs(d2['220'])<1:
                        flag += 1
                    if fabs(d['50'] - d2['50'])<1:
                        flag += 1
                    elif fabs(d['50'] - 180 - d2['50'])<1:
                        flag += 1
                    elif fabs(d['50'] + 180 - d2['50'])<1:
                        flag += 1
                    if flag == 3:
                        d2 = opening_bounding_box(d, d2)

                    if d2['2'] == 'a-openwall':#success!
                        collection[x2] = d2
                        if d['2'] == 'a-window':
                            d['MATERIAL'] = d2['MATERIAL']
                            d['pool'] = d2['pool']
                            d['MATERIAL2'] = d2['MATERIAL2']
                            d['pool2'] = d2['pool2']
                            d['TILING'] = d2['TILING']
                            d['SKIRTING'] = d2['SKIRTING']
                            d['TILING2'] = d2['TILING2']
                            d['SKIRTING2'] = d2['SKIRTING2']
                            collection[x] = d

    return collection

def opening_bounding_box(d, d2):
    """Cheks if door bounding box is inside wall bounding box.

    Works if insertion points are on the same plane, even if tilted. Returns
    modified wall info.
    """
    sx = sin(radians(-d['210']))
    cx = cos(radians(-d['210']))
    sy = sin(radians(-d['220']))
    cy = cos(radians(-d['220']))
    sz = sin(radians(-d['50']))
    cz = cos(radians(-d['50']))
    dx = d['41']/2
    dy = -d['42']/2
    dz = 0
    #Center of door base
    xgd = d['10'] + (cy*cz-sx*sy*sz)*dx + (-cx*sz)*dy +  (cz*sy+cy*sx*sz)*dz
    ygd = d['20'] + (cz*sx*sy+cy*sz)*dx +  (cx*cz)*dy + (-cy*cz*sx+sy*sz)*dz
    zgd = d['30'] +         (-cx*sy)*dx +     (sx)*dy +           (cx*cy)*dz

    sx = sin(radians(-d2['210']))
    cx = cos(radians(-d2['210']))
    sy = sin(radians(-d2['220']))
    cy = cos(radians(-d2['220']))
    sz = sin(radians(-d2['50']))
    cz = cos(radians(-d2['50']))
    dx = d2['41']/2
    dy = -d2['42']/2
    dz = 0
    #Center of wall base
    xgw = d2['10'] + (cy*cz-sx*sy*sz)*dx + (-cx*sz)*dy +  (cz*sy+cy*sx*sz)*dz
    ygw = d2['20'] + (cz*sx*sy+cy*sz)*dx +  (cx*cz)*dy + (-cy*cz*sx+sy*sz)*dz
    zgw = d2['30'] +         (-cx*sy)*dx +     (sx)*dy +           (cx*cy)*dz

    #translated door coordinates
    sx = sin(radians(d2['210']))
    cx = cos(radians(d2['210']))
    sy = sin(radians(d2['220']))
    cy = cos(radians(d2['220']))
    sz = sin(radians(d2['50']))
    cz = cos(radians(d2['50']))
    dx = xgd - xgw
    dy = ygd - ygw
    dz = zgd - zgw

    #flattened door coordinates YXZ euler angles
    xd = (cy*cz+sx*sy*sz)*dx + (cz*sx*sy-cy*sz)*dy + (cx*sy)*dz
    yd =          (cx*sz)*dx +          (cx*cz)*dy +   (-sx)*dz
    zd = (cy*sx*sz-cz*sy)*dx + (cy*cz*sx+sy*sz)*dy + (cx*cy)*dz

    flag = True
    #conditions of inclusion
    if fabs(zd)>0.01:
        flag = False
    if fabs(d2['41']/2) - fabs(xd) - fabs(d['41']/2) < -0.01:
        flag = False
    if fabs(d2['42']/2) - fabs(yd) - fabs(d['42']/2) < -0.01:
        flag = False

    if flag:
        d2['door'] = d['num']
        d2['2'] = 'a-openwall'
        if d['43']>d2['43']:
            d2['door_height'] = d2['43']
        else:
            d2['door_height'] = d['43']
        if d2['41']>0:
            d2['door_off_1'] = d2['41']/2 + xd - fabs(d['41']/2)
            d2['door_off_2'] = d2['41']/2 + xd + fabs(d['41']/2)
        else:
            d2['door_off_1'] = -fabs(d2['41']/2) + xd + fabs(d['41']/2)
            d2['door_off_2'] = -fabs(d2['41']/2) + xd - fabs(d['41']/2)

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
                            d2['PART'] = d['PART']
                            d2['MATERIAL'] = d['MATERIAL']
                            d2['pool'] = d['pool']
                            d2['TILING'] = d['TILING']
                            d2['SKIRTING'] = d['SKIRTING']
                            d2['MATERIAL2'] = d['MATERIAL2']
                            d2['pool2'] = d['pool2']
                            d2['TILING2'] = d['TILING2']
                            d2['SKIRTING2'] = d['SKIRTING2']

                        elif d['2'] == 'a-animation':
                            d2['animation'] = True
                            if d['PROPERTY'] == 'stalker':
                                d2['animation'] = False
                            elif d['PROPERTY'] == 'look-at':
                                d2['animation'] = False
                            elif d['PROPERTY'] == 'checkpoint':
                                d2['animation'] = False
                            elif d['PROPERTY'] == 'event':
                                d2['animation'] = False
                            d2['PROPERTY'] = d['PROPERTY']
                            d2['FROM'] = d['FROM']
                            d2['TO'] = d['TO']
                            d2['START_EVENTS'] = d['START_EVENTS']
                            d2['DIRECTION'] = d['DIRECTION']
                            d2['LOOP'] = d['LOOP']
                            d2['DURATION'] = d['DURATION']
                            d2['TARGET'] = d['TARGET']
                            d2['TEXT'] = d['TEXT']
                            d2['LINK'] = d['LINK']
                            if d['PROPERTY'] == 'stalker':
                                d2['RIG'] = False
                            elif d['PROPERTY'] == 'look-at':
                                d2['RIG'] = False
                            elif d['PROPERTY'] == 'checkpoint':
                                d2['RIG'] = False
                            elif d['PROPERTY'] == 'event':
                                d2['RIG'] = False
                            else:
                                d2['RIG'] = eval(d['RIG'])

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
            entities_dict[x] = entities.make_camera(page, d, mode)
        elif d['2'] == 'a-box':
            entities_dict[x] = entities.make_box(page, d)
        elif d['2'] == 'a-cone' or d['2'] == 'a-cylinder' or d['2'] == 'a-circle' or d['2'] == 'a-sphere':
            entities_dict[x] = entities.make_circular(page, d)
        elif d['2'] == 'a-curvedimage':
            entities_dict[x] = entities.make_curvedimage(page, d)
        elif d['2'] == 'a-plane':
            entities_dict[x] = entities.make_plane(page, d)
        elif d['2'] == 'a-triangle':
            entities_dict[x] = entities.make_triangle(page, d)
        elif d['2'] == 'a-line':
            entities_dict[x] = entities.make_line(page, d)
        elif d['2'] == 'a-poly':
            entities_dict[x] = entities.make_poly(page, d)
        elif d['2'] == 'a-light':
            entities_dict[x] = entities.make_light(page, d)
        elif d['2'] == 'a-link':
            entities_dict[x] = entities.make_link(page, d)
        elif d['2'] == 'a-text':
            entities_dict[x] = entities.make_text(page, d)
        elif d['2'] == 'a-wall':
            entities_dict[x] = entities.make_bim_block(page, d)
        elif d['2'] == 'a-door':
            entities_dict[x] = entities.make_bim_block(page, d)
        elif d['2'] == 'a-window':
            entities_dict[x] = entities.make_bim_block(page, d)
        elif d['2'] == 'a-slab':
            entities_dict[x] = entities.make_bim_block(page, d)
        elif d['2'] == 'a-openwall':
            entities_dict[x] = entities.make_bim_block(page, d)
        elif d['2'] == 'a-stair':
            entities_dict[x] = entities.make_bim_block(page, d)
        elif d['2'] == 'a-block':
            d['NAME'] = d.get('NAME', 't01')
            entities_dict[x] = entities.make_block(page, d)

        elif d['2'] == 'a-animation' or d['2'] == 'a-mason':
            pass

    if no_camera:
        x += 1
        d = {
        '10': 0, '20': 0, '30': 0, '210': 0, '50': 0, '220': 0,  '43': 1,
        'LIGHT-INT': 1,
        }
        entities_dict[x] = entities.make_camera(page, d, mode)

    return entities_dict

def make_survey(collection, layer_dict):
    entities_dict = {}
    for x, d in collection.items():
        if layer_dict[d['layer']]:
            pass
        else:
            if d['2'] == 'a-wall':
                d['ide'] = 'wall'
                entities_dict[x] = entities.survey_wall(d)
            elif d['2'] == 'a-slab':
                d['ide'] = 'slab'
                entities_dict[x] = entities.survey_slab(d)
            elif d['2'] == 'a-door':
                d['ide'] = 'door'
                entities_dict[x] = entities.survey_door(d)
            elif d['2'] == 'a-window':
                d['ide'] = 'window'
                entities_dict[x] = entities.survey_window(d)
            elif d['2'] == 'a-openwall':
                entities_dict[x] = entities.survey_openwall(d)
    return entities_dict

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
