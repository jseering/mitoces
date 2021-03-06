$(function(){

    // === handle delete button click === //
    $('button.delete').click(function(){
        // get the header text
        var header_text = $('h4#header').text();
        var r=confirm('Are you sure you want to delete "'+header_text+'"?');
        if (r==true) { // confirmed deletion
            // get class/id of object we are deleting
            var object_class = getLastWord($(this).text());
            var object_id = $(this).attr('object_id');  
            // make an ajax post to the corresponding url
            $.ajax({
                type:"POST",
                url:"/"+object_class+"s/"+object_id.toString()+"/delete/",
                data:{
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(jsondata) {
                    var returned_data = jsondata;
                    if (returned_data.result=="succeeded") { // success 
                        // if deletion successful, redirect to "/"
                        window.location.href = "/";
                    } else { // deletion failed
                        // don't do anything
                    }
                },
                dataType:'json'
            });
        } // end if true
    }); // end delete button click

    // === handle red-x click === //
    $('img.delete').click(function(){
        // get the class and id of current page 
        var object_class = $('h4#header').attr('object_type');
        var object_id = $('h4#header').attr('object_id');
        // get the list item object type and id
        var lielem = $(this).parent();
        var remove_class = lielem.attr('object_type');
        var remove_id = lielem.attr('object_id');
        // make an ajax post to the corresponding url
        $.ajax({
            type:"POST",
            url:"/"+object_class+"s/"+object_id.toString()+"/remove/"+remove_class+"/"+remove_id.toString()+"/",
            data:{
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    // if deletion successful, remove the parent li element
                    lielem.remove();
                } else { // deletion failed
                    // don't do anything
                }
            },
            dataType:'json'
        });
    }); // end red-x click 

});

// === HELPER FUNCTIONS === //
function getLastWord(str) {
    var lastIndex = str.lastIndexOf(" ");
    var str = str.substring(lastIndex+1);
    return str;
}
