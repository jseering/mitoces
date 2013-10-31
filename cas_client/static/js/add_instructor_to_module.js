$(function(){

    // === get the selected instructor as it changes === //
    var instructor_id;
    var all_dep_outcome_bool = 0;
    $(document).on('change', 'select#instructor_list', function(e) {
        var instructor_name = this.options[e.target.selectedIndex].text;
        instructor_id = $('select#instructor_list option[value="'+instructor_name+'"]').attr('user_id');
    });
    /*
    $(document).on('change', 'input[type="checkbox"]', function(e) {
        if (this.is(':checked')) {
            all_dep_outcome_bool = 1;
        } else {
            all_dep_outcome_bool = 0;    
        }
    }); 
    */

    // === handle save module click === //
    $('button#save').click(function() {
        if ($('input[type="checkbox"]').prop('checked')) {
            all_dep_outcome_bool = 1;
        } else {
            all_dep_outcome_bool = 0;
        }
        if (instructor_id) {
           // do an ajax post to add the instructor
            var module_id = $('h1#header').attr('module_id');
            $.ajax({
                type:"POST",
                url:"/modules/"+module_id+"/add/instructor/",
                data:{
                    'module_id': module_id,
                    'instructor_id': instructor_id,
                    'incl_on_outcomes': all_dep_outcome_bool,
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
            alert('Please select an instructor from the dropdown list.');
        }
    });
   
});

