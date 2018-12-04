import os
from math import radians, sin, cos, asin, degrees, pi, sqrt, pow, fabs, atan2

from django.conf import settings

def get_layer_list(page):
    path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', page.dxf_file.filename)
    dxf_f = open(path_to_dxf, encoding = 'utf-8')

    layer_list = []
    value = 'dummy'

    while value !='ENTITIES':
        key = dxf_f.readline().strip()
        value = dxf_f.readline().strip()
        if value == 'AcDbLayerTableRecord':#dict of layer names and colors
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

def get_entity_material(page):
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

            elif value == 'ATTRIB':#start attribute within block
                attr_value = ''
                flag = 'attrib'

            elif flag == 'block':#close block
                #is material set in layer?
                layer = layer_dict[data['8']]
                invisible = layer[1]
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
                    if data['MATERIAL']:
                        component_pool = material_dict[data['MATERIAL']]
                        if component_pool:
                            component = component_pool[0]
                            data['color'] = component[1]
                            data['8'] = layer_material + '-' + component[0]
                            data['repeat'] = component[2]
                            data['pool'] = component_pool

                    data['num'] = x
                    collection[x] = data

                    flag = False

            if value == '3DFACE':#start 3D face
                data = {}#default values
                flag = 'face'
                x += 1

            elif value == 'INSERT':#start block
                data = {'41': 1, '42': 1, '43': 1, '50': 0, '210': 0, '220': 0,
                 '230': 1,'repeat': False, 'type': '', 'MATERIAL': '', 'animation': False}#default values
                flag = 'block'
                x += 1

    return collection

def make_html(page, collection, material_dict):
    entities_dict = {}
    for x, data in collection.items():
        if data['2'] == '3dface':
            entities_dict[x] = make_triangle(page, x, data)

        elif data['2'] == 'a-box':
            entities_dict[x] = make_box(page, x, data)

    return entities_dict

def make_triangle(page, x, data):
    outstr = f'<a-triangle id="triangle-{x}" \n'
    if page.shadows:
        outstr += 'shadow="receive: true; cast: true" \n'
    outstr += f'geometry="vertexA:{data["10"]} {data["30"]} {data["20"]}; \n'
    outstr += f'vertexB:{data["11"]} {data["31"]} {data["21"]}; \n'
    outstr += f'vertexC:{data["12"]} {data["32"]} {data["22"]}" \n'
    outstr += f'material="src: #{data["8"]}; color: {data["color"]}; '
    if page.double_face:
        outstr += 'side: double; '
    outstr += '">\n</a-triangle> \n'
    return outstr

def make_box(page, x, data):
    outstr = f'<a-entity id="box-{x}-ent" \n'
    if page.shadows:
        outstr += 'shadow="receive: true; cast: true" \n'
    outstr += f'position="{data["10"]} {data["30"]} {data["20"]}" \n'
    outstr += f'rotation="{data["210"]} {data["50"]} {data["220"]}">\n'
    outstr += f'<a-box id="box-{x}" \n'
    outstr += f'position="{data["41"]/2} {data["43"]/2} {-data["42"]/2}" \n'
    outstr += f'scale="{fabs(data["41"])} {fabs(data["43"])} {fabs(data["42"])}" \n'
    outstr += 'geometry="'
    try:
        if data['segments-depth']!='1':
            outstr += f'segments-depth: {data["segments-depth"]};'
        if data['segments-height']!='1':
            outstr += f'segments-height: {data["segments-height"]};'
        if data['segments-width']!='1':
            outstr += f'segments-width: {data["segments-width"]};'
        outstr += '" \n'
    except KeyError:
        outstr += '" \n'
    outstr += f'material="src: #{data["8"]}; color: {data["color"]}'
    outstr += is_repeat(data["repeat"], data["41"], data["43"])
    outstr += '">\n'
    if data['animation']:
        outstr += is_animation(data)
    outstr += '</a-box>\n</a-entity>\n'
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
    outstr += f'duration="{data["DURATION"]}"\n'
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
