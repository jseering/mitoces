$(function(){

    // === handle switching between adding new outcome and selecting from existing === //
    $('button#create_new').click(function() {
        $('div.existing').css('display','none');
        $('div.new').css('display','block');
        $(this).attr('disabled','disabled');
        $('button#existing').removeAttr('disabled');
    });
    $('button#existing').click(function() {
        $('div.new').css('display','none');
        $('div.existing').css('display','block');
        $(this).attr('disabled','disabled');
        $('button#create_new').removeAttr('disabled');
    });

    // === when the existing outcome is selected, display its title and description for review before saving === //
    var module_id;
    $(document).on('change', 'select#module_list', function(e) {
        var module_name = this.options[e.target.selectedIndex].text;
        module_id = $('select#module_list option[value="'+module_name+'"]').attr('module_id');
        // perform an ajax call to get the description
        $.ajax({
            type:"POST",
            url:"/modules/"+module_id+"/get/description/",
            data:{
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    // make the info visible and populate it
                    $('p#name').text(module_name);
                    var description = returned_data.description;
                    $('p#description').text(description);
                } else { // failed
                    // do nothing
                }
            },
            dataType:'json'
        });
    });

    // === handle save module click === //
    $('button#save').click(function() {
        if ($('button#create_new').attr('disabled')=="disabled"){
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
            // do an ajax post to add the outcome
            var subject_id = $('h1#header').attr('subject_id');
            var module_name = $('input#id_name').val();  
            var module_description = $('textarea#id_description').val();
            var module_creator_id = $('select#id_creator option').attr('value');
            $.ajax({
                type:"POST",
                url:"/subjects/"+subject_id+"/add/module/",
                data:{
                    'subject_id': subject_id,
                    'module_name': module_name,
                    'module_description': module_description,
                    'module_creator_id': module_creator_id,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(jsondata) {
                    var returned_data = jsondata;
                    if (returned_data.result=="succeeded") { // success 
                        // close the pop up and send the main window to the new module
                        window.close();
                        window.opener.location.href="/subjects/" + subject_id + "/edit/";
                    } else { // creation failed
                        // do nothing
                    }
                },
                dataType:'json'
            });
        } else { // selected from existing
            // check to make sure there is something selected
            if (module_id) {
                // do an ajax post to add the outcome
                var subject_id = $('h1#header').attr('subject_id');
                $.ajax({
                    type:"POST",
                    url:"/subjects/"+subject_id+"/add/module/"+module_id+"/",
                    data:{
                        'module_id': module_id,
                        'subject_id': subject_id,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // close the pop up and send the main window to the new module
                            window.close();
                            window.opener.location.href="/subjects/" + subject_id + "/edit/";
                        } else { // creation failed
                            // do nothing
                        }
                    },
                    dataType:'json'
                });
            } else {
                alert('Please select a module from the dropdown list.');
            }
        }
    });
   
});

