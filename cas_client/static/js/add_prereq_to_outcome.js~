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
    var prereq_id;
    $(document).on('change', 'select#outcome_list', function(e) {
        var prereq_name = this.options[e.target.selectedIndex].text;
        prereq_id = $('select#outcome_list option[value="'+prereq_name+'"]').attr('outcome_id');
        // perform an ajax call to get the description
        $.ajax({
            type:"POST",
            url:"/outcomes/"+prereq_id+"/get/description/",
            data:{
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    // make the info visible and populate it
                    $('p#name').text(prereq_name);
                    var description = returned_data.description;
                    $('p#description').text(description);
                } else { // failed
                    // do nothing
                }
            },
            dataType:'json'
        });
    });

    // === handle save outcome click === //
    $('button#save').click(function() {
        if ($('button#create_new').attr('disabled')=="disabled"){
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
            // do an ajax post to add the outcome
            var outcome_id = $('h1#header').attr('outcome_id');
            var prereq_name = $('input#id_name').val();  
            var prereq_description = $('textarea#id_description').val();
            var prereq_creator_id = $('select#id_creator option').attr('value');
            $.ajax({
                type:"POST",
                url:"/outcomes/"+outcome_id+"/add/outcome/",
                data:{
                    'outcome_id': outcome_id,
                    'prereq_name': prereq_name,
                    'prereq_description': prereq_description,
                    'prereq_creator_id': prereq_creator_id,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(jsondata) {
                    var returned_data = jsondata;
                    if (returned_data.result=="succeeded") { // success 
                        // close the pop up and send the main window to the new outcome
                        window.close();
                        window.opener.location.href="/outcomes/" + outcome_id + "/edit/";
                    } else { // creation failed
                        // do nothing
                    }
                },
                dataType:'json'
            });
        } else { // selected from existing
            // check to make sure there is something selected
            if (prereq_id) {
                // do an ajax post to add the outcome
                var outcome_id = $('h1#header').attr('outcome_id');
                $.ajax({
                    type:"POST",
                    url:"/outcomes/"+outcome_id+"/add/outcome/"+prereq_id+"/",
                    data:{
                        'outcome_id': outcome_id,
                        'prereq_id': prereq_id,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // close the pop up and send the main window to the new outcome
                            window.close();
                            window.opener.location.href="/outcomes/" + outcome_id + "/edit/";
                        } else { // creation failed
                            // do nothing
                        }
                    },
                    dataType:'json'
                });
            } else {
                alert('Please select an outcome from the dropdown list.');
            }
        }
    });
   
});

