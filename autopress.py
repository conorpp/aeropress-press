from solid import *

use('lib/springs.scad')


ptol = 0.9
ptol_tight = 0.5

RESOLUTION = 40

aeropress_d = 108.
spring_base_x = aeropress_d * 1.6
spring_base_y = aeropress_d * 1.1
spring_base_z = 67.

spring_top_z = spring_base_z/5.

lswitch_x = 8.0 + ptol
lswitch_y = 5.0 + ptol
lswitch_z = 5.
lswitch_compressed_z = 1.5 # how much it moves when clicked
lswitch_sink = 0.5

lead_screw_d = 8.0
lead_screw_h = 350
lead_screw_pad = 10.2 - lead_screw_d + ptol_tight
lead_nut_r = 8.0 # for the mounting holes
lead_nut_hole_d = 3.5 + ptol # for the mounting holes

hexnut_d = 5.
hexnut_sink = 2.

spring_d = 18.0
spring_h = 25.4
spring_compressed_h = 9.652
spring_sink = spring_compressed_h/2 - (lswitch_z - lswitch_sink)/2. + lswitch_compressed_z/2.

rod_hole_start_h = spring_base_z - spring_sink - 5.
rod_d = 8
bearing_od = 15.
bearing_id = 8.0 + 0.1
bearing_h = 24.0
rod_h = lead_screw_h + 15.0

coupler_od = 25.0 + ptol * 5

stepper_x = 42. + ptol
stepper_y = 42. + ptol
stepper_z = 48.
stepper_ring_d = 22. + ptol
stepper_ring_h = 2.0
stepper_sink = 48.

top_to_roof_dist = 25.0

keep_out_d = 108.0
max_h = 435.0
min_inside_h = 381.0

spring_locs = []
rod_holes = []
lead_screw_holes = []

pad = spring_d

SPRINGS = 0
SPLICE = 0

def spring_base():
    r = cube([spring_base_x,spring_base_y,spring_base_z])
    spr = translate([0,0,spring_base_z - spring_sink])( cylinder(d = spring_d + ptol, h = spring_h) )

    r -= translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,spring_base_z - lswitch_sink + 1e-3])( cube([lswitch_x, lswitch_y, lswitch_sink]) )

    for x in [0+pad, spring_base_x-pad]:
    
        lsh = translate([x, spring_base_y/2., -1e-3])(cylinder(d = coupler_od, h = lead_screw_h))
        stepper = translate([x-stepper_x/2, spring_base_y/2.-stepper_y/2, -1e-3])(cube([stepper_x,stepper_y,stepper_sink]))
        stepper_ring = translate([x, spring_base_y/2., stepper_sink - 1e-2])(cylinder(h = stepper_ring_h + 1e-2, d = stepper_ring_d))
        r -= lsh
        r -= stepper
        r -= stepper_ring
        lead_screw_holes.append(lsh)

        for y in [0+pad, spring_base_y-pad]:
            spring_locs.append([x,y,spring_base_z - spring_sink])
            hol = translate([x,y,rod_hole_start_h])(cylinder(d = rod_d + ptol_tight, h = rod_h))
            r -= hol
            rod_holes.append(hol)
            r -= translate([x,y,0])(spr)

    return r

def spring_top():
    r = cube([spring_base_x,spring_base_y,spring_top_z])
    spr = translate([0,0,-1e-3])( cylinder(d = spring_d + ptol, h = spring_sink) )
    for i in lead_screw_holes:
        r -= i
    for i in spring_locs:
        r -= translate([i[0],i[1],0])(spr)
        r -= translate([i[0],i[1],0])(cylinder(d = bearing_od + ptol_tight, h = spring_top_z + 1e-3))

    r -= translate([spring_base_x/2,spring_base_y/2, spring_top_z - 2.0])(cylinder(d = keep_out_d*4/5, h = 3.0))
    return r

def top_plate():
    r = cube([spring_base_x,spring_base_y,spring_top_z])

    leg_x = pad * 2
    leg_y = spring_base_y
    leg_z = spring_top_z*1.4
    legr = translate([0,0,0])( cube([leg_x, leg_y, leg_z]))
    legl = translate([spring_base_x - leg_x,0,0])( cube([leg_x, leg_y, leg_z]))

    print 'screw len min: ', spring_top_z

    for x in [0+pad, spring_base_x-pad]:
        lsh = translate([x, spring_base_y/2., spring_top_z - hexnut_sink + 1e-3])(cylinder(d = hexnut_d, h = hexnut_sink,segments=6))
        r -= lsh
        legr -= lsh
        legl -= lsh
        lsh = translate([x, spring_base_y/2., -1e-3])(cylinder(d = lead_screw_d + lead_screw_pad, h = spring_top_z*2),
                translate([lead_nut_r,0,0])(cylinder(d = lead_nut_hole_d, h = spring_top_z*2)),
                translate([-lead_nut_r,0,0])(cylinder(d = lead_nut_hole_d, h = spring_top_z*2)),
                translate([0,lead_nut_r,0])(cylinder(d = lead_nut_hole_d, h = spring_top_z*2)),
                translate([0,-lead_nut_r,0])(cylinder(d = lead_nut_hole_d, h = spring_top_z*2)),
                translate([0,0,0])(cylinder(d = lead_nut_r * 2 + lead_nut_hole_d *1.8, h = leg_z))
   
                )
        r -= lsh
        legr -= lsh
        legl -= lsh

    for i in spring_locs:
        s = translate([i[0],i[1],-1e-3])(cylinder(d = bearing_od + ptol_tight, h = spring_top_z*2 + 2e-3))
        r -= s
        legr -= s
        legl -= s

    r -= translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,-1e-3])( cube([lswitch_x, lswitch_y, lswitch_sink]) )
    r += translate([0,0,-leg_z])(legr)
    r += translate([0,0,-leg_z])(legl)
    
    r -= translate([pad*1.5,pad*1.5/4,-spring_top_z])(cube([spring_base_x-2*pad*1.5,spring_base_y,spring_top_z]))

    return r

