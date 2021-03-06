$(function(){

    // === get the selected instructor as it changes === //
    var subject_id;
    $(document).on('change', 'select#subject_list', function(e) {
        subject_id = $('select#subject_list :selected').attr('subject_id');
    });

    // === handle save module click === //
    $('button#save').click(function() {
        if (subject_id) {
           // do an ajax post to add the instructor
            var module_id = $('h1#header').attr('module_id');
            $.ajax({
                type:"POST",
                url:"/modules/"+module_id+"/add/subject/",
                data:{
                    'module_id': module_id,
                    'subject_id': subject_id,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(jsondata) {
                    var returned_data = jsondata;
                    if (returned_data.result=="succeeded") { // success 
                        // close the pop up and send the main window to the edited module
                        window.close();
                        window.opener.location.href="/modules/" + module_id + "/edit/";
                    } else { // creation failed
                        // do nothing
                    }
                },
                dataType:'json'
            });
        } else {
            alert('Please select a subject from the dropdown list.');
        }
    });
   
});

