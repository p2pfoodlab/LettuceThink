use <emergencystop.scad>

module box(depth, width, height, d)
{
        translate([0, width, 0])
        rotate([0, 0,180]) {
                color([200/255, 151/255, 95/255]) {
                        // bottom
                        cube([depth, width, d]);
                        echo("Box, : ", depth, "x", width);

                        // top
                        translate([0, 0, height+10])
                                cube([depth, width, d]);

                        echo("Box, : ", depth, "x", width);
                        
                        // left
                        translate([30, 0, 10])
                                cube([depth-2*30, d, height]);
                        echo("Box, : ", depth-2*30, "x", height);
                        
                        // right
                        translate([30, width-d, 10])
                                cube([depth-2*30, d, height]);
                        echo("Box, : ", depth-2*30, "x", height);

                        // back
                        translate([30, 10, 10])
                                cube([d, width - 2 * d, height]);
                        echo("Box, : ", width - 2 * d, "x", height);

                        // front
                        translate([depth-30-10, d, d])
                                cube([d, width - 2 * d, height]);                
                        echo("Box, : ", width - 2 * d, "x", height);

                }
                translate([30, 100, height/2])
                        rotate([0, -90, 0])
                        emergencystop2();

                translate([30, width-100, height/2])
                        rotate([0, -90, 0])
                        emergencystop2();
        }
}

box(320, 1000, 260, 10);
