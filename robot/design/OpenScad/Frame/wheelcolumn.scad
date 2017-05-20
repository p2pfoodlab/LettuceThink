use <../Common/tubular.scad>;
use <../Common/nema.scad>;
use <ring.scad>;

module top_cover()
{
        color("gray") 
                difference() {
                cylinder(r=50, h=140);
                translate([0, 0, -1]) cylinder(r=47, h=138);
        }
}

module wheelcolumn(wheel_radius, height, clamp_interspacing)
{
        // Calcuate the height of various elements:
        height_fork = (wheel_radius - 20) + 30 + 30 + 30 + 30;
        z_start_inner_tube = wheel_radius + 20 + height_fork - 90;
        z_bottom_clamp = height + 30; // +30: bottom tube main frame
        z_top_clamp = z_bottom_clamp + clamp_interspacing;
        z_end_inner_tube = z_top_clamp - 8;
        z_start_outer_tube = z_start_inner_tube + 90 + 10;
        z_end_outer_tube = z_top_clamp + 48;
        height_outer_tube = z_end_outer_tube - z_start_outer_tube;

        // stepper
        translate([0, 0, z_end_inner_tube-20])
                nema23_phidget_3332_0();

        echo("Height outer tube: ", height_outer_tube);

        // outer tube
        translate([0, 0, z_start_outer_tube])
                round_tube(60, height_outer_tube);

        // clamps/rings
        translate([0, 0, z_bottom_clamp+15]) // 15: the clamp is centered along z
                rotate([0, 0, -90])
                ring2();
        translate([0, 0, z_top_clamp+15]) // 15: the clamp is centered along z
                rotate([0, 0, -90])
                ring2();

        translate([0, 0, z_top_clamp + 30])
                top_cover();
}

wheelcolumn(160, 800, 100);







