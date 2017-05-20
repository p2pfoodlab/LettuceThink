
module emergencystop()
{
        color("yellow") cube([68, 68, 53]);
        color("red") translate([34, 34, 53]) cylinder(r=15, h=92-53-10);
        color("red") translate([34, 34, 82]) cylinder(r=20, h=10);
}


module emergencystop2()
{
        color("yellow") cylinder(r=34, h=1);
        color("red") translate([0, 0, 1]) cylinder(r=15, h=30);
        color("red") translate([0, 0, 30]) cylinder(r=20, h=10);
}

emergencystop2();
