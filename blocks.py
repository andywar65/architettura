from math import fabs

def make_table_01(data):
    try:
        component_pool = data['pool']
        component = component_pool[1]#gets second component for legs
        data['leg_color'] = component[1]
        data['leg_image'] = data['MATERIAL'] + '-' + component[0]
    except:
        data['leg_color'] = data['color']
        data['leg_image'] = data['8']

    #table top
        outstr = f'<a-box id="{data["2"]}-{data["num"]}-table-top" \n'
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
