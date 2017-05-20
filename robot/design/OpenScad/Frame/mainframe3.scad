use <tubular.scad>;
use <box.scad>

module side_frames(length, height, clamp_interspacing, top_panel)
{
        translate([0, 0, 30])
                rotate([0, 0, 90])
                square_tube(length, 30);

        translate([0, 0, clamp_interspacing+30])
                rotate([0, 0, 90])
                square_tube(length, 30);

        echo("Main frame: 2x: ", length);

        if (top_panel) 
        translate([0, 60, height-60])
                rotate([0, 0, 90])
                square_tube(length, 30);

        echo("Main frame: 1x: ", length);
}

module cross_frames(width, height, clamp_interspacing, top_panel, box_width)
{
        // left-to-right, front
        translate([-30, 0, 0])
                square_tube(width, 30);

        translate([-30, 0, clamp_interspacing+60])
                square_tube(width, 30);

        echo("Main frame: 2x: ", width);

        if (top_panel) 
        translate([-30, 60, height-30])
                square_tube(width-120, 30);

        echo("Main frame: 1x: ", width-120);
        
        // left-to-right, back
        translate([-320, 0, 0])
                square_tube(width, 30);

        translate([-320, 0, clamp_interspacing+60])
                square_tube(width, 30);

        echo("Main frame: 2x: ", width);

        if (top_panel) 
        translate([-320, 30, height-30])
                square_tube(width-60, 30);

        echo("Main frame: 1x: ", width-60);

        h1 = clamp_interspacing+90;
        h2 = height;

        delta_box = (width - box_width) / 2;
                
        // top-down, left
        translate([-60, 30, h1])
                rotate([-90, 0, 0])
                square_tube(h1, 30);

        translate([-290, 30, top_panel? h2 : h1])
                rotate([-90, 0, 0])
                square_tube(top_panel? h2 : h1, 30);
        
        translate([-60, delta_box-30, h1])
                rotate([-90, 0, 0])
                square_tube(h1, 30);

        translate([-290, delta_box-30, h1])
                rotate([-90, 0, 0])
                square_tube(h1, 30);

        // top-down, right
        echo("Main frame, 3x: ", h1);
        echo("Main frame, 1x: ", h2);

        translate([-60, width-60, h1])
                rotate([-90, 0, 0])
                square_tube(h1, 30);

        translate([-290, width-60, top_panel? h2 : h1])
                rotate([-90, 0, 0])
                square_tube(top_panel? h2 : h1, 30);

        translate([-60, width-delta_box, h1])
                rotate([-90, 0, 0])
                square_tube(h1, 30);

        translate([-290, width-delta_box, h1])
                rotate([-90, 0, 0])
                square_tube(h1, 30);

        echo("Main frame, 3x: ", h1);
        echo("Main frame, 1x: ", h2);
}

module main_frame3(length, width, height, clamp_interspacing, top_panel)
{
        box_width = 600; //width - 2*60 - 2*100;

        translate([0, 0, 0])
                side_frames(length, height, clamp_interspacing, top_panel);

        translate([-length, width, 0])
                rotate([0, 0, 180])
                side_frames(length, height, clamp_interspacing, top_panel);

        translate([0, 0, 0])
                cross_frames(width, height, clamp_interspacing, top_panel, box_width);

        translate([-(length), width, 0])
                rotate([0, 0, 180])
                cross_frames(width, height, clamp_interspacing, top_panel, box_width);

        if (top_panel) 
        translate([-length/2, 60, height-30])
                square_tube(width-120, 30);
        
        echo("Main frame, 1x: ", width-120);

        h = clamp_interspacing + 90;
        translate([0, (width-box_width)/2, -10])
                box(320, box_width, h, 10);

        translate([-length, (width+box_width)/2, -10])
                rotate([0, 0, 180])
                box(320, box_width, h, 10);
}

main_frame3(1675, 1260, 800, 200, 1);
