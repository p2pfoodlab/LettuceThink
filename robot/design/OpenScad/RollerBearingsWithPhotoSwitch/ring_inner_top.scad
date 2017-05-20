module ring_inner_top()
{
    color("red") 
        union() {
            difference() {
                translate([0, 0, 0]) cylinder(r=19, h=5, $fn=720);
                translate([0, 0, -0.1]) cylinder(r=35/2+0.02, h=5.2, $fn=720);
                //translate([17, 0, -0.1]) cylinder(r=2.5, h=5.2);
                //translate([-17, 0, -0.1]) cylinder(r=2.5, h=5.2);
            }
            difference() {
                translate([0, 0, 5]) cylinder(r=19, h=14, $fn=720);
                translate([0, 0, 4.9]) cylinder(r=15.1, h=14.2, $fn=720);
                translate([17, 0, 4.9]) cylinder(r=1, h=14.2, $fn=720);
                translate([-17, 0, 4.9]) cylinder(r=1, h=14.2, $fn=720);
            }
        }
}

ring_inner_top();