def sense_plate():
    return translate([pad*1.5 + ptol/2,0,0])(cube([spring_base_x-2*pad*1.5 - ptol,spring_base_y - pad * 1.5/4,spring_top_z/2]))

def roof_plate():
    r = cube([spring_base_x,spring_base_y,spring_top_z])
    for i in spring_locs:
        r -= translate([i[0],i[1],-1e-3])(cylinder(d = rod_d + ptol_tight, h = spring_top_z - rod_hole_start_h))
    r -= translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,-1e-3])( cube([lswitch_x, lswitch_y, lswitch_sink]) )
    return r


def _spring():
    return spring(_Windings = 6, R = spring_d/2, r = spring_d/20, h = spring_h, slices = 20)

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
    tp = top_plate() + translate([0,0,top_to_roof_dist])(roof_plate()+color('red')(lsw)) + translate([0,0,0])(color('red')(lsw))

    top_plates_h = rod_h - top_to_roof_dist + rod_hole_start_h + 1e-1
    sb += translate([0,0,top_plates_h])(tp) 

    for i in spring_locs:
        sb += translate([0,0,spring_h - spring_sink])( translate(i)(color('orange')(bearing())))
        #sb += translate([0,0,top_plates_h - i[2]])( translate(i)(color('orange')(bearing())))
        sb += translate([i[0], i[1], rod_hole_start_h])( color('pink')(rod()))

    for x in [0+pad, spring_base_x-pad]:
        ls = translate([x, spring_base_y/2., spring_base_z - hexnut_sink + 1e-3])(lead_screw())
        sb += color('orange')(ls)

    lsw = translate([(spring_base_x - lswitch_x)/2.,(spring_base_y - lswitch_y)/2.,spring_base_z - lswitch_sink + 1e-3])( lswitch() )
    sb += color('red')(lsw)

    sb += translate([0,pad*1.5/4,top_plates_h - spring_top_z])(color('orange')(sense_plate()))


    if SPLICE:
        sb -= translate([-1e-3,-1e-3,0])(cube([100,pad,1000]))
        sb -= rotate([0,0,90])(translate([-1e-3,+1e-3-pad,0])(cube([100,pad,1000])))



    nema = import_stl('../models/nema17.stl')
    nema = color('grey')(nema)
    nema = translate([pad,spring_base_y/2,-stepper_z/2 + stepper_sink])(nema)
    sb += nema

    # coffee mug, keep outs

    mug = translate([spring_base_x/2, spring_base_y/2, spring_base_z + spring_h])( scale([1.0]*3)(import_stl("../models/mug.stl")) )

    aero = cylinder(d = 11.0, h = 2.)
    aero += translate([0,0,2.])(cylinder(d = 8.0, h = 10))
    aero = color('Bisque')(aero)
    aero2 = translate([0,0,12.])(cylinder(d = 7.0, h = 9.))
    aero2 += translate([0,0,21.])(cylinder(d = 11.0, h = 2.))
    aero2 = color('BurlyWood')(aero2)
    aero += aero2
    
    aero = translate([spring_base_x/2, spring_base_y/2, spring_base_z + spring_h + 9])( aero )

    sb += (color('tan')(mug) + aero)

    sb += color([0.5,0.2,0., 0.5])(translate([spring_base_x/2, spring_base_y/2, 0])(cylinder(d = keep_out_d, h = max_h)))
    sb += color([0.7,.7,1., .4])(translate([spring_base_x/2, spring_base_y/2, 0])(cylinder(d = keep_out_d, h = min_inside_h)))
    return sb

open('scad/spring_base.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(spring_base()))
open('scad/spring_top.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(spring_top()))
open('scad/top_plate.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(top_plate()))
open('scad/roof_plate.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(roof_plate()))
open('scad/assembly.scad','w+').write(('$fn=%d;' % RESOLUTION)+scad_render(assembly()))
print 'done'


