module ring_inner_bottom()
{
    color("red") 
        difference() {
            union() {
                cylinder(r=24, h=15, $fn=720);
                translate([0, 0, 15]) cylinder(r=19, h=23, $fn=720);
                translate([0, 0, 38]) cylinder(r=35/2, h=12, $fn=720);
                //translate([17, 0, 45]) cylinder(r=2.5, h=5);
                //translate([-17, 0, 45]) cylinder(r=2.5, h=5);
            }
            translate([0, 0, -1]) cylinder(r=15.1, h=52,$fn=720);
            translate([0, 0, -1]) cube([30, 1, 52]);
        }
}

ring_inner_bottom();