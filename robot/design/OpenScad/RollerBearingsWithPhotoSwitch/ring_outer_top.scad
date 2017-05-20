module ring_outer_top()
{
    color("red") 
        difference() {
        cylinder(r=27.75, h=6, $fn=720);
        translate([0, 0, -1]) cylinder(r=47/2-2, h=8, $fn=720);
        translate([25, -2.5, -1]) cube([4, 5, 8]);
        rotate([0, 0, 45]) translate([25, -2.51, -1]) cube([4, 5.2, 8]);
        rotate([0, 0, 225]) translate([25, -2.51, -1]) cube([4, 5.2, 8]);
        translate([25, -2.5, -1]) cube([4, 5, 8]);
        translate([0, 25, -0.1]) cylinder(r=1, h=8.2, $fn=720);
        translate([0, -25, -0.1]) cylinder(r=1, h=8.2, $fn=720);
    }
}

ring_outer_top();