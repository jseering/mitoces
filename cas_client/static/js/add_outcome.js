$(function(){

    // === handle save module click === //
    $('button#save').click(function() {
        // check to make sure there is a title and description
        if ($('input#id_name').val()=="") {
            alert('Please title your new outcome.');
            $('input#id_name').focus();
            return false;
        }   
        if ($('textarea#id_description').val()=="") {
            alert('Please give your new outcome a description.');
            $('textarea#id_description').focus();
            return false;
        }   
        // do an ajax post to create the new module
        var module_id = $('h1#header').attr('module_id');
        var outcome_name = $('input#id_name').val();  
        var outcome_description = $('textarea#id_description').val();
        var outcome_creator_id = $('select#id_creator option').attr('value');
        $.ajax({
            type:"POST",
            url:"/modules/"+module_id+"/add/outcome/",
            data:{
                'module_id': module_id,
                'outcome_name': outcome_name,
                'outcome_description': outcome_description,
                'outcome_creator_id': outcome_creator_id,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    // close the pop up and send the main window to the new module
                    window.close();
                    window.opener.location.href="/modules/" + module_id + "/edit/";
                } else { // creation failed
                    // do nothing
                }
            },
            dataType:'json'
        });
        
    });
   
});

