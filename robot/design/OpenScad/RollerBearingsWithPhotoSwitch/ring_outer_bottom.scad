module ring_outer_bottom()
{
    color("red") 
        difference() {
            union () {
                cylinder(r=27.75, h=20, $fn=720);
                rotate([0, 0, 45]) translate([25, -2.51, 20]) cube([2.65, 5, 11]);
                rotate([0, 0, 45]) translate([24, -2.51, 26]) rotate([0, 10, 0]) cube([2.65, 5, 5]);
                rotate([0, 0, 225]) translate([25, -2.51, 20]) cube([2.65, 5, 11]);
                rotate([0, 0, 225]) translate([24, -2.51, 26]) rotate([0, 10, 0]) cube([2.65, 5, 5]);
                

            }
            translate([0, 0, -1]) cylinder(r=22, h=22, $fn=720);
            translate([0, 0, 13]) cylinder(r=47/2, h=8, $fn=720);
            translate([25, -2.5, -1]) cube([4, 5, 22]);
            translate([0, -10, 8]) rotate([90, 0, 0]) cylinder(r=2.75, h=20, $fn=720);
            translate([0, 10, 8]) rotate([-90, 0, 0]) cylinder(r=2.75, h=20, $fn=720);
    }
}

ring_outer_bottom();