use <../Common/tubular.scad>;

module connector_1()
{
        color("black") {
                difference() {
                        cylinder(r=13, h=20);
                        translate([0, 0, -1])
                                cylinder(r=6, h=22);
                }
        }
}

module roller_bearings()
{
        color("black") {
                difference() {
                        cylinder(r=28, h=14);
                        translate([0, 0, -1])
                                cylinder(r=15, h=16);
                }
        }
}

module wheelfork(wheel_radius, axis_width, height, clamp_interspacing)
{
        height_fork = (wheel_radius - 20) + 30 + 30 + 30 + 30;

        // flat plates to fix wheel
        color("gray") {
                translate([-15, axis_width/2, -20])
                        cube([30, 2, 140]);
                translate([-15, -axis_width/2-4, -20])
                        cube([30, 2, 140]);
        }

        // fork: top-down elements
        translate([-15, 30+axis_width/2+4, 20])
                rotate([90, 0, 0])
                square_tube(height_fork, 30);
                
        translate([-15, -axis_width/2-4, 20])
                rotate([90, 0, 0])
                square_tube(height_fork, 30);
                
        width_fork_outside = axis_width + 2 * 2 + 2 * 30;

        echo("Fork vertical length: ", height_fork);
        echo("Fork width: ", width_fork_outside);

        
        // fork
        // left-right elements
        translate([15, -width_fork_outside/2, 20+height_fork-30])
                square_tube(width_fork_outside, 30);

        translate([-45, -width_fork_outside/2, 20+height_fork-30])
                square_tube(width_fork_outside, 30);


        translate([15, -width_fork_outside/2, 20+height_fork-90])
                square_tube(width_fork_outside, 30);

        translate([-45, -width_fork_outside/2, 20+height_fork-90])
                square_tube(width_fork_outside, 30);

        // Calcuate the height of various elements:
        z_start_inner_tube = 20 + height_fork - 90;
        z_bottom_clamp = height + 30; // +30: bottom tube main frame
        z_top_clamp = z_bottom_clamp + clamp_interspacing;
        z_end_inner_tube = z_top_clamp - 8;
        height_inner_tube = z_end_inner_tube - z_start_inner_tube;

        echo("Height inner tube: ", height_inner_tube);
        
        // inner tube for steering
        translate([0, 0, z_start_inner_tube])
                round_tube(30, height_inner_tube);

        // roller bearings
        translate([0, 0, z_start_inner_tube + 90 + 10])
                roller_bearings();

        // connector to fix the stepper to the inner tube 
        translate([0, 0, z_end_inner_tube-20])
                connector_1();
}

wheelfork(160, 110, 800, 100);
