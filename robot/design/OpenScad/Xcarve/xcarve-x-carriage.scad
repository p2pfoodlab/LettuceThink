use <xcarve-z-carriage.scad>
use <../Common/nema.scad>

module leadscrew(length)
{
        color("lightgray") {
                cylinder(r=4, h=length);
        }
}

module x_carriage(height, tool_length, z, invert)
{
        color("black") {
                // plates
                translate([0, 0, 0]) cube([150, 4, 140]);
                translate([0, 61, 0]) cube([150, 4, 140]);
                translate([0, 0, 120]) cube([150, 65, 4]);
        }

        translate([0, 0, 50]) {
                color("black") {
                        // z-axis makeslide 
                        translate([55, -20, -height])
                                cube([40, 20, height+140]);

                        // motor plate
                        translate([(150-57)/2, -40, 140])
                                cube([57, 97, 5]);
                }
                translate([75, -25, -height]) 
                        leadscrew(height+140+20);

                translate([57/2+(150-57)/2, 57/2, 140-45])
                        nema23_motor(45);
                *translate([5, -35, -z])
                        z_carriage(height, tool_length, invert);
        }
        
}

x_carriage(600, 200, 0, 0);

