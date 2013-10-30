$(function(){

    // === handle new object creation === //
    $('a[link_type="new"]').click(function(){
        var object_type = $(this).attr('object_type');
        var win = window.open("/"+object_type+"s/add/", "Add " + object_type, 'height=400,width=500,resizable=yes,scrollbars=yes');
    });    

    // === add object_type to parent_object_type === //
    $('img.add').click(function(){
        var parent_object_type = $('h4#header').attr('object_type');
        var parent_object_id = $('h4#header').attr('object_id');
        var this_object_type = getLastWord($(this).attr('title'));
        var win = window.open("/"+parent_object_type+"s/"+parent_object_id+"/add/"+this_object_type+"/", "Add " + this_object_type, 'height=400,width=500,resizable=yes,scrollbars=yes');
    });

});


// === HELPER FUNCTIONS === //
function getLastWord(str) {
    var lastIndex = str.lastIndexOf(" ");
    var str = str.substring(lastIndex+1);
    return str;
}
