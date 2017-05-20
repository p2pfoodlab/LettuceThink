use <xcarve-vwheel.scad>

module weedingtool(length)
{
        color("yellow") {
                translate([-50, -100, -50])
                cube([100, 100, 100]);
        }
        color("grey") {
                translate([0, -50, -length-50])
                cylinder(r=16, h=length);
        }
}

module z_carriage(height, tool_length, invert)
{
        translate([70, 0, 70]) 
                rotate([0, invert? 180 : 0, 0])
                weedingtool(tool_length);
        color("black") {
                cube([140, 4, 140]);
        }
        translate([40, 4, 20]) 
                rotate([-90, 0, 0])
                vwheel(10);
        translate([40, 4, 120]) 
                rotate([-90, 0, 0])
                vwheel(10);
        translate([140-40, 4, 20]) 
                rotate([-90, 0, 0])
                vwheel(10);
        translate([140-40, 4, 120]) 
                rotate([-90, 0, 0])
                vwheel(10);
}

z_carriage(600, 600);