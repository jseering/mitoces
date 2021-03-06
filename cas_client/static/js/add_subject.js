$(function(){

    // === handle save module click === //
    $('button#save').click(function() {
        // check to make sure there is a title and description
        if ($('input#id_name').val()=="") {
            alert('Please title your new subject.');
            $('input#id_name').focus();
            return false;
        }   
        if ($('input#id_number').val()=="") {
            alert('Please give your new subject a number.');
            $('input#id_number').focus();
            return false;
        }
        if ($('textarea#id_description').val()=="") {
            alert('Please give your new subject a description.');
            $('textarea#id_description').focus();
            return false;
        }   
        // do an ajax post to create the new module
        var subject_number = $('input#id_number').val();
        var subject_name = $('input#id_name').val();  
        var subject_description = $('textarea#id_description').val();
        var subject_creator_id = $('select#id_creator option').attr('value');
        $.ajax({
            type:"POST",
            url:"/subjects/add/",
            data:{
                'subject_number': subject_number,
                'subject_name': subject_name,
                'subject_description': subject_description,
                'subject_creator_id': subject_creator_id,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    var new_subject_id = returned_data.new_subject_id;
                    // close the pop up and send the main window to the new module
                    window.close();
                    window.opener.location.href="/subjects/" + new_subject_id + "/edit/";
                } else { // creation failed
                    // do nothing
                }
            },
            dataType:'json'
        });
        
    });
   
});

