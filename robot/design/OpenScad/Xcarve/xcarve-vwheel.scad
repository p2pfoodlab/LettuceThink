
module vwheel(spacer)
{
        color("grey") {
                translate([0, 0, 10]) cylinder(r=12, h=10);
                cylinder(r=5, h=spacer);
        }
}
