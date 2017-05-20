use <wheel.scad>;
use <wheelfork.scad>;
use <wheelcolumn.scad>;

module wheelmodule(height, wheel_radius, axis_width, clamp_interspacing)
{
        *translate([0, 0, wheel_radius])
                wheel(wheel_radius, 50, axis_width); // the wheel axis is at z=0
        
        *translate([0, 0, wheel_radius]) // the wheel axis is at z=0
                wheelfork(wheel_radius, axis_width, height, clamp_interspacing);        

        wheelcolumn(wheel_radius, height, clamp_interspacing);
}

wheelmodule(800, 160, 110, 100);



