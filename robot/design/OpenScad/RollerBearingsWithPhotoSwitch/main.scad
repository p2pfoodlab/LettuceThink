use <../tubular.scad>;
use <ring_outer_bottom.scad>;
use <ring_outer_top.scad>;
use <ring_inner_bottom.scad>;
use <ring_inner_top.scad>;

module ball_bearing()
{
        color("gray") 
                difference() {
                cylinder(r=47/2, h=7);
                translate([0, 0, -1]) cylinder(r=35/2, h=9);
        }
}

module disk_circuit()
{
        color("darkgreen") 
                difference() {
                cylinder(r=27, h=2);
                translate([0, 0, -1]) cylinder(r=20, h=4);
                translate([25, -2.5, -1]) cube([4, 5, 8]);
        }
}

module photoreflector()
{
        color("black") {
            cube([6.4, 4.9, 6.5], center=true);
        }
}

module disk_reflector()
{
        color("grey") 
                difference() {
                cylinder(r=27, h=2);
                translate([0, 0, -1]) cylinder(r=16.1, h=4);
        }
}

*translate([0, 0, -50])
    round_tube(30, 200);

translate([0, 0, -25])
    ring_inner_bottom();

ring_outer_bottom();

*translate([0, 0, 13])
    ball_bearing();

translate([0, 0, -25])
    translate([0, 0, 45])
        ring_inner_top();

translate([0, 0, 20])
    ring_outer_top();

*union() {
    translate([0, 0, 26])
        disk_circuit();
    translate([0, 20+2.5, 28+6.5/2])
        photoreflector();
    translate([0, -20-2.5, 28+6.5/2])
        rotate([0, 0, 180])
        photoreflector();
}

*translate([0, 0, -25])
    translate([0, 0, 64])
        disk_reflector();

*translate([0, 0, -1])
    round_tube(60, 100);
