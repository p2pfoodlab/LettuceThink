

module solarpanel_sunmodule_protect_SW250_mono_black()
{
        //1675 x 1001 x 33 mm
        color("lightgray") {
                cube([1675, 20,  33]);
                translate([0, 1001-20, 0])
                        cube([1675, 20,  33]);
                cube([20, 1001,  33]);
                translate([1675-20, 0, 0])
                        cube([20, 1001,  33]);
        }
        color([1, 1, 1, 1]) {
                translate([20, 20, 18])
                        cube([1675-2*20, 1001-2*20,  12]);
        }
        color("black") {
                w = 158;
                d = 15;
                for (x = [0 : 9]) {
                        for (y = [0 : 5]) {
                                translate([34 + x*160, 22 + y*160, 31])
                                polygon([[d,0],[w-d,0],[w,d],[w,w-d],[w-d,w],[d,w],[0,w-d],[0,d],[d,0]]);
                        }
                }
        }
}

solarpanel_sunmodule_protect_SW250_mono_black();
