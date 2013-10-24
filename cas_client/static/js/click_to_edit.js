$(function(){

    // === handle header edit === //
    var click_to_edit = true;
    $('#header.edit').on('click',function(){
        if (!click_to_edit) return(false);
        var front_matter = getFrontMatter($(this).text());
        var curr_header = stripFrontMatter($(this).text());
        var object_class = $(this).attr('object_type');
        var object_id = $(this).attr('object_id');
        $(this).text(front_matter + ": ");
        $(this).append('<input type="text" name="header" size="40" style="width:360px;" value="'+curr_header+'">');
        click_to_edit = false;
        $("input[name='header']").focus();
        $("input[name='header']").on('blur',function() {
            if ($(this).val()=="") {
                alert("The " + front_matter + " must have a name.");
                $(this).focus();
            } else if ($(this).val()==curr_header) { // header didn't change actually
                $('#header.edit').text(front_matter + ": " + $(this).val());
            } else {
                // perform an AJAX post to change the name/header
                var newname = $(this).val();
                $.ajax({
                    type:"POST",
                    url:"/"+object_class+"s/"+object_id.toString()+"/editname/",
                    data:{
                        'newname': newname,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // if deletion successful, change the header
                            $('#header.edit').text(front_matter + ": " + newname);
                        } else { // deletion failed, turn header back to what it was originally
                            $('#header.edit').text(front_matter + ": " + curr_header);
                        }
                    },
                    dataType:'json'
                });
            }
            click_to_edit = true;
        });
    });

    // === handle description edit === //
    var click_to_edit = true;
    $('#description.edit').on('click',function(){
        if (!click_to_edit) return(false);
        var curr_desc = $(this).text();
        var object_class = $(this).attr('object_type');
        var object_id = $(this).attr('object_id');
        // get the current size of the <p> element to set size of textarea appropriately
        var p_width = $(this).width();
        var p_height = $(this).height();
        $(this).after('<textarea id="description" style="width:' + Math.floor(0.95*p_width) + 'px;max-width:' + Math.floor(0.95*p_width) + 'px;height:'+Math.floor(1.05*p_height)+'px;">'+curr_desc+'</textarea>');
        $(this).hide();
        click_to_edit = false;
        $("textarea#description").focus();
        $("textarea#description").on('blur',function() {
            if ($(this).val()=="") {
                alert("There must be a description for the " + object_class + ".");
                $(this).focus();
            } else if ($(this).val()==curr_desc) { // header didn't change actually
                $('#description.edit').show();
                $(this).remove();
            } else {
                // perform an AJAX post to change the name/header
                var newdescription = $(this).val();
                $.ajax({
                    type:"POST",
                    url:"/"+object_class+"s/"+object_id.toString()+"/editdescription/",
                    data:{
                        'newdescription': newdescription,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // if deletion successful, change the paragraph and remove the textarea
                            $('#description.edit').show();
                            $('#description.edit').text(newdescription);
                            $("textarea#description").remove();
                        } else { // deletion failed, turn description back to what it was originally by just showing it
                            $('#description.edit').show();
                            $("textarea#description").remove();
                        }
                    },
                    dataType:'json'
                });
            }
            click_to_edit = true;
        });
    });
});



// === HELPER FUNCTIONS === //

function stripFrontMatter(str){
    var colonIndex = str.indexOf(": ");
    var str = str.substring(colonIndex+2); // take the part after the space
    return str;
}

function getFrontMatter(str){
    var colonIndex = str.indexOf(": ");
    var str = str.substring(0,colonIndex); // take the part up to and including the colon and space
    return str;
}


