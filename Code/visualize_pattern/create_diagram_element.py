box_identifier = 0
arrow_identifier = 0
hexagon_identifier = 0
ellipse_identifier = 0
document_identifier = 0

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

# Function to create a drawio.io ellipse element
def create_ellipse(ellipse_value, x_pos, y_pos):
    global ellipse_identifier
    ellipse_identifier += 1
    id = f'ellipse-{ellipse_identifier}'
    ellipse =   f'        <mxCell id="{id}" value="{ellipse_value}" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fontSize=17;" vertex="1" parent="1">\n'\
                f'          <mxGeometry x="{x_pos}" y="{y_pos}" width="30" height="30" as="geometry" />\n'\
                 '        </mxCell>\n'
    
    return ellipse, id, 30

def create_dashed_arrow(line_value, source, target):
    global arrow_identifier
    arrow_identifier += 1
    arrow = f'        <mxCell id="arrow-{arrow_identifier}" value="{line_value}" style="rounded=0;jumpSize=4;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;endFill=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;" edge="1" source="{source}" target="{target}" parent="1">\n'\
             '          <mxGeometry relative="1" as="geometry" />\n'\
             '        </mxCell>\n'
    return arrow

# Function to create a drawio.io empty dashed arrow element
def create_empty_dashed_arrow(source, target):
    global arrow_identifier
    arrow_identifier += 1
    arrow = f'        <mxCell id="arrow-{arrow_identifier}" value="" style="rounded=0;jumpSize=4;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;endFill=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;edgeStyle=orthogonalEdgeStyle;" edge="1" source="{source}" target="{target}" parent="1">\n'\
             '          <mxGeometry relative="1" as="geometry" />\n'\
             '        </mxCell>\n'
    return arrow

# Function to create a drawio.io hexagon element
def create_hexagon(hexagon_value, x_pos, y_pos):
    global hexagon_identifier
    hexagon_identifier += 1
    width = (len(hexagon_value)) * 3.3
    id = f'hexagon-{hexagon_identifier}'
    hexagon =   f'        <mxCell id="{id}" value="{hexagon_value}" style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;" vertex="1" parent="1">\n'\
                f'          <mxGeometry x="{x_pos}" y="{y_pos}" width="{width}" height="30" as="geometry" />\n'\
                 '        </mxCell>\n'
    
    return hexagon, id, width

def create_block_arrow(source, target):
    global arrow_identifier
    arrow_identifier += 1
    arrow = f'        <mxCell id="arrow-{arrow_identifier}" value="" style="endArrow=block;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;endFill=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endSize=8;arcSize=0;rounded=0;" edge="1" source="{source}" target="{target}" parent="1">\n'\
             '          <mxGeometry relative="1" as="geometry" />\n'\
             '        </mxCell>\n'
    return arrow

def create_double_block_dashed_arrow(line_value, source, target):
    global arrow_identifier
    arrow_identifier += 1
    arrow = f'        <mxCell id="arrow-{arrow_identifier}" value="{line_value}" style="endArrow=open;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;endFill=0;dashed=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;endSize=8;startArrow=open;startFill=0;startSize=8;rounded=0;" edge="1" source="{source}" target="{target}" parent="1">\n'\
             '          <mxGeometry relative="1" as="geometry" />\n'\
             '        </mxCell>\n'
    return arrow

def create_document(document_value, width_lenght, height_lenght, x_pos, y_pos):
    global document_identifier
    document_identifier += 1
    width = width_lenght * 6.2
    height = height_lenght * 25
    document =  f'        <mxCell id="document-{document_identifier}" value="{document_value}" style="shape=document;whiteSpace=wrap;html=1;boundedLbl=1;labelBackgroundColor=#ffffff;strokeColor=#000000;fontSize=12;fontColor=#000000;size=0.1875;align=left;" vertex="1" parent="1">\n'\
                f'          <mxGeometry x="{x_pos}" y="{y_pos}" width="{width}" height="{height}" as="geometry" />\n'\
                 '        </mxCell>\n'
    
    return document, width, height

def create_document2(document_value, width_lenght, height_lenght, x_pos, y_pos, pattern_number):
    global document_identifier
    document_identifier += 1
    width = width_lenght * 5.5
    height = height_lenght * 15
    document =  f'        <mxCell id="document-{document_identifier}" value="{pattern_number}" style="swimlane;whiteSpace=wrap;html=1;" vertex="1" parent="1">\n'\
                f'          <mxGeometry x="{x_pos}" y="{y_pos}" width="{width}" height="{height + 25}" as="geometry" />\n'\
                 '        </mxCell>\n'\
                f'        <mxCell id="text-document-{document_identifier}" value="{document_value}" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;align=left;" vertex="1" parent="document-{document_identifier}">\n'\
                f'          <mxGeometry x="0" y="25" width="{width}" height="{height}" as="geometry" />\n'\
                 '        </mxCell>\n'
    
    return document, width, height