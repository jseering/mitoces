$(function(){

    // === handle header edit === //
    $('#header.edit').focus(function(){
        alert("hello");
        $(this).text('Outcome: ');
        $(this).append('<input type="text" name="header" size="40" style="width:360px;">');
    }).blur(function(){

    });

/*
$('.answerSpace').bind('blur', function(){ $('.normProf').removeClass("normProf").addClass('opacProf'); });
$('.answerSpace').bind('focus', function(){ $('.opacProf').removeClass("opacProf").addClass('normProf'); });
*/
/*
    $('#header.edit').toggle(
        function(){
            alert("clicked once");
        },
        function(){
            alert("clicked twice");
        }
    );
*/


/*
        // get tagname
        var id = $(this).attr('id');
        if (id=="header") { // header click
            alert('this class = ' + $(this).attr('class'));
            $(this).removeClass("edit");
            $(this).text('Outcome: ');
            $(this).append('<input type="text" name="header" size="40" style="width:360px;">');
        } else if (id=="description") { // description click

        }
    });
*/

});

