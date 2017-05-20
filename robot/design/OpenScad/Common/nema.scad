
module nema_motor(w, d, length)
{
        color("black") {
                translate([-w/2, -w/2, 0])
                        cube([w, w, length]);
        }
        color("lightgray") {
                cylinder(r=d, h=length+20);
        }
}

module nema23_motor(length)
{
        nema_motor(57, 6, length);
}

function nema34_dim() = 85.85;

module nema34_motor(length)
{
        nema_motor(nema34_dim(), 7, length);
}

function nema42_dim() = 110;

module nema42_motor(length)
{
        nema_motor(110, 8.5, length);
}

module nema23_phidget_3332_0()
{
        color("black") {
                translate([-57/2, -57/2, 48+28])
                        cube([57, 57, 56]);
                translate([0, 0, 28])
                    cylinder(r=26, h=48);
        }
        color("lightgray") {
                cylinder(r=6, h=26);
                translate([0, 0, 26])
                    cylinder(r=16, h=2);
        }        
}
