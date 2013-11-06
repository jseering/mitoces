$(function(){

    // === handle switching between adding new subject and selecting from existing === //
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

    // === when the existing subject is selected, display its title and description for review before saving === //
    var prereq_id;
    $(document).on('change', 'select#subject_list', function(e) {
        prereq_id = $('select#subject_list :selected').attr('subject_id');
        // perform an ajax call to get the description
        $.ajax({
            type:"POST",
            url:"/subjects/"+prereq_id+"/get/description/",
            data:{
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(jsondata) {
                var returned_data = jsondata;
                if (returned_data.result=="succeeded") { // success 
                    // make the info visible and populate it
                    $('p#name').text(returned_data.name);
                    var description = returned_data.description;
                    $('p#description').text(description);
                } else { // failed
                    // do nothing
                }
            },
            dataType:'json'
        });
    });

    // === handle save subject click === //
    $('button#save').click(function() {
        if ($('button#create_new').attr('disabled')=="disabled"){
            // check to make sure there is a title and description
            if ($('input#id_name').val()=="") {
                alert('Please title your new subject.');
                $('input#id_name').focus();
                return false;
            }   
            if ($('textarea#id_description').val()=="") {
                alert('Please give your new subject a description.');
                $('textarea#id_description').focus();
                return false;
            }   
            // do an ajax post to add the subject
            var subject_id = $('h1#header').attr('subject_id');
            var prereq_number = $('input#id_number').val();
            var prereq_name = $('input#id_name').val();  
            var prereq_description = $('textarea#id_description').val();
            var prereq_creator_id = $('select#id_creator option').attr('value');
            $.ajax({
                type:"POST",
                url:"/subjects/"+subject_id+"/add/subject/",
                data:{
                    'subject_id': subject_id,
                    'prereq_number': prereq_number,
                    'prereq_name': prereq_name,
                    'prereq_description': prereq_description,
                    'prereq_creator_id': prereq_creator_id,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(jsondata) {
                    var returned_data = jsondata;
                    if (returned_data.result=="succeeded") { // success 
                        // close the pop up and send the main window to the new subject
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
            if (prereq_id) {
                // do an ajax post to add the subject
                var subject_id = $('h1#header').attr('subject_id');
                $.ajax({
                    type:"POST",
                    url:"/subjects/"+subject_id+"/add/subject/"+prereq_id+"/",
                    data:{
                        'subject_id': subject_id,
                        'prereq_id': prereq_id,
                        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                    },
                    success: function(jsondata) {
                        var returned_data = jsondata;
                        if (returned_data.result=="succeeded") { // success 
                            // close the pop up and send the main window to the new subject
                            window.close();
                            window.opener.location.href="/subjects/" + subject_id + "/edit/";
                        } else { // creation failed
                            // do nothing
                        }
                    },
                    dataType:'json'
                });
            } else {
                alert('Please select an subject from the dropdown list.');
            }
        }
    });
   
});

