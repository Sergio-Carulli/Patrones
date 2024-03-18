def create_box(box_value, x_pos, y_pos):
    width = (len(box_value)) * 6.2
    box =   '      <g>\n'\
            f'         <rect x="{x_pos}" y="{y_pos}" width="{width}" height="30" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>\n'\
            '      </g>\n'\
            '      <g>\n'\
            '         <g transform="translate(-0.5 -0.5)">\n'\
            '            <switch>\n'\
            '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
            f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: {width - 2.4}px; height: 1px; padding-top: {y_pos + 15}px; margin-left: {x_pos + 1.5}px;">\n'\
            '                     <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
            f'                        <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">{box_value}</div>\n'\
            '                     </div>\n'\
            '                  </div>\n'\
            '               </foreignObject>\n'\
            '            </switch>\n'\
            '         </g>\n'\
            '      </g>\n'
    return box, width

def create_underlined_box(box_value, x_pos, y_pos):
    width = (len(box_value)) * 6.2
    box =   '      <g>\n'\
            f'         <rect x="{x_pos}" y="{y_pos}" width="{width}" height="30" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>\n'\
            '      </g>\n'\
            '      <g>\n'\
            '         <g transform="translate(-0.5 -0.5)">\n'\
            '            <switch>\n'\
            '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
            f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: {width - 2.4}px; height: 1px; padding-top: {y_pos + 15}px; margin-left: {x_pos + 1.5}px;">\n'\
            '                     <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
            f'                        <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;"><u>{box_value}</u></div>\n'\
            '                     </div>\n'\
            '                  </div>\n'\
            '               </foreignObject>\n'\
            '            </switch>\n'\
            '         </g>\n'\
            '      </g>\n'
    
    return box, width

def create_block_arrow(arrow_value, x_pos, y_pos):
    next_x = len(arrow_value) * 8 + x_pos
    arrow = '      <g>\n'\
            f'         <path d="M {x_pos} {y_pos} L {next_x - 10.12} {y_pos}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>\n'\
            f'         <path d="M {next_x - 1.12} {y_pos} L {next_x - 10.12} {y_pos + 4.5} L {next_x - 10.12} {y_pos - 4.5} Z" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
            '      </g>\n'
    return arrow, next_x

def create_double_block_dashed_arrow(arrow_value, x_pos, next_x, y_pos):
    arrow = '      <g>\n'\
            f'         <path d="M {x_pos + 2.24} {y_pos} L {next_x - 2.24} {y_pos}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" stroke-dasharray="3 3" pointer-events="stroke"/>\n'\
            f'         <path d="M {x_pos + 10.12} {y_pos - 4.5} L {x_pos + 1.12} {y_pos} L {x_pos + 10.12} {y_pos + 4.5}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
            f'         <path d="M {next_x - 10.12} {y_pos + 4.5} L {next_x - 1.12} {y_pos} L {next_x - 10.12} {y_pos - 4.5}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
            '      </g>\n'\
            '      <g>\n'\
            '         <g transform="translate(-0.5 -0.5)">\n'\
            '            <switch>\n'\
            '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
            f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: 15px; margin-left: {(x_pos + next_x)/2}px;">\n'\
            '                     <div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
            f'                        <div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;">{arrow_value}</div>\n'\
            '                     </div>\n'\
            '                  </div>\n'\
            '               </foreignObject>\n'\
            '            </switch>\n'\
            '         </g>\n'\
            '      </g>\n'
    
    return arrow, next_x

def create_empty_box(x_pos, y_pos):
    box =   '      <g>\n'\
            f'         <rect x="{x_pos}" y="{y_pos}" width="60" height="30" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>\n'\
            '      </g>\n'
    
    return box, 60

def create_empty_box_2(width, x_pos, y_pos):
    box =   '      <g>\n'\
            f'         <rect x="{x_pos}" y="{y_pos}" width="{width}" height="30" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>\n'\
            '      </g>\n'
    
    return box, width

