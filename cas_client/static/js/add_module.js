$(function(){

    // === handle save module click === //
    $('button#save').click(function() {
        // check to make sure there is a title and description
        if ($('input#id_name').val()=="") {
            alert('Please title your new module.');
            $('input#id_name').focus();
            return false;
        }   
        if ($('textarea#id_description').val()=="") {
            alert('Please give your new module a description.');
            $('textarea#id_description').focus();
            return false;
        }   
        // do an ajax post to create the new module
        var module_name = $('input#id_name').val();  
        var module_description = $('textarea#id_description').val();
        var module_creator_id = $('select#id_creator option').attr('value');
        $.ajax({
            type:"POST",
            url:"/modules/add/",
            data:{
                'module_name': module_name,
                'module_description': module_description,
                'module_creator_id': module_creator_id,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    var new_module_id = returned_data.new_module_id;
                    // close the pop up and send the main window to the new module
                    window.close();
                    window.opener.location.href="/modules/" + new_module_id + "/edit/";
                } else { // creation failed
                    // do nothing
                }
            },
            dataType:'json'
        });
        
    });
   
});

