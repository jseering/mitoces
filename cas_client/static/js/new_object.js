$(function(){

    // === handle new object creation === //
    $('a[link_type="new"]').click(function(){
        var object_type = $(this).attr('object_type');
        var win = window.open("/"+object_type+"s/add/", "Add " + object_type, 'height=500,width=800,resizable=yes,scrollbars=yes');
    });    

});



