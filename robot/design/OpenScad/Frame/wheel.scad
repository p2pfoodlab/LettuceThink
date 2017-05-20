module wheel(radius, thick, axis_width)
{
    color("black")
        rotate([90, 0, 0])
            rotate_extrude(convexity = 100, $fn = 100)
                translate([radius-thick/2, 0, 0])
                    circle(r = thick/2, $fn = 100);
    color("grey") {
        rotate([90, 0, 0])
                difference() {
                cylinder(h=0.6*thick, r=radius-0.8*thick, center=true);
                translate([0, 0, 0])
                        cylinder(h=0.6*thick+2, r=radius-1.1*thick, center=true);
        }
        rotate([90, 0, 0])
            cylinder(h=axis_width+2*20, r=5, center=true);
        rotate([90, 0, 0])
            cylinder(h=axis_width-10, r=20, center=true);
        rotate([90, 0, 0])
            cylinder(h=thick, r=80, center=true);
    }
}

translate([0, 0, 160])
   wheel(160, 50, 110);
