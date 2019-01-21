import os
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
                if value == 'TYPE':
                    if attr_value == 'obj-mtl' or attr_value == 'obj-stalker':
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
    file for 3Dfaces, lines and blocks. Assigns values to each entity, including
    geometric and appearance values plus functional attributes. Returns a
    nested dictionary.
    """
    path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', page.dxf_file.filename)
    dxf_f = open(path_to_dxf, encoding = 'utf-8')

    collection = {}
    layer_color = {}
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
            layer_color[layer_name] = cad2hex(dxf_f.readline().strip())

        elif value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return collection

    while value !='ENDSEC':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value=='EOF' or key=='':#security to avoid loops if file is corrupted
            return collection

        if flag == 'face':#stores values for 3D faces
            if key == '8':#layer name
                data[key] = value
            elif key == '10' or key == '11' or key == '12' or key == '13':#X position
                data[key] = float(value)
            elif key == '20' or key == '21' or key == '22' or key == '23':#mirror Y position
                data[key] = -float(value)
            elif key == '30' or key == '31' or key == '32' or key == '33':#Z position
                data[key] = float(value)

        elif flag == 'line':#stores values for lines
            if key == '8':#layer name
                data[key] = value
            elif key == '10' or key == '11':#X position
                data[key] = float(value)
            elif key == '20' or key == '21':#mirror Y position
                data[key] = -float(value)
            elif key == '30' or key == '31':#Z position
                data[key] = float(value)
            elif key == '39':#thickness
                data[key] = float(value)
            elif key == '62':#color
                data['color'] = cad2hex(value)

        elif flag == 'block':#stores values for blocks
            if key == '2':#block name
                data[key] = value
            if key == '8':#layer name
                data[key] = value
                data['layer'] = value#sometimes key 8 is replaced, so I need the original layer value
            elif key == '10' or key == '30':#X Z position
                data[key] = float(value)
            elif key == '20':#Y position, mirrored
                data[key] = -float(value)
            elif key == '50':#Z rotation
                data[key] = float(value)
            elif key == '41' or key == '42' or key == '43':#scale values
                data[key] = float(value)
            elif key == '210':#X of OCS unitary vector
                Az_1 = float(value)
                P_x = data['10']
            elif key == '220':#Y of OCS unitary vector
                Az_2 = float(value)
                P_y = -data['20']#reset original value
            elif key == '230':#Z of OCS unitary vector
                Az_3 = float(value)
                P_z = data['30']
                #arbitrary axis algorithm
                #see if OCS z vector is close to world Z axis
                if fabs(Az_1) < (1/64) and fabs(Az_2) < (1/64):
                    W = ('Y', 0, 1, 0)
                else:
                    W = ('Z', 0, 0, 1)
                #cross product for OCS x arbitrary vector, normalized
                Ax_1 = W[2]*Az_3-W[3]*Az_2
                Ax_2 = W[3]*Az_1-W[1]*Az_3
                Ax_3 = W[1]*Az_2-W[2]*Az_1
                Norm = sqrt(pow(Ax_1, 2)+pow(Ax_2, 2)+pow(Ax_3, 2))
                Ax_1 = Ax_1/Norm
                Ax_2 = Ax_2/Norm
                Ax_3 = Ax_3/Norm
                #cross product for OCS y arbitrary vector, normalized
                Ay_1 = Az_2*Ax_3-Az_3*Ax_2
                Ay_2 = Az_3*Ax_1-Az_1*Ax_3
                Ay_3 = Az_1*Ax_2-Az_2*Ax_1
                Norm = sqrt(pow(Ay_1, 2)+pow(Ay_2, 2)+pow(Ay_3, 2))
                Ay_1 = Ay_1/Norm
                Ay_2 = Ay_2/Norm
                Ay_3 = Ay_3/Norm
                #insertion world coordinates from OCS
                data['10'] = P_x*Ax_1+P_y*Ay_1+P_z*Az_1
                data['20'] = P_x*Ax_2+P_y*Ay_2+P_z*Az_2
                data['30'] = P_x*Ax_3+P_y*Ay_3+P_z*Az_3
                #OCS X vector translated into WCS
                Ax_1 = ((P_x+cos(radians(data['50'])))*Ax_1+(P_y+sin(radians(data['50'])))*Ay_1+P_z*Az_1)-data['10']
                Ax_2 = ((P_x+cos(radians(data['50'])))*Ax_2+(P_y+sin(radians(data['50'])))*Ay_2+P_z*Az_2)-data['20']
                Ax_3 = ((P_x+cos(radians(data['50'])))*Ax_3+(P_y+sin(radians(data['50'])))*Ay_3+P_z*Az_3)-data['30']
                #cross product for OCS y vector, normalized
                Ay_1 = Az_2*Ax_3-Az_3*Ax_2
                Ay_2 = Az_3*Ax_1-Az_1*Ax_3
                Ay_3 = Az_1*Ax_2-Az_2*Ax_1
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
                        yaw = -atan2(Az_1, Ax_1)
                        roll = 0
                else:
                    pitch = pi/2
                    yaw = atan2(Az_1, Ax_1)
                    roll = 0

                #Y position, mirrored
                data['20'] = -data['20']
                #rotations from radians to degrees
                data['210'] = degrees(pitch)
                data['50'] = degrees(yaw)
                data['220'] = -degrees(roll)

        elif flag == 'attrib':#stores values for attributes within block
            if key == '1':#attribute value
                attr_value = value
            elif key == '2':#attribute key
                data[value] = attr_value
                flag = 'block'#restore block modality

        if key == '0':
            invisible = False#by default layer is visible

            if flag == 'face':#close 3D face
                data['2'] = '3dface'
                #is material set in layer?
                layer = layer_dict[data['8']]
                invisible = layer[1]
                data['wireframe'] = layer[2]
                data['wf_width'] = layer[3]
                if invisible:
                    flag = False
                else:
                    layer_material = layer[0]
                    data['color'] = layer_color[data['8']]
                    data['8'] = 'default'
                    if layer_material != 'default':
                        component_pool = material_dict[layer_material]
                        if component_pool:
                            component = component_pool[0]
                            data['color'] = component[1]
                            data['8'] = layer_material + '-' + component[0]

                    data['num'] = x
                    collection[x] = data

                    if data['12']!=data['13'] or data['22']!=data['23'] or data['32']!=data['33']:
                        data2 = data.copy()
                        data2['11'] = data['12']
                        data2['21'] = data['22']
                        data2['31'] = data['32']
                        data2['12'] = data['13']
                        data2['22'] = data['23']
                        data2['32'] = data['33']
                        x += 1
                        data2['num'] = x
                        collection[x] = data2

                    flag = False

            elif flag == 'line':#close line
                if data['39']:#if thickness transform in a-plane, works if on X-Y plane
                    dx = data['10']-data['11']
                    dy = data['20']-data['21']
                    data['2'] = 'a-plane'
                    data['43'] = data['39']
                    data['41'] = sqrt(pow(dx, 2) + pow(dy, 2))
                    data['50'] = 180-degrees(atan2(dy, dx))
                    data['repeat'] = data['animation'] = data['checkpoint'] = False
                    data['MATERIAL'] = ''
                    data['210'] = data['220'] = 0
                    layer = layer_dict[data['8']]
                    invisible = layer[1]
                    data['wireframe'] = layer[2]
                    data['wf_width'] = layer[3]
                    if invisible:
                        flag = False
                    else:
                        layer_material = layer[0]
                        data['color'] = layer_color[data['8']]
                        data['8'] = 'default'
                        if layer_material != 'default':
                            component_pool = material_dict[layer_material]
                            if component_pool:
                                component = component_pool[0]
                                data['color'] = component[1]
                                data['8'] = layer_material + '-' + component[0]

                        data['num'] = x
                        collection[x] = data
                else:
                    data['2'] = 'line'
                    #is material set in layer?
                    layer = layer_dict[data['8']]
                    invisible = layer[1]
                    if invisible:
                        flag = False
                    else:
                        if data['color']:
                            pass
                        else:
                            layer_material = layer[0]
                            data['color'] = layer_color[data['8']]

                        data['num'] = x
                        collection[x] = data

                        flag = False

            elif value == 'ATTRIB':#start attribute within block
                attr_value = ''
                flag = 'attrib'

            elif flag == 'block':#close block
                #is material set in layer?
                layer = layer_dict[data['8']]
                invisible = layer[1]
                data['wireframe'] = layer[2]
                data['wf_width'] = layer[3]
                if invisible:
                    flag = False
                else:
                    layer_material = layer[0]
                    data['color'] = layer_color[data['8']]
                    data['8'] = 'default'
                    if layer_material != 'default':
                        component_pool = material_dict[layer_material]
                        if component_pool:
                            component = component_pool[0]
                            data['color'] = component[1]
                            data['8'] = layer_material + '-' + component[0]
                            data['repeat'] = component[2]
                    try:
                        if data['MATERIAL']:
                            component_pool = material_dict[data['MATERIAL']]
                            if component_pool:
                                component = component_pool[0]
                                data['color'] = component[1]
                                data['8'] = data['MATERIAL'] + '-' + component[0]
                                data['repeat'] = component[2]
                                data['pool'] = component_pool
                    except:
                        pass
                    try:
                        if data['2'] == 'a-wall' and data['MATERIAL2']:
                            data['pool2'] = material_dict[data['MATERIAL2']]
                    except:
                        pass

                    data['num'] = x
                    collection[x] = data

                    flag = False

            if value == '3DFACE':#start 3D face
                data = {'wireframe': False, 'wf_width': 2}#default values
                flag = 'face'
                x += 1

            elif value == 'INSERT':#start block
                data = {'41': 1, '42': 1, '43': 1, '50': 0, '210': 0, '220': 0,
                 '230': 1,'repeat': False, 'TYPE': '', 'MATERIAL': '',
                 'animation': False, 'checkpoint': False, 'wireframe': False, 'wf_width': 2}#default values
                flag = 'block'
                x += 1

            elif value == 'LINE':#start line
                data = {'color': '', '39': 0,}#default values
                flag = 'line'
                x += 1

    return collection

def reference_openings(collection):
    """Compares each door entity with each wall.

    Has two helper functions, straight case and tilted case, but latter has not
    been implemented yet. Returns modified entity collection.
    """
    collection2 = collection.copy()
    for x, data in collection.items():
        if data['2'] == 'a-door':
            collection[x] = data
            for x2, data2 in collection2.items():
                if data2['2'] == 'a-wall':
                    if data['210']==0 and data['220']==0 and data2['210']==0 and data2['220']==0:
                        data2 = door_straight_case(data, data2)
                    else:
                        data2 = door_tilted_case(data, data2)
                    collection[x2] = data2

    return collection

def door_straight_case(data, data2):
    """Cheks if door bounding box is inside wall bounding box.

    Works if both blocks are not rotated on X and Y axis and if insertion point
    is on the same plane. Returns modified wall data.
    """
    if data['30']==data2['30'] and data['43']>0 and data2['43']>0:
        rotd = round(data['50'], 0)
        rotw = round(data2['50'], 0)
        if rotd==rotw-180 or rotd-180==rotw:
            backwards = -1
        else:
            backwards = 1
        if rotd == rotw or backwards == -1:
            #translation
            xt = data['10']-data2['10']
            zt = data['20']-data2['20']
            #rotation
            alfa = radians(data2['50'])
            xd = round(xt*cos(alfa)-zt*sin(alfa), 4)
            zd = round(xt*sin(alfa)+zt*cos(alfa), 4)
            xde = xd + round(data['41'], 4)*backwards
            zde = zd + round(data['42'], 4)
            #wall bounding box
            if data2['41'] > 0:
                xmaxw = round(data2['41'], 4)
                xminw = 0
            else:
                xmaxw = 0
                xminw = round(data2['41'], 4)
            if data2['42'] > 0:
                zmaxw = 0
                zminw = -round(data2['42'], 4)
            else:
                zmaxw = -round(data2['42'], 4)
                zminw = 0
            #door bounding box
            if xde > xd:
                xmaxd = xde
                xmind = xd
            else:
                xmaxd = xd
                xmind = xde
            if zde > zd:
                zmaxd = zde * ( - backwards)
                zmind = zd * ( - backwards)
            else:
                zmaxd = zd * ( - backwards)
                zmind = zde * ( - backwards)
            #door inclusion
            if xmaxw >= xmaxd and xminw <= xmind and zmaxw >= zmaxd and zminw <= zmind:
                data2['door'] = data['num']
                data2['2'] = 'a-openwall'
                if data['43']>data2['43']:
                    data2['door_height'] = data2['43']
                else:
                    data2['door_height'] = data['43']
                if data2['41']>0:
                    data2['door_off_1'] = xmind
                    data2['door_off_2'] = xmaxd
                else:
                    data2['door_off_1'] = xmaxd - xmaxw
                    data2['door_off_2'] = xmind - xmaxw

    return data2

def door_tilted_case(data, data2):
    """Not working yet.
    """
    d210 = round(data['210']*fabs(data['41'])/data['41'], 4)
    d220 = round(data['220']*fabs(data['42'])/data['42'], 4)
    d50 = round(data['50']*fabs(data['43'])/data['43'], 4)
    w210 = round(data2['210']*fabs(data2['41'])/data2['41'], 4)
    w220 = round(data2['220']*fabs(data2['42'])/data2['42'], 4)
    w50 = round(data2['50']*fabs(data2['43'])/data2['43'], 4)
    return data2

def reference_animations(collection):
    """Assigns animations and checkpoints.

    Controls if animation / checkpoint block shares insertion point with other
    blocks. Animation / checkpoint attributes will be appended to selected
    block. Returns nested dictionary.
    """
    collection2 = collection.copy()
    for x, data in collection.items():
        if data['2'] == 'a-animation' or data['2'] == 'checkpoint':
            for x2, data2 in collection2.items():
                d = data2['2']
                if x == x2 or d == 'a-wall' or d == 'a-openwall' or d == 'a-door' or d == 'a-slab':
                    pass
                else:
                    dx = fabs(data['10']-data2['10'])
                    dy = fabs(data['20']-data2['20'])
                    dz = fabs(data['30']-data2['30'])
                    if dx < 0.01 and dy < 0.01 and dz < 0.01:
                        if data['2'] == 'checkpoint':
                            data2['checkpoint'] = True
                        elif data['2'] == 'a-animation':
                            data2['animation'] = True
                            data2['ATTRIBUTE'] = data['ATTRIBUTE']
                            data2['FROM'] = data['FROM']
                            data2['TO'] = data['TO']
                            data2['BEGIN'] = data['BEGIN']
                            data2['DIRECTION'] = data['DIRECTION']
                            data2['REPEAT'] = data['REPEAT']
                            data2['DURATION'] = data['DURATION']
                        collection[x2] = data2
    return collection

def make_html(page, collection, mode):
    entities_dict = {}
    if mode == 'ar':
        no_camera = False
    else:
        no_camera = True
    for x, data in collection.items():

        if data['2'] == '3dface':
            entities_dict[x] = make_triangle(page, data)

        elif data['2'] == 'line':
            entities_dict[x] = make_line(data)

        elif data['2'] == 'a-box':
            entities_dict[x] = make_box(page, data)

        elif data['2'] == 'a-curvedimage':
            entities_dict[x] = make_curvedimage(page, data)

        elif data['2'] == 'a-cone' or data['2'] == 'a-cylinder' or data['2'] == 'a-circle' or data['2'] == 'a-sphere':
            entities_dict[x] = make_circular(page, data)

        elif data['2'] == 'a-plane' or data['2'] == 'look-at':
            entities_dict[x] = make_plane(page, data)

        elif data['2'] == 'a-light':
            entities_dict[x] = make_light(page, data)

        elif data['2'] == 'a-text':
            entities_dict[x] = make_text(data)

        elif data['2'] == 'a-link':
            entities_dict[x] = make_link(page, data)

        elif data['2'] == 'a-camera' and no_camera:
            no_camera = False
            entities_dict[x] = make_camera(page, data, mode)

        elif data['2'] == 'a-animation' or data['2'] == 'checkpoint':
            pass

        else:
            entities_dict[x] = make_block(page, data)

    if no_camera:
        x += 1
        data = {
        '10': 0, '20': 0, '30': 0, '210': 0, '50': 0, '220': 0,  '43': 1,
        'LIGHT-INT': 1,
        }
        entities_dict[x] = make_camera(page, data, mode)

    return entities_dict

def make_triangle(page, data):
    outstr = f'<a-triangle id="triangle-{data["num"]}" \n'
    if page.shadows:
        outstr += 'shadow="receive: true; cast: true" \n'
    outstr += f'geometry="vertexA:{data["10"]} {data["30"]} {data["20"]}; \n'
    outstr += f'vertexB:{data["11"]} {data["31"]} {data["21"]}; \n'
    outstr += f'vertexC:{data["12"]} {data["32"]} {data["22"]}" \n'
    if data['wireframe']:
        outstr += f'material="wireframe: true; wireframe-linewidth: {data["wf_width"]}; color: {data["color"]}; '
    else:
        outstr += f'material="src: #{data["8"]}; color: {data["color"]}; '
        if page.double_face:
            outstr += 'side: double; '
    outstr += '">\n</a-triangle> \n'
    return outstr

def make_line(data):
    outstr = f'<a-entity id="line-{data["num"]}" \n'
    outstr += f'line="start:{data["10"]} {data["30"]} {data["20"]}; \n'
    outstr += f'end:{data["11"]} {data["31"]} {data["21"]}; \n'
    outstr += f'color: {data["color"]};"> \n'
    outstr += '</a-entity> \n'
    return outstr

def make_box(page, data):
    outstr = start_entity_wrapper(page, data)
    outstr += '> \n'
    outstr += start_entity(data)
    outstr += entity_material(data)
    if data['animation']:
        outstr += is_animation(data)
    outstr += close_entity(data)
    return outstr

def make_circular(page, data):
    outstr = start_entity_wrapper(page, data)
    outstr += '> \n'
    outstr += start_entity(data)
    outstr += entity_geometry(data)
    outstr += entity_material(data)
    if data['animation']:
        outstr += is_animation(data)
    outstr += close_entity(data)
    return outstr

def make_curvedimage(page, data):
    outstr = start_entity_wrapper(page, data)
    outstr += '> \n'
    outstr += start_entity(data)
    try:
        if data['THETA-LENGTH']!='270':
            outstr += f'theta-length="{data["THETA-LENGTH"]}" '
        if data['THETA-START']!='0':
            outstr += f'theta-start="{data["THETA-START"]}" '
    except KeyError:
        pass
    outstr += f'src="#{data["8"]}">\n'
    if data['animation']:
        outstr += is_animation(data)
    outstr += close_entity(data)
    return outstr

def make_plane(page, data):
    outstr = start_entity_wrapper(page, data)
    outstr += '> \n'
    outstr += f'<a-plane id="{data["2"]}-{data["num"]}" \n'
    if data['2'] == 'look-at':#if it's a look at, it is centered and looks at the camera foot
        outstr += f'position="0 {data["43"]/2} 0" \n'
        outstr += 'look-at="#camera-foot" \n'
    else:#insertion is at corner
        outstr += f'position="{data["41"]/2} {data["43"]/2} 0" \n'
    outstr += f'width="{fabs(data["41"])}" height="{fabs(data["43"])}" \n'
    if data['wireframe']:
        outstr += f'material="wireframe: true; wireframe-linewidth: {data["wf_width"]}; color: {data["color"]}; '
    else:
        outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
        outstr += is_repeat(data["repeat"], data["41"], data["43"])
        if page.double_face:
            outstr += 'side: double; '
    outstr += '">\n'
    if data['animation']:
        outstr += is_animation(data)
    outstr += close_entity(data)
    return outstr

def make_text(data):
    outstr = f'<a-entity id="a-text-{data["num"]}" \n'
    outstr += f'position="{data["10"]} {data["30"]} {data["20"]}" \n'
    outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}"\n'
    outstr += f'text="width: {data["41"]}; align: {data["ALIGN"]}; color: {data["color"]}; '
    outstr += f'value: {data["TEXT"]}; wrap-count: {data["WRAP-COUNT"]}; '
    outstr += '">\n'
    if data['animation']:
        outstr += is_animation(data)
    outstr += '</a-entity>\n'
    return outstr

def make_link(page, data):
    outstr = f'<a-link id="a-link-{data["num"]}" \n'
    outstr += f'position="{data["10"]} {data["30"]} {data["20"]}" \n'
    outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}"\n'
    outstr += f'scale="{data["41"]} {data["43"]} {data["42"]}"\n'
    if data['TREE'] == 'parent':
        target = page.get_parent()
    elif data['TREE'] == 'child':
        target = page.get_first_child()
    elif data['TREE'] == 'previous' or data['tree'] == 'prev':
        target = page.get_prev_sibling()
    else:#we default to next sibling
        target = page.get_next_sibling()
    try:
        if target:
            outstr += f'href="{target.url}"\n'
            outstr += f'title="{data["TITLE"]}" color="{data["color"]}" on="click"\n'
            try:
                eq_image = target.specific.equirectangular_image
                if eq_image:
                    outstr += f'image="{eq_image.file.url}"'
            except:
                outstr += 'image="#default-sky"'
            outstr += '>\n'
            if data['animation']:
                outstr += is_animation(data)
            outstr += '</a-link>\n'
            return outstr
        else:
            return ''
    except:
        return ''

def make_light(page, data):
    outstr = start_entity_wrapper(page, data)
    outstr += '> \n'
    outstr += f'<a-entity id="{data["2"]}-{data["num"]}" \n'

    try:
        outstr += f'light="type: {data["TYPE"]}; color: {data["color"]}; intensity: {data["INTENSITY"]}; '
        if data['TYPE'] != 'ambient':
            if page.shadows:
                outstr += 'castShadow: true; '
        if data['TYPE'] == 'point' or data['TYPE'] == 'spot':
            outstr += f'decay: {data["DECAY"]}; distance: {data["DISTANCE"]}; '
        if data['TYPE'] == 'spot':
            outstr += f'angle: {data["ANGLE"]}; penumbra: {data["PENUMBRA"]}; '
        if data['TYPE'] == 'directional':
            outstr += f'shadowCameraBottom: {-5*fabs(data["42"])}; \n'
            outstr += f'shadowCameraLeft: {-5*fabs(data["41"])}; \n'
            outstr += f'shadowCameraTop: {5*fabs(data["42"])}; \n'
            outstr += f'shadowCameraRight: {5*fabs(data["41"])}; \n'
        if data['TYPE'] == 'directional' or data['TYPE'] == 'spot':
            outstr += make_light_target(data)
        else:
            outstr += '">\n'
    except KeyError:#default if no light type is set
        outstr += 'light="type: point; intensity: 0.75; distance: 50; decay: 2; '
        if page.shadows:
            outstr += 'castShadow: true;'
        outstr += '">\n'

    if data['animation']:
        outstr += is_animation(data)
    outstr += '</a-entity></a-entity>\n'#close light entity
    return outstr

def make_light_target(data):
    outstr = f'target: #light-{data["num"]}-target;"> \n'
    outstr += f'<a-entity id="light-{data["num"]}-target" position="0 -1 0"> </a-entity> \n'
    return outstr

def make_block(page, data):
    outstr = start_entity_wrapper(page, data)
    try:
        if data['TYPE'] == 't01':
            outstr += '> \n'
            outstr += animation_wrapper(data)
            outstr += blocks.make_table_01(data)

        elif data['TYPE'] == 'stalker' or data['TYPE'] == 'obj-stalker':
            outstr += 'look-at="#camera-foot"> \n'
            outstr += blocks.make_stalker(page, data)

        elif data['TYPE'] == 'obj-mtl':
            outstr += '> \n'
            outstr += animation_wrapper(data)
            outstr += blocks.make_object(data)

        elif data['TYPE'] == 'tree':
            outstr += '> \n'
            outstr += animation_wrapper(data)
            outstr += blocks.make_tree(data)

        elif data['2'] == 'a-door':
            outstr += '> \n'
            outstr += blocks.make_door(data)

        elif data['2'] == 'a-slab':
            outstr += '> \n'
            outstr += blocks.make_slab(data)

        elif data['2'] == 'a-wall':
            outstr += '> \n'
            outstr += blocks.make_wall(data)

        elif data['2'] == 'a-openwall':
            outstr += '> \n'
            #make left wall
            data2 = data.copy()
            data2['41'] = data2['door_off_1']
            data2['2'] = 'a-openwall-left'
            outstr += blocks.make_wall(data2)
            #make part above door
            data2 = data.copy()
            data2['41'] = data2['door_off_2'] - data2['door_off_1']
            data2['2'] = 'a-openwall-above'
            outstr += f'<a-entity id="{data2["2"]}-{data2["num"]}-ent" \n'
            outstr += f'position="{data2["door_off_1"]} {data2["door_height"]} 0"> \n'
            outstr += blocks.make_wall(data2)
            outstr += '</a-entity> \n'
            #make right wall
            data2 = data.copy()
            data2['41'] = data2['41'] - data2['door_off_2']
            data2['2'] = 'a-openwall-right'
            outstr += f'<a-entity id="{data2["2"]}-{data2["num"]}-ent" \n'
            outstr += f'position="{data2["door_off_2"]} 0 0"> \n'
            outstr += blocks.make_wall(data2)
            outstr += '</a-entity> \n'

        #other elifs here
    except:
        outstr += '> \n'
        outstr += animation_wrapper(data)
        outstr += blocks.make_table_01(data)

    if data['animation']:
        outstr += is_animation(data)
        outstr += '</a-entity>\n'
    outstr += '</a-entity>\n'
    return outstr

def make_camera(page, data, mode):
    outstr = f'<a-entity id="camera-ent" position="{data["10"]} {data["30"]} {data["20"]}" \n'
    outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}" \n'
    if mode == 'digkom':
        outstr += 'movement-controls="controls: checkpoint" checkpoint-controls="mode: animate"> \n'
        outstr += f'<a-camera id="camera" look-controls="pointerLockEnabled: true" wasd-controls="enabled: false" '
        outstr += f' position="0 {data["43"]*1.6} 0"> \n'
        outstr += '<a-cursor color="black"></a-cursor> \n'
    else:
        outstr += '> \n'
        outstr += f'<a-camera id="camera" wasd-controls="fly: {str(page.fly_camera).lower() }" '
        outstr += f' position="0 {data["43"]*1.6} 0"> \n'
        outstr += '<a-cursor color="#2E3A87"></a-cursor> \n'

    outstr += f'<a-light type="point" distance="10" intensity="{data["LIGHT-INT"]}"></a-light> \n'
    outstr += f'<a-entity position="0 {-data["43"]*1.6} 0" id="camera-foot"></a-entity> \n'
    outstr += '</a-camera></a-entity> \n'
    return outstr

def start_entity_wrapper(page, data):
    outstr = f'<a-entity id="{data["2"]}-{data["num"]}-ent" \n'
    if data['checkpoint']:
        outstr += 'checkpoint \n'
    if page.shadows:
        if data['2'] == 'a-curvedimage':
            outstr += 'shadow="receive: false; cast: false" \n'
        elif data['2'] == 'a-light':
            pass
        else:
            outstr += 'shadow="receive: true; cast: true" \n'
    outstr += f'position="{data["10"]} {data["30"]} {data["20"]}" \n'
    outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}" \n'

    return outstr

def animation_wrapper(data):
    outstr = ''
    if data['animation']:
        outstr += f'<a-entity id="{data["2"]}-{data["num"]}-animation"> \n'
    return outstr

def start_entity(data):
    outstr = f'<{data["2"]} id="{data["2"]}-{data["num"]}" \n'
    if data['2'] == 'a-box':
        outstr += f'position="{data["41"]/2} {data["43"]/2} {-data["42"]/2}" \n'
    elif data['2'] == 'a-circle':
        pass
    elif data['2'] == 'a-sphere':
        outstr += f'position="0 {data["43"]} 0" \n'
    else:
        outstr += f'position="0 {data["43"]/2} 0" \n'
    if data['2'] == 'a-circle':
        outstr += f'radius="{fabs(data["41"])}" \n'
    else:
        outstr += f'scale="{fabs(data["41"])} {fabs(data["43"])} {fabs(data["42"])}" \n'
    if float(data['43']) < 0:
        if data['2'] == 'a-cone' or data['2'] == 'a-cylinder' or data['2'] == 'a-curvedimage' or data['2'] == 'a-sphere':
            outstr += 'rotation="180 0 0">\n'

    return outstr

def entity_geometry(data):
    attr_dict = {
        'a-cone': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-cylinder': ('OPEN-ENDED', 'RADIUS-BOTTOM', 'RADIUS-TOP', 'SEGMENTS-RADIAL', 'THETA-LENGTH', 'THETA-START', ),
        'a-circle': ('SEGMENTS', 'THETA-LENGTH', 'THETA-START', ),
        'a-curvedimage': ('THETA-LENGTH', 'THETA-START', ),
        'a-sphere': ('PHI-LENGTH', 'PHI-START', 'SEGMENTS-HEIGHT', 'SEGMENTS-WIDTH', 'THETA-LENGTH', 'THETA-START', ),
    }
    attributes = attr_dict[data['2']]
    outstr = 'geometry="'
    for attribute in attributes:
        try:
            if data[attribute]:
                outstr += f'{attribute.lower()}: {data[attribute]};'
        except:
            pass

    outstr += '" \n'
    return outstr

def entity_material(data):
    outstr = ''
    if data['wireframe']:
        outstr += f'material="wireframe: true; wireframe-linewidth: {data["wf_width"]}; color: {data["color"]}; '
    else:
        outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
        outstr += is_repeat(data["repeat"], data["41"], data["43"])
    outstr += '">\n'
    return outstr

def close_entity(data):
    outstr = f'</{data["2"]}>\n</a-entity>\n'
    return outstr

def is_repeat(repeat, rx, ry):
    if repeat:
        output = f'; repeat:{fabs(rx)} {fabs(ry)}'
        return output
    else:
        return ';'

def is_animation(data):
    outstr = f'<a-animation attribute="{data["ATTRIBUTE"]}"\n'
    outstr += f'from="{data["FROM"]}"\n'
    outstr += f'to="{data["TO"]}"\n'
    outstr += f'begin="{data["BEGIN"]}"\n'
    outstr += f'direction="{data["DIRECTION"]}"\n'
    outstr += f'repeat="{data["REPEAT"]}"\n'
    outstr += f'dur="{data["DURATION"]}"\n'
    outstr += '></a-animation>\n'
    return outstr

def cad2hex(cad_color):
    cad_color = abs(int(cad_color))
    if cad_color<0 or cad_color>255:
        return 'white'
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
