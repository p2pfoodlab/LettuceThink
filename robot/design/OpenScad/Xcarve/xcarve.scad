use <../Common/tubular.scad>
use <xcarve-gantry.scad>

module base_frames(length, width)
{
        color("black") {
                cube([length, 20, 20]);
                translate([0, 980, 0]) cube([length, 20, 20]);
        }
}

module y_rails(length, width)
{
        color("black") {
                translate([0, 0, 60]) cube([20, length, 40]);
                translate([980, 0, 60]) cube([20, length, 40]);

                translate([0, -4, 0]) cube([20, 4, 100]);
                translate([0, width, 0]) cube([20, 4, 100]);
                translate([length-20, -4, 0]) cube([20, 4, 100]);
                translate([length-20, width, 0]) cube([20, 4, 100]);
        }
}

module xcarve(length, width, height, tool_length, x, y, z, invert)
{
        base_frames(length, width);
        y_rails(length, width);
        *translate([0, y, 0])
                gantry(length, width, height, tool_length, x, z, invert);
}

module xcarve_upside_down(length, width, height, tool_length, x, y, z)
{
        translate([0, width, 20]) 
        rotate([180, 0, 0]) {
                xcarve(length, width, height, tool_length, x, y, z, 1);
        }
}

//xcarve(1000, 1000, 800, 500, 500, 600);
translate([0, 1000, 20]) 
rotate([180, 0, 0]) {
        xcarve(1000, 1000, 600, 600, 500, 500, 400, 1);
}