def create_arrow(arrow_value, start_x_axis, end_x_axis, y_pos):
    arrow = '      <g>\n'\
            f'         <path d="M {start_x_axis} {y_pos} L {end_x_axis - 7.87} {y_pos}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="stroke"/>\n'\
            f'         <path d="M {end_x_axis - 1.12} {y_pos} L {end_x_axis - 10.12} {y_pos + 4.5} L {end_x_axis - 7.87} {y_pos} L {end_x_axis - 10.12} {y_pos - 4.5} Z" fill="rgb(0, 0, 0)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
            '      </g>\n'\
            '      <g>\n'\
            '         <g transform="translate(-0.5 -0.5)">\n'\
            '            <switch>\n'\
            '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
            f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: {y_pos}px; margin-left: {(start_x_axis + end_x_axis)/2}px;">\n'\
            '                     <div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
            f'                        <div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;">{arrow_value}</div>\n'\
            '                     </div>\n'\
            '                  </div>\n'\
            '               </foreignObject>\n'\
            '            </switch>\n'\
            '         </g>\n'\
            '      </g>\n'
    return arrow

def create_dashed_arrow(arrow_value, start_x_axis, end_x_axis, y_pos):
    arrow = '      <g>\n'\
            f'         <path d="M {start_x_axis} {y_pos} L {end_x_axis - 2.24} {y_pos}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" stroke-dasharray="3 3" pointer-events="stroke"/>\n'\
            f'         <path d="M {end_x_axis - 8.12} {y_pos + 3.5} L {end_x_axis - 1.12} {y_pos} L {end_x_axis - 8.12} {y_pos - 3.5}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
            '      </g>\n'\
            '      <g>\n'\
            '         <g transform="translate(-0.5 -0.5)">\n'\
            '            <switch>\n'\
            '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
            f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 1px; height: 1px; padding-top: {y_pos}px; margin-left: {(start_x_axis + end_x_axis)/2}px;">\n'\
            '                     <div data-drawio-colors="color: rgb(0, 0, 0); background-color: rgb(255, 255, 255); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
            f'                        <div style="display: inline-block; font-size: 11px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; background-color: rgb(255, 255, 255); white-space: nowrap;">{arrow_value}</div>\n'\
            '                     </div>\n'\
            '                  </div>\n'\
            '               </foreignObject>\n'\
            '            </switch>\n'\
            '         </g>\n'\
            '      </g>\n'

    return arrow

def create_empty_dashed_arrow(start_x_axis, end_x_axis, y_pos):
    arrow =     '      <g>\n'\
                f'         <path d="M {start_x_axis} {y_pos} L {end_x_axis - 2.24} {y_pos}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" stroke-dasharray="3 3" pointer-events="stroke"/>\n'\
                f'         <path d="M {end_x_axis - 8.12} {y_pos + 3.5} L {end_x_axis - 1.12} {y_pos} L {end_x_axis - 8.12} {y_pos - 3.5}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
                '      </g>\n'

    return arrow

def create_empty_orthogonal_dashed_arrow(start_x_axis, end_x_axis, start_y_axis, end_y_axis):
    mid = (start_x_axis + end_x_axis)/2
    arrow =     '      <g>\n'\
                f'         <path d="M {start_x_axis} {start_y_axis} L {mid} {start_y_axis} L {mid} {end_y_axis} L {end_x_axis - 2.24} {end_y_axis}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" stroke-dasharray="3 3" pointer-events="stroke"/>\n'\
                f'         <path d="M {end_x_axis - 8.12} {end_y_axis + 3.5} L {end_x_axis - 1.12} {end_y_axis} L {end_x_axis - 8.12} {end_y_axis - 3.5}" fill="none" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
                '      </g>\n'

    return arrow

