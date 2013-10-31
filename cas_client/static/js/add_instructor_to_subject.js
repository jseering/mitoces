$(function(){

    // === get the selected instructor as it changes === //
    var instructor_id;
    $(document).on('change', 'select#instructor_list', function(e) {
        var instructor_name = this.options[e.target.selectedIndex].text;
        instructor_id = $('select#instructor_list option[value="'+instructor_name+'"]').attr('user_id');
    });

    // === handle save module click === //
    $('button#save').click(function() {
        if (instructor_id) {
           // do an ajax post to add the instructor
            var subject_id = $('h1#header').attr('subject_id');
            $.ajax({
                type:"POST",
                url:"/subjects/"+subject_id+"/add/instructor/",
                data:{
                    'subject_id': subject_id,
                    'instructor_id': instructor_id,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(jsondata) {
                    var returned_data = jsondata;
                    if (returned_data.result=="succeeded") { // success 
                        // close the pop up and send the main window to the edited module
                        window.close();
                        window.opener.location.href="/subjects/" + subject_id + "/edit/";
                    } else { // creation failed
                        // do nothing
                    }
                },
                dataType:'json'
            });
        } else {
            alert('Please select an instructor from the dropdown list.');
        }
    });
   
});

