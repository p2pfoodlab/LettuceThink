
module square_tube(len, L)
{
        difference() {
                color("lightgray")
                        cube([L, len,  L]);
                translate([2, -1, 2])
                        color("lightgray")
                        cube([L-4, len+2,  L-4]);
        }
}

module cube_connector(L)
{
    color("gray")
        cube([L, L,  L]);    
}

module round_tube(d, L)
{
        color("lightgray") {
                difference() {
                        cylinder(r=d/2, h=L);
                        translate([0, 0, -1])
                                cylinder(r=d/2-2, h=L+2);
                }
        }
}
