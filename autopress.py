from solid import *

use('lib/springs.scad')

RESOLUTION = 40

aeropress_d = 15.
spring_base_x = aeropress_d * 2.
spring_base_y = aeropress_d * 1.3
spring_base_z = 5.

spring_top_z = spring_base_z/2.

lswitch_x = 2.0
lswitch_y = 1.0
lswitch_z = 2.2
lswitch_sink = 0.5

lead_screw_d = 3.0
lead_screw_h = 24.
lead_screw_pad = 1.0

hexnut_d = 5.
hexnut_sink = 2.

spring_d = 3.2
spring_h = 5.0
spring_sink = spring_h/5.

rod_hole_start_h = 1.
rod_d = 1.0
bearing_od = 2.0
bearing_id = 1.0
bearing_h = 3.0
rod_h = 25.

stepper_x = 8.
stepper_y = 8.
stepper_sink = 2.

top_to_roof_dist = 5.0

spring_locs = []
rod_holes = []
lead_screw_holes = []

pad = spring_d

SPRINGS = 0

def spring_base():
    r = cube([spring_base_x,spring_base_y,spring_base_z])
    spr = translate([0,0,spring_base_z - spring_sink])( cylinder(d = spring_d, h = spring_h) )

    r -= translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,spring_base_z - lswitch_sink + 1e-3])( cube([lswitch_x, lswitch_y, lswitch_sink]) )

    for x in [0+pad, spring_base_x-pad]:
    
        lsh = translate([x, spring_base_y/2., -1e-3])(cylinder(d = lead_screw_d + lead_screw_pad, h = lead_screw_h))
        stepper = translate([x-stepper_x/2, spring_base_y/2.-stepper_y/2, -1e-3])(cube([stepper_x,stepper_y,stepper_sink]))
        r -= lsh
        r -= stepper
        lead_screw_holes.append(lsh)

        for y in [0+pad, spring_base_y-pad]:
            spring_locs.append([x,y,spring_base_z - spring_sink])
            hol = translate([x,y,rod_hole_start_h])(cylinder(d = rod_d, h = rod_h))
            r -= hol
            rod_holes.append(hol)
            r -= translate([x,y,0])(spr)

    return r

def spring_top():
    r = cube([spring_base_x,spring_base_y,spring_top_z])
    spr = translate([0,0,-1e-3])( cylinder(d = spring_d, h = spring_sink) )
    for i in lead_screw_holes:
        r -= i
    for i in spring_locs:
        r -= translate([i[0],i[1],0])(spr)
        r -= translate([i[0],i[1],0])(cylinder(d = bearing_od, h = spring_top_z + 1e-3))
    return r

def top_plate():
    r = cube([spring_base_x,spring_base_y,spring_top_z])
    for x in [0+pad, spring_base_x-pad]:
        lsh = translate([x, spring_base_y/2., spring_top_z - hexnut_sink + 1e-3])(cylinder(d = hexnut_d, h = hexnut_sink,segments=6))
        r -= lsh
        lsh = translate([x, spring_base_y/2., -1e-3])(cylinder(d = lead_screw_d, h = spring_top_z + 1e-3))
        r -= lsh
    
    for i in spring_locs:
        r -= translate([i[0],i[1],-1e-3])(cylinder(d = bearing_od, h = spring_top_z + 2e-3))

    return r

def roof_plate():
    r = cube([spring_base_x,spring_base_y,spring_top_z])
    for i in spring_locs:
        r -= translate([i[0],i[1],-1e-3])(cylinder(d = rod_d, h = spring_top_z - rod_hole_start_h))
    r -= translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,-1e-3])( cube([lswitch_x, lswitch_y, lswitch_sink]) )
    return r


def _spring():
    return spring(_Windings = 10, R = spring_d/2, r = spring_d/20, h = spring_h, slices = 20)

def bearing():
    return cylinder(d = bearing_od, h = bearing_h) - translate([0,0,-1e-3])(cylinder(d = bearing_id, h = bearing_h + 2e-3))

def hexnut():
    pass

def lswitch():
    return cube([lswitch_x, lswitch_y, lswitch_z])

def lead_screw():
    return cylinder(d = lead_screw_d, h = lead_screw_h)

def rod():
    return cylinder(d = rod_d, h = rod_h)

def case():
    pass

def assembly():
    sb = spring_base()
    s = _spring()
    if SPRINGS:
        for l in spring_locs:
            sb += translate(l)(s) 
    sb += translate([0,0,spring_base_z + spring_h - spring_sink*2])(spring_top())
    lsw = translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,lswitch_sink - lswitch_z])( lswitch() )
    tp = top_plate() + translate([0,0,top_to_roof_dist])(roof_plate()+color('red')(lsw))
    sb += translate([0,0,spring_base_z * 4])(tp)

    for i in spring_locs:
        sb += translate([0,0,spring_h - spring_sink])( translate(i)(color('orange')(bearing())))
        sb += translate([0,0,spring_base_z * 4 - i[2]])( translate(i)(color('orange')(bearing())))
        sb += translate([i[0], i[1], rod_hole_start_h])( color('pink')(rod()))

    for x in [0+pad, spring_base_x-pad]:
        ls = translate([x, spring_base_y/2., spring_top_z - hexnut_sink + 1e-3])(lead_screw())
        sb += color('orange')(ls)

    lsw = translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,spring_base_z - lswitch_sink + 1e-3])( lswitch() )
    sb += color('red')(lsw)

    return sb

open('scad/spring_base.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(spring_base()))
open('scad/spring_top.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(spring_top()))
open('scad/top_plate.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(top_plate()))
open('scad/roof_plate.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(roof_plate()))
open('scad/assembly.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(assembly()))
print 'done'


