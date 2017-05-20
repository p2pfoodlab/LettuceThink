
module ring()
{
        translate([0, 0, -35]) // center
        color("red") {
                
                difference() {
                        union() {
                                cylinder(r=50, h=70);
                                // straight extensions tangent to round border  
                                translate([0, -50, 0])
                                        cube([50, 100, 70]);
                                // fixation block
                                translate([30, -80, 0])
                                        cube([50, 160, 70]);
                                // extension for the thightening screw
                                translate([-50, 2, 25])
                                        cube([20, 37.5, 20]);
                                
                                translate([-50, -2-37.5, 25])
                                        cube([20, 37.5, 20]);
                        }
                        // center hole
                        translate([0, 0, -1])
                                cylinder(r=30, h=72);
                        // cut-out for fixation block
                        translate([50, -81, 20])
                                cube([31, 162, 30]);

                        // vertical fixtion screw
                        translate([65, 0, -1])
                                cylinder(r=4, h=72);

                        // two horizontal fixtion screw
                        translate([30, 65, 35])
                                rotate([0, 90, 0])
                                translate([0, 0, -1])
                                cylinder(r=4, h=22);
                        translate([30, -65, 35])
                                rotate([0, 90, 0])
                                translate([0, 0, -1])
                                cylinder(r=4, h=22);

                        // opening for thightening
                        translate([-51, -2, -1])
                                cube([22, 4, 72]);

                        // opening for thightening screw
                        translate([-40, 40, 35])
                                rotate([90, 0, 0])
                                translate([0, 0, -1])
                                cylinder(r=3.5, h=82);
                }
        }
}

module ring2()
{
        translate([-50, -50, -15]) // center
        color("lightgray") {
                difference() {
                        translate([0, 0, 0])
                                cube([100, 100, 30]);
                        // center hole
                        translate([50, 50, -1])
                                cylinder(r=30, h=52);
                        // slit
                        translate([48, -1, -1])
                                cube([4, 102, 32]);
                        // hole for thightening screws
                        translate([-1, 10, 15])
                                rotate([0, 90, 0])
                                cylinder(r=4, h=102);
                        translate([-1, 90, 15])
                                rotate([0, 90, 0])
                                cylinder(r=4, h=102);
                }
        }        
}

*ring();

ring2();




