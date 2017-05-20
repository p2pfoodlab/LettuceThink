use <xcarve-x-carriage.scad>

module gantry(length, width, height, tool_length, x, z, invert)
{
        color("black") {
                // x-rail
                translate([0, 0, 145]) cube([length, 45, 40]);
                // plates
                translate([-4, 0, 60]) cube([4, 45, 125]);
                translate([width, 0, 60]) cube([4, 45, 125]);
        }
        translate([x, -10, 145-40])
                x_carriage(height, tool_length, z, invert);
}

gantry(1000, 1000, 600, 600, 500, 500, 400, 1);