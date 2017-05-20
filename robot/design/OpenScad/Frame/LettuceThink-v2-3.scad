use <mainframe3.scad>;
use <wheelmodule.scad>;
use <solarpanel.scad>;
use <../Xcarve/xcarve.scad>

length = 1675;
width = 1260;
wheel_height = 600;
wheel_radius = 160;
axis_width = 110;
clamp_interspacing = 200;
height = wheel_height + clamp_interspacing;
top_panel = 1;

rotate([0, 0, 3600*$t]) {
    translate([length/2, -width/2, 0]) {
        
        translate([0, 0, wheel_height])
                main_frame3(length, width, height, clamp_interspacing, top_panel);

        // front-left wheel
        translate([-160, 80, 0])
                wheelmodule(wheel_height, wheel_radius, axis_width, clamp_interspacing);

        // back-left wheel
        translate([-(length-160), 80, 0])
                wheelmodule(wheel_height, wheel_radius, axis_width, clamp_interspacing);

        // front-right wheel
        translate([-160, width-80, 0])
                rotate([0, 0, 180])
                wheelmodule(wheel_height, wheel_radius, axis_width, clamp_interspacing);

        // back-right wheel
        translate([-(length-160), width-80, 0])
                rotate([0, 0, 180])
                wheelmodule(wheel_height, wheel_radius, axis_width, clamp_interspacing);

        deltax = 320 + (length - 2 * 320 - 1000) / 2;
        deltay = (width - 1000) / 2;
        translate([-deltax, deltay, wheel_height + 60 + clamp_interspacing + 5])
                rotate([0, 0, 90]) 
                xcarve_upside_down(1000, 1000, wheel_height, wheel_height, 500, 500, 600);

        if (top_panel) {
                translate([-1675+(1675-length)/2, (width-1001)/2, wheel_height + height])
                        solarpanel_sunmodule_protect_SW250_mono_black();
        } 
    }
}