def create_ellipse(ellipse_value, x_pos, y_pos):
    ellipse =   '      <g>\n'\
                f'         <ellipse cx="{x_pos + 15}" cy="{y_pos + 15}" rx="15" ry="15" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" pointer-events="all"/>\n'\
                '      </g>\n'\
                '      <g>\n'\
                '         <g transform="translate(-0.5 -0.5)">\n'\
                '            <switch>\n'\
                '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
                f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 28px; height: 1px; padding-top: {y_pos + 15}px; margin-left: {x_pos + 1}px;">\n'\
                '                     <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
                f'                        <div style="display: inline-block; font-size: 17px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">{ellipse_value}</div>\n'\
                '                     </div>\n'\
                '                  </div>\n'\
                '               </foreignObject>\n'\
                '            </switch>\n'\
                '         </g>\n'\
                '      </g>\n'
    
    return ellipse, 30

def create_hexagon(hexagon_value, x_pos, y_pos, width):
    next_x_pos = width + x_pos
    hexagon =   '      <g>\n'\
                f'         <path d="M {x_pos + 20} {y_pos} L {next_x_pos - 20} {y_pos} L {next_x_pos} {y_pos + 15} L {next_x_pos - 20} {y_pos + 30} L {x_pos + 20} {y_pos + 30} L {x_pos} {y_pos + 15} Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
                '      </g>\n'\
                '      <g>\n'\
                '         <g transform="translate(-0.5 -0.5)">\n'\
                '            <switch>\n'\
                '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
                f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: {width - 2}px; height: 1px; padding-top: {y_pos + 15}px; margin-left: {x_pos + 1}px;">\n'\
                '                     <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
                f'                        <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">{hexagon_value}</div>\n'\
                '                     </div>\n'\
                '                  </div>\n'\
                '               </foreignObject>\n'\
                '            </switch>\n'\
                '         </g>\n'\
                '      </g>\n'
    
    return hexagon, width

def create_cloud(x_pos, y_pos):
    print(x_pos, y_pos)
    #437 30 
    cloud = '      <g>\n'\
            f'         <path d="M {x_pos + 37.3} {y_pos - 10} C {x_pos + 13.3} {y_pos - 10} {x_pos + 7.3} {y_pos + 10} {x_pos + 26.5} {y_pos + 14} C {x_pos + 7.3} {y_pos + 22.8} {x_pos + 28.9} {y_pos + 42} {x_pos + 44.5} {y_pos + 34} C {x_pos + 55.3} {y_pos + 50} {x_pos + 91.3} {y_pos + 50} {x_pos + 103.3} {y_pos + 34} C {x_pos + 127.3} {y_pos + 34} {x_pos + 127.3} {y_pos + 18} {x_pos + 112.3} {y_pos + 10} C {x_pos + 127.3} {y_pos - 6} {x_pos + 103.3} {y_pos - 22} {x_pos + 82.3} {y_pos - 14} C {x_pos + 67.3} {y_pos - 26} {x_pos + 43.3} {y_pos - 26} {x_pos + 37.3} {y_pos - 10} Z" fill="rgb(255, 255, 255)" stroke="rgb(0, 0, 0)" stroke-miterlimit="10" pointer-events="all"/>\n'\
            '      </g>\n'\
            '      <g>\n'\
            '         <g transform="translate(-0.5 -0.5)">\n'\
            '            <switch>\n'\
            '               <foreignObject pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility" style="overflow: visible; text-align: left;">\n'\
            f'                  <div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: {y_pos + 10}px; margin-left: {x_pos + 8}px;">\n'\
            '                     <div data-drawio-colors="color: rgb(0, 0, 0); " style="box-sizing: border-box; font-size: 0px; text-align: center;">\n'\
            '                        <div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: rgb(0, 0, 0); line-height: 1.2; pointer-events: all; white-space: normal; overflow-wrap: normal;">No further chowlk <br />notation</div>\n'\
            '                     </div>\n'\
            '                  </div>\n'\
            '               </foreignObject>\n'\
            '            </switch>\n'\
            '         </g>\n'\
            '      </g>\n'
    return cloud