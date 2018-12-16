from math import fabs

"""
Table 01, default block (t01)

A simple table with four legs. Gets dimensions from block scaling, except for
leg diameter (5cm). Gets top material from first component and leg material
from third component.
"""

def make_table_01(data):
    try:
        component_pool = data['pool']
        component = component_pool[2]#gets third component for legs
        data['leg_color'] = component[1]
        data['leg_image'] = data['MATERIAL'] + '-' + component[0]
    except:
        data['leg_color'] = data['color']
        data['leg_image'] = data['8']

    outstr = '> \n'#blocks need to close wrapper
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

"""
Stalker, a look-out image with eventual balloon text and link.

Stalker always looks towards camera. Plane dimension is set by block X and Z
scaling. Image is set by material, text is on PARAM1, link tree is on PARAM2
(allowed values: parent, child, next, previous).
"""

def make_stalker(page, data):
    outstr = 'look-at="#camera-foot"> \n'#blocks need to close wrapper
    outstr += f'<a-plane id="{data["TYPE"]}-{data["num"]}" \n'
    outstr += f'position="0 {data["43"]/2} 0" \n'
    outstr += f'width="{fabs(data["41"])}" height="{fabs(data["43"])}" \n'
    outstr += entity_material(data)
    outstr += '</a-plane>\n'
    if data['PARAM1']:
        outstr += f'<a-plane id="a-text-{data["num"]}" \n'
        outstr += f'position="0 {data["43"]+data["41"]/4+.1} 0.01" \n'
        outstr += f'width="{fabs(data["41"])}" height="{fabs(data["41"])/2}" \n'
        outstr += f'text="width: {data["41"]*.9}; align: center; color: black; '
        outstr += f'value: {data["PARAM1"]}; wrap-count: {data["41"]*9}; '
        outstr += '">\n</a-plane>\n'
        outstr += f'<a-triangle id="triangle-{data["num"]}" \n'
        outstr += f'geometry="vertexA:0 {data["43"]+.1} 0.01; \n'
        outstr += f'vertexB:0 {data["43"]-.05} 0.01; \n'
        outstr += f'vertexC:{data["41"]/4} {data["43"]+.1} 0.01"> \n'
        outstr += '</a-triangle> \n'
    if data['PARAM2']:
        outstr += f'<a-link id="a-link-{data["num"]}" \n'
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

def close_leg(data):
        outstr = 'radius="0.025" \n'
        outstr += f'height="{data["leg"]}" \n'
        outstr += f'material="src: #{data["leg_image"]}; color: {data["leg_color"]} '
        outstr += '"></a-cylinder>\n'
        return outstr

    #returns positive/negative scaling
def unit(nounit):
    unit = fabs(nounit)/nounit
    return unit

def is_repeat(repeat, rx, ry):
    if repeat:
        output = f'; repeat:{fabs(rx)} {fabs(ry)}'
        return output
    else:
        return ';'

def entity_material(data):
    outstr = f'material="src: #{data["8"]}; color: {data["color"]}'
    outstr += is_repeat(data["repeat"], data["41"], data["43"])
    outstr += '">\n'
    return outstr
