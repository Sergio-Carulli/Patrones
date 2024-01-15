box_identifier = 0
arrow_identifier = 0

# Function to create a drawio.io box element
def create_box(box_value, x_pos, y_pos):
    global box_identifier
    box_identifier += 1
    width = (len(box_value)) * 6.2
    id = f'class-{box_identifier}'
    box =   f'        <mxCell id="{id}" value="{box_value}" style="rounded=0;whiteSpace=wrap;html=1;snapToPoint=1;points=[[0.1,0],[0.2,0],[0.3,0],[0.4,0],[0.5,0],[0.6,0],[0.7,0],[0.8,0],[0.9,0],[0,0.1],[0,0.3],[0,0.5],[0,0.7],[0,0.9],[0.1,1],[0.2,1],[0.3,1],[0.4,1],[0.5,1],[0.6,1],[0.7,1],[0.8,1],[0.9,1],[1,0.1],[1,0.3],[1,0.5],[1,0.7],[1,0.9]];" vertex="1" parent="1">\n'\
            f'          <mxGeometry x="{x_pos}" y="{y_pos}" width="{width}" height="30" as="geometry" />\n'\
             '        </mxCell>\n'
    
    return box, id, width

# Function to create a drawio.io box element
def create_empty_box(x_pos, y_pos):
    global box_identifier
    box_identifier += 1
    id = f'class-{box_identifier}'
    box =   f'        <mxCell id="{id}" value="" style="rounded=0;whiteSpace=wrap;html=1;snapToPoint=1;points=[[0.1,0],[0.2,0],[0.3,0],[0.4,0],[0.5,0],[0.6,0],[0.7,0],[0.8,0],[0.9,0],[0,0.1],[0,0.3],[0,0.5],[0,0.7],[0,0.9],[0.1,1],[0.2,1],[0.3,1],[0.4,1],[0.5,1],[0.6,1],[0.7,1],[0.8,1],[0.9,1],[1,0.1],[1,0.3],[1,0.5],[1,0.7],[1,0.9]];" vertex="1" parent="1">\n'\
            f'          <mxGeometry x="{x_pos}" y="{y_pos}" width="60" height="30" as="geometry" />\n'\
             '        </mxCell>\n'
    
    return box, id, 60

# Function to create a drawio.io arrow element
def create_arrow(line_value, source, target):
    global arrow_identifier
    arrow_identifier += 1
    arrow = f'        <mxCell id="arrow-{arrow_identifier}" value="{line_value}" style="endArrow=classic;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endSize=8;arcSize=0;rounded=0;" edge="1" source="{source}" target="{target}" parent="1">\n'\
             '          <mxGeometry relative="1" as="geometry" />\n'\
             '        </mxCell>\n'
    return arrow