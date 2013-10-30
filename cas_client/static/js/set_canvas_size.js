$(function(){

    // === set canvas size to take up remainder of screen === //
    var ctx = $('canvas#viewport');
    var width_percent = ctx.attr('width_percent');
    var width_adj = 0.95;
    var height_adj = 0.9;
    var canvas_width = width_adj*(width_percent/100.0)*window.innerWidth;
    var canvas_height = height_adj*window.innerHeight;
    /*
    ctx.width  = (width_percent/100.0)*window.innerWidth;
    ctx.height = window.innerHeight;
    */

   
    $('canvas#viewport').attr('width',canvas_width.toString()+"px").attr('height',canvas_height.toString()+"px");

});

