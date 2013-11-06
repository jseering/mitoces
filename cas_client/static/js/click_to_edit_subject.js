$(function(){

    // === handle header edit === //
    var click_to_edit = true;
    $('#header.edit span#number').on('click',function(){
        if (!click_to_edit) return(false);
        var subject_number = $('#header.edit span#number').text();
        var subject_id = $(this).parent().attr('object_id');
        $(this).text("");
        $(this).append('<input type="text" name="subj_number" size="5" style="width:60px;" value="'+subject_number+'" maxlength="10">');
        click_to_edit = false;
        $("input[name='subj_number']").focus();
        $("input[name='subj_number']").on('blur',function() {
            if (($("input[name='subj_number']").val()=="")) {
                alert("The subject must have a number.");
                $("input[name='subj_number']").focus();
            } else if ($("input[name='subj_number']").val()==subject_number) { // header didn't change actually
                $('#header.edit span#number').text(subject_number);
            } else {
                // perform an AJAX post to change the name/header
                var newnumber = $("input[name='subj_number']").val();
                $.ajax({
                    type:"POST",
                    url:"/subjects/"+subject_id.toString()+"/editnumber/",
                    data:{
                        'newnumber': newnumber,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // if deletion successful, change the header
                            $('#header.edit span#number').text(newnumber);
                        } else { // deletion failed, turn header back to what it was originally
                            $('#header.edit span#number').text(subject_number);
                        }
                    },
                    dataType:'json'
                });
            }
            click_to_edit = true;
        });
    });

    // === handle header edit === //
    var click_to_edit = true;
    $('#header.edit span#name').on('click',function(){
        if (!click_to_edit) return(false);
        var subject_name = $('#header.edit span#name').text();
        var subject_id = $(this).parent().attr('object_id');
        $(this).text("");
        $(this).append('<input type="text" name="subj_name" size="5" style="width:420px;" value="'+subject_name+'" maxlength="60">');
        click_to_edit = false;
        $("input[name='subj_name']").focus();
        $("input[name='subj_name']").on('blur',function() {
            if (($("input[name='subj_name']").val()=="")) {
                alert("The subject must have a name.");
                $("input[name='subj_name']").focus();
            } else if ($("input[name='subj_name']").val()==subject_name) { // header didn't change actually
                $('#header.edit span#name').text(subject_name);
            } else {
                // perform an AJAX post to change the name/header
                var newname = $("input[name='subj_name']").val();
                $.ajax({
                    type:"POST",
                    url:"/subjects/"+subject_id.toString()+"/editname/",
                    data:{
                        'newname': newname,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // if deletion successful, change the header
                            $('#header.edit span#name').text(newname);
                        } else { // deletion failed, turn header back to what it was originally
                            $('#header.edit span#name').text(subject_name);
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


