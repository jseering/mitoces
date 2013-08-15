$(function(){
    $('[id^=delete_module_]').click(function() {
        // click to delete a module
        var idstr = $(this).attr('id');
        var module_num_str = idstr.substring(14);
        var module_id = parseInt(module_num_str);
        var module_name = $('#module_name').text();
        var result = confirm('Are you sure you want to delete the module "' + module_name + '"?');
        if (result == true) {
            // perform an ajax post to delete the module
            $.ajax({
                type: "POST",
                url: "/module/delete/",
                data: {
                    'module_id': module_id,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: deletionSuccess, 
                datatype: 'html'
            });
        } else {
            return false;
        }
    });
});

function deletionSuccess(data,textStatus,jqXHR) {
    document.location.href = "/modules/";
}

$(function(){
    $('#exploresearch').keyup(function(){
        $.ajax({
            type:"POST",
            url:"/exploresearch/",
            data:{
                'search_text':$('#exploresearch').val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: exploreSearchSuccess,
            dataType:'html'
        });
    });
});

function exploreSearchSuccess(data,textStatus,jqXHR) {
    $('#exploresearch-results').html(data);
}

$('input[value="Save Module"]').on('click',function() { // double check that the selected options correspond to keyword buttons shown
    // check to make sure the user has added at least one keyword tag and at least one outcome
    var needsnewname = 0;
    $('#id_name').each( function() {
        if ($(this).val() == "Module Name") {
            alert("Please select a more informative module name.");
            needsnewname = 1;
        }
    });
    if (needsnewname == 1) {
        $('#id_name').focus();
        return false;
    }
    var needsurl = 0;
    $('#id_link').each( function() {
        if ($(this).val() == "Enter Module URL") {
            alert("Please link your module to MITx content.");
            needsurl = 1;
        }
    });
    if (needsurl == 1) {
        $('#id_link').focus();
        return false;
    }
    if ($('#id_keywords option[selected="selected"]').length == 0) {
        alert("Please specify at least one keyword tag for your module.");
        return false;
    }    
    if ($('#id_outcomes option[selected="selected"]').length == 0) {
        alert("Please specify at least one outcome tag for your module.");
        return false;
    }    
    // first go through buttons and make sure there is corresponding select
    $('#manually_added_keywords button,#automatic_keyword_recommendation button, #automatic_keyword_recommendation_from_outcomes button').each( function() {
        var kwval = $(this).attr('value');
        if ($('#id_keywords option[value='+kwval+']').length == 0) { // should have selected option, but it's not there
            alert("Missing selected option --- button exists, but select option doesn't.");
            return false;
        }
    });
    // then check that for each selected option in keywords, there is a corresponding button below
    $('#id_keywords option[selected="selected"]').each( function() {
        var optval = $(this).attr('value');
        var inmanual = 0;
        var inauto = 0;
        var inautofromoutcome = 0;
        if ($('#manually_added_keywords button[value='+optval+']').length > 0) { 
            inmanual = 1;
        }
        if ($('#automatic_keyword_recommendation button[value='+optval+']').length > 0) { 
            inauto = 1;
        }
        if ($('#automatic_keyword_recommendation_from_outcomes button[value='+optval+']').length > 0) { 
            inautofromoutcome = 1;
        }
        if (inmanual + inauto + inautofromoutcome == 0) {
            alert("There is a selected keyword option that does not appear as a tag below.");
            return false;
        }
    });
});

$('#id_outcomes').change(function() { // when the selections in outcomes change
    // Temporary solution to set selected outcomes to selected="selected"
    $('#id_outcomes option:selected').attr('selected',"selected");
    // redo keyword recommendations based on selected outcomes
    // alert("Handler for outcome change called.");
    var selected_outcome_ids = [];
    $('#id_outcomes option[selected="selected"]').each( function() {
        selected_outcome_ids.push($(this).attr('value')); // collect all selected_outcomes into array
    });
    $.ajax({
        type: "POST",
        url: "/create_outcome_keyword/",
        data: {
            'selected_outcome_ids': selected_outcome_ids,
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: outcomeBasedKeywordRecommendation,
        datatype: 'html'
    });
});

function outcomeBasedKeywordRecommendation(data, textStatus, jqXHR)
{
    // load everything, then immediately delete the repeats
    $('#automatic_keyword_recommendation_from_outcomes').html(data); 
    $('#automatic_keyword_recommendation_from_outcomes button').each( function() {
        var thiskwbutton = $(this);
        var thiskwval = $(this).attr('value');
        if ($('#id_keywords option[value='+thiskwval+'][class!="from_outcome_auto_recommendation"]').length > 0) { // found it, so remove from results   
            $(this).remove();
        } else { // if it is not in select option, we must add it
            if ($('#id_keywords option[value='+thiskwval+'][class="from_outcome_auto_recommendation"]').length == 0) {
                var new_keyword = '<option value="'+thiskwval+'" selected="selected" class="from_outcome_auto_recommendation">'+thiskwbutton.text()+'</option>';
                $('#id_keywords').append(new_keyword);
            }
        }
    });
}

$(document).on('click','input#id_name', function() {
    if ($(this).val() == "Module Name") {
        $(this).val("");
    }
}).on('blur','input#id_name', function() {
    if ($(this).val() == "") {
        $(this).val("Module Name");
    }
}).bind('keydown','input#id_name', function(e) {
    var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
    if(key == 13) {
        e.preventDefault();
        $(this).blur();
    }
});

$(document).on('click','input#id_link', function() {
    if ($(this).val() == "Enter Module URL") {
        $(this).val("");
    }
}).on('blur','input#id_link', function() {
    if ($(this).val() == "" || $(this).val() == "http://Enter Module URL" || $(this).val() == "https://Enter Module URL") {
        $(this).val("Enter Module URL");
        $('#module_iframe').removeAttr('src');
    } else {
        var val = $(this).val();
        if (val && !val.match(/^http([s]?):\/\/.*/)) {
            $(this).val('http://' + val);
        }
        $('#module_iframe').attr('src',$(this).val());
    }
}).bind('keydown','input#id_link', function(e) {
    var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
    if(key == 13) {
        e.preventDefault();
        $(this).blur();
    }
});


$(document).on('click','#add_outcome_button',addOutcomeButtonClick);

function addOutcomeButtonClick() {
    $('#add_outcome_button').remove(); 
    $('#add_outcome_li').html('<div class="dropdown"><input class="dropdown-toggle" data-toggle="dropdown" type="text" id="add_outcome_text" maxlength="150" style="background:transparent;border:none;padding:0px;margin:4px;width:500px;"> &nbsp; <button type="button" id="save_new_outcome_button" class="no_name_yet">Save New Outcome</button><button type="button" id="cancel_new_outcome_button">Cancel</button><ul class="dropdown-menu" role="menu" aria-labelledby="dLabel" id="outcome_search_matches"></ul></div>');
    $('#add_outcome_text').focus();
    $('#add_outcome_text').keyup(function() {
        $.ajax({
            type: "POST",
            url: "/outcome/search/",
            data: {
                'outcome_search_text': $("#add_outcome_text").val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: outcomeSearchSuccess,
            datatype: 'html'
        });
    });
    /*
    $('#add_outcome_text').keypress(function(e) {
        //alert("Any old keypress on new outcome text field.");
        if (e.which == 13) { // enter pressed
            alert("You pressed ENTER from new outcome box.");
            var outcome_description = $(this).val()
            // check if this option is already selected
            if ($('#id_outcomes option:contains('+outcome_description+')').length > 0) { // an option already exists that is this
                alert('That outcome is already included.');
                return false;
            }
            // ask for a short name for the outcome, then do an ajax post to add the new outcome to the db
            showAddAnotherPopup('<a href="/outcome/add/" class="add-another" id="add_id_outcomes">Add Outcome</a>');            
            //createNewOutcome(outcome_name,outcome_description);
            hideOutcomeButtonSearchMatches();
            return false;
        }
    }).blur(hideKeywordButtonSearchMatches); // TODO: not working, when the user clicks away, it should go back to being Add Outcome button
    */
    $('#save_new_outcome_button').on('click',function() {
        $(this).before('<input type="text" id="new_outcome_name" maxlength="40" style="background:transparent;border:none;padding:0px;margin:4px;width:200px;" title="Provide a short outcome name" value="Outcome name">');
        $(this).attr('id',"save_new_outcome_button_for_real_this_time");
        $(this).off('click');
        $('#new_outcome_name').focus();
        $('#new_outcome_name').on('blur',function() {
            if ($(this).val() == '') {
                $(this).val("Outcome name");
            }
        });
        $('#save_new_outcome_button_for_real_this_time').on('click',function() {
            // do the ajax submission to create new outcome
            var outcome_name = $('#new_outcome_name').val();
            var outcome_description = $('#add_outcome_text').val();
            if (outcome_name == "Outcome name") {
                alert("Please give your new outcome a more appropriate name.");
                $('#new_outcome_name').focus();
                return false;
            } 
            // check if this outcome is already included:
            var already_included = 0;
            $('#id_outcomes option[selected="selected"]').each( function () {
                if ($(this).text() == outcome_name) {
                    already_included = 1;
                }
            });
            if (already_included == 1) {
                alert("That outcome is already included in this module.");
                return false;
            }   
            createNewOutcome(outcome_name,outcome_description);
        });
    });
    $('#cancel_new_outcome_button').on('click',function() {
        // set this li back to the Add Outcome button
        $('#add_outcome_li').html('<button type="button" id="add_outcome_button" value="add_outcome"><i>Add Outcome</i></button>');
    });
}


function createNewOutcome(outcome_name,outcome_description) {
    $.ajax({
	    type: "POST",
	    url: "/outcome/new/",
	    data: {
		    'outcome_description': outcome_description,
            'outcome_name': outcome_name,
 		    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
	    },
	    success: newOutcomeSuccess,
	    dataType: 'html'
    });
}

function newOutcomeSuccess(data, textStatus, jqXHR)
{
    $("#id_outcomes").append(data);
    // add the new outcome to the list of outcomes
    var outcome_id = $(data).filter('option').attr('value');
    var outcome_name = $(data).filter('option').text()
    var outcome_description = $(data).filter('option').attr('title');
    $('#add_outcome_li').before('<li value="'+ outcome_id+ '" title="' + outcome_name + '">'+ outcome_description +' &nbsp; &nbsp; <img src="/static/img/trash_can.png" alt="delete" class="deleteOutcome" title="delete"></li> ');
    // remove the input fields and put the "Add Outcome" button back in its place
    $('#add_outcome_li').html('<button type="button" id="add_outcome_button" value="add_outcome"><i>Add Outcome</i></button>');
}


function outcomeSearchSuccess(data, textStatus, jqXHR)
{
    $("#outcome_search_matches").html(data);
    // TODO: check to see if the returned matches already are in option before displaying them
    // what comes back: <li><a href="#" class="outcome_search_result" value="{{ outcome.id }}" title="{{ outcome.name }}">{{ outcome.description }}</a></li>
    $('#outcomes_ul li a').each( function() {
        var thisocval = $(this).attr('value');
        if ($('#id_outcomes option[value='+thisocval+'][selected="selected"]').length > 0) { // found it, so remove from results
            $(this).parent().remove();
        }
    });
}


function hideOutcomeButtonSearchMatches() {
    $('#outcome_search_matches').html('');
    $('#add_outcome_li').html('<button type="button" id="add_outcome_button" value="add_outcome"><i>Add Outcome</i></button>');
}

$(document).on('click','#add_keyword_button',addKeywordButtonClick);

function addKeywordButtonClick() {
    $('#add_keyword_button').html('<input type="text" id="add_keyword_button_text" maxlength="30" style="background:transparent;border:none;padding:0px;margin:4px;width:150px;">');
    $('#add_keyword_button').prop('value',"input_text");
    $("#add_keyword_button_text").focus();
    $('#add_keyword_button_text').keyup(function() {
        $.ajax({
            type: "POST",
            url: "/keyword/search/",
            data: {
                'keyword_search_text': $("#add_keyword_button_text").val(),
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: keywordSearchSuccess,
            datatype: 'html'
        });
    });
    $('#add_keyword_button_text').keypress(function(e) {
        if (e.which == 13) { // enter pressed
            var kw = $(this).val()
            // check if this option is already selected
            if ($('#id_keywords option:contains('+kw+')').length > 0) { // an option already exists that is this
                alert(kw+' is already included as a keyword.');
                return false;
            }
            // do an ajax post to add the new keyword to the db
            createNewKeyword(kw);
            hideKeywordButtonSearchMatches();
            return false;
        }
        /*
        if (e.which == 32) { // spacebar pressed -- Right now, spacebar makes the input textfield get deleted completely
            // alert("Spacebar pressed");
            // $(this).val() = $(this).val + ' ';
            return false;
        }
        */
    });
}


function createNewKeyword(kwname) {
    $.ajax({
	    type: "POST",
	    url: "/keyword/new/",
	    data: {
		    'keyword_name': kwname,
 		    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
	    },
	    success: newKeywordSuccess,
	    dataType: 'html'
    });
}

function newKeywordSuccess(data, textStatus, jqXHR)
{
    $("#id_keywords").append(data);
    // add the new keyword button to manually created keywords area
    var kwval = $(data).filter('option').attr('value');
    var kwname = $(data).filter('option').text();
    var newbuttonhtml = '<button type="button" class="new_keyword" value="'+ kwval +'" title="Click to remove">' + kwname + '</button>';
    $('#manually_added_keywords').append(newbuttonhtml);
}

$(document).on('blur','#add_keyword_button',hideKeywordButtonSearchMatches);

$(document).on('mousedown','a.outcome_search_result', function() {
    var outcome_id = $(this).attr('value');
    var outcome_name = $(this).attr('title');
    var outcome_description = $(this).text();
    $('#add_outcome_li').before('<li value="'+ outcome_id+ '" title="' + outcome_name + '">'+ outcome_description +' &nbsp; &nbsp; <img src="/static/img/trash_can.png" alt="delete" class="deleteOutcome" title="delete"></li> ');
    var new_outcome = '<option value="'+outcome_id+'" selected="selected">'+outcome_name+'</option>';
    $('#id_outcomes').append(new_outcome);
    hideOutcomeButtonSearchMatches();
    $('.deleteOutcome').css('cursor', 'pointer');
});

$(document).on('mousedown','.deleteOutcome', function() {
    var outcome_li = $(this).parent();
    var outcome_id = outcome_li.attr('value');
    $('#id_outcomes option[value="'+outcome_id+'"]').remove();
    $(this).parent().remove();
});

$(document).on('mousedown','.keyword_search_result_button', function() {
    $("document").off('blur','#add_keyword_button',hideKeywordButtonSearchMatches);
    $('#add_keyword_button').html('<i>Add Keyword</i>');
    $('#add_keyword_button').prop('value',"add_keyword");
    var keywordbuttonfromsearch = $(this);
    keywordbuttonfromsearch.prop('class',"existing_keyword");
    keywordbuttonfromsearch.prop('title',"Click to remove");
    var keywordbuttonfromsearchvalue = keywordbuttonfromsearch.attr('value');
    $('#manually_added_keywords').append(keywordbuttonfromsearch);
    // add and set this keyword to 'selected' in the selected html in the form
    var new_keyword = '<option value="'+keywordbuttonfromsearchvalue+'" selected="selected">'+keywordbuttonfromsearch.text()+'</option>';
    $('#id_keywords').append(new_keyword);
    hideKeywordButtonSearchMatches();
    $("document").on('blur','#add_keyword_button',hideKeywordButtonSearchMatches);
});

$(document).on('click','#manually_added_keywords button', function() {
    // when a selected keyword is clicked, it should be removed from the selected_keywords section and 
    // also should be removed as a selected option in the select section #id_keywords for the form
    var kwval = $(this).attr('value');
    $('#id_keywords option[value='+kwval+']').remove();
    $(this).remove();
});

$(document).on('click','#automatic_keyword_recommendation button', function() {
    // when a selected keyword is clicked, it should be removed from the selected_keywords section and 
    // also should be removed as a selected option in the select section #id_keywords for the form
    var kwval = $(this).attr('value');
    $('#id_keywords option[value='+kwval+']').remove();
    $(this).remove();
});

$(document).on('click','#automatic_keyword_recommendation_from_outcomes button', function() {
    // when a selected keyword is clicked, it should be removed from the selected_keywords section and 
    // also should be removed as a selected option in the select section #id_keywords for the form
    var kwval = $(this).attr('value');
    $('#id_keywords option[value='+kwval+']').remove();
    $(this).remove();
});


function hideKeywordButtonSearchMatches() {
    $('#keyword_button_search_matches').html('');
    $('#add_keyword_button').html('<i>Add Keyword</i>');
    $('#add_keyword_button').prop('value',"add_keyword");
}


function keywordSearchSuccess(data, textStatus, jqXHR)
{
    // check to see if the returned matches already are in option before displaying them
    $("#keyword_button_search_matches").html(data);
    $('#keyword_button_search_matches button').each( function() {
        var thiskwbutton = $(this);
        var thiskwval = $(this).attr('value');
        if ($('#id_keywords option[value='+thiskwval+']').length > 0) { // found it, so remove from results
            thiskwbutton.remove();
        }
    });
}

$(function(){

	$('#search').keyup(function() {

		$.ajax({
			type: "POST",
			url: "/search/",
			data: {
				'search_text': $('#search').val(),
 				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType: 'html'
		});
	});
});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search-results').html(data);

}

$(function(){

	$('#id_name').blur(function() {

		$.ajax({
			type: "POST",
			url: "/create_name_keyword/",
			data: {
				'name_text': $('#id_name').val(),
 				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
			},
			success: keywordRecommendationSuccess,
			dataType: 'html'
		});

		$.ajax({
			type: "POST",
			url: "/create_name_outcome/",
			data: {
				'name_text': $('#id_name').val(),
 				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
			},
			success: outcomeRecommendationSuccess,
			dataType: 'html'
		});
	});
});

function keywordRecommendationSuccess(data, textStatus, jqXHR)
{
    // load everything, then immediately delete the repeats
    $('#automatic_keyword_recommendation').html(data); 
    $('#automatic_keyword_recommendation button').each( function() {
        var thiskwbutton = $(this);
        var thiskwval = $(this).attr('value');
        if ($('#id_keywords option[value='+thiskwval+']').length > 0) { // found it, so remove from results
            thiskwbutton.remove();
        } else { // if it is not in select option, we must add it
            var new_keyword = '<option value="'+thiskwval+'" selected="selected" class="from_auto_recommendation">'+thiskwbutton.text()+'</option>';
            $('#id_keywords').append(new_keyword);
        }
    });
    $('#id_keywords option.from_auto_recommendation').each( function() {
        var optionval = $(this).attr('value');
        if ($('#automatic_keyword_recommendation button[value='+optionval+']').length == 0) { 
            $(this).remove();
        }
    });
}

function outcomeRecommendationSuccess(data, textStatus, jqXHR)
{
    // get outcome recommendations, and if they are already in the outcome_ul list, delete them
    $('#add_outcome_li').before(data);
    $('#outcomes_ul li').not('#add_outcome_li').each( function() {
        // for each outcome in the li list, check that it is selected (only once!) in the select #id_outcomes
        var outcome_id = $(this).attr('value');
        var outcome_name = $(this).attr('title');
        var num_appearances = 0;
        $('#id_outcomes option').each( function() {
            if (($(this).attr('value')==outcome_id) && ($(this).attr('selected')=="selected")) {
                num_appearances++;
            }
        });
        if (num_appearances == 0) { // need to add it
            $('#id_outcomes').prepend('<option value="'+outcome_id+'" selected="selected">'+outcome_name+'</option>');
        } else { // need to make just one of them
            $('#id_outcomes option[value="'+outcome_id+'"]').remove(); // remove all
            $('#id_outcomes').prepend('<option value="'+outcome_id+'" selected="selected">'+outcome_name+'</option>'); // add one back
        }
    });
}

// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.
function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct 
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showRelatedObjectLookupPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);
    var href;
    if (triggeringLink.href.search(/\?/) >= 0) {
        href = triggeringLink.href + '&pop=1';
    } else {
        href = triggeringLink.href + '?pop=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissRelatedLookupPopup(win, chosenId) {
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(name).value = chosenId;
    }
    win.close();
}

function showAddAnotherPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissAddAnotherPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = document.getElementById(name);
    if (elem) {
        var elemName = elem.nodeName.toUpperCase();
        if (elemName == 'SELECT') {
            var o = new Option(newRepr, newId);
            elem.options[elem.options.length] = o;
            o.selected = true;
        } else if (elemName == 'INPUT') {
            if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
                elem.value += ',' + newId;
            } else {
                elem.value = newId;
            }
        }
    } else {
        var toId = name + "_to";
        elem = document.getElementById(toId);
        var o = new Option(newRepr, newId);
        SelectBox.add_to_cache(toId, o);
        SelectBox.redisplay(toId);
    }
    win.close();
}


/* gettext library */

var catalog = new Array();

function pluralidx(count) { return (count == 1) ? 0 : 1; }


function gettext(msgid) {
  var value = catalog[msgid];
  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  value = catalog[singular];
  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[pluralidx(count)];
  }
}

function gettext_noop(msgid) { return msgid; }

function pgettext(context, msgid) {
  var value = gettext(context + '' + msgid);
  if (value.indexOf('') != -1) {
    value = msgid;
  }
  return value;
}

function npgettext(context, singular, plural, count) {
  var value = ngettext(context + '' + singular, context + '' + plural, count);
  if (value.indexOf('') != -1) {
    value = ngettext(singular, plural, count);
  }
  return value;
}

function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
  } else {
    return fmt.replace(/%s/g, function(match){return String(obj.shift())});
  }
}

/* formatting library */

var formats = new Array();

formats['DATETIME_FORMAT'] = 'N j, Y, P';
formats['DATE_FORMAT'] = 'N j, Y';
formats['DECIMAL_SEPARATOR'] = '.';
formats['MONTH_DAY_FORMAT'] = 'F j';
formats['NUMBER_GROUPING'] = '3';
formats['TIME_FORMAT'] = 'P';
formats['FIRST_DAY_OF_WEEK'] = '0';
formats['TIME_INPUT_FORMATS'] = ['%H:%M:%S', '%H:%M'];
formats['THOUSAND_SEPARATOR'] = ',';
formats['DATE_INPUT_FORMATS'] = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'];
formats['YEAR_MONTH_FORMAT'] = 'F Y';
formats['SHORT_DATE_FORMAT'] = 'm/d/Y';
formats['SHORT_DATETIME_FORMAT'] = 'm/d/Y P';
formats['DATETIME_INPUT_FORMATS'] = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%m/%d/%Y', '%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%m/%d/%y'];

function get_format(format_type) {
    var value = formats[format_type];
    if (typeof(value) == 'undefined') {
      return msgid;
    } else {
      return value;
    }
}

// Core javascript helper functions

// basic browser identification & version
var isOpera = (navigator.userAgent.indexOf("Opera")>=0) && parseFloat(navigator.appVersion);
var isIE = ((document.all) && (!isOpera)) && parseFloat(navigator.appVersion.split("MSIE ")[1].split(";")[0]);

// Cross-browser event handlers.
function addEvent(obj, evType, fn) {
    if (obj.addEventListener) {
        obj.addEventListener(evType, fn, false);
        return true;
    } else if (obj.attachEvent) {
        var r = obj.attachEvent("on" + evType, fn);
        return r;
    } else {
        return false;
    }
}

function removeEvent(obj, evType, fn) {
    if (obj.removeEventListener) {
        obj.removeEventListener(evType, fn, false);
        return true;
    } else if (obj.detachEvent) {
        obj.detachEvent("on" + evType, fn);
        return true;
    } else {
        return false;
    }
}

// quickElement(tagType, parentReference, textInChildNode, [, attribute, attributeValue ...]);
function quickElement() {
    var obj = document.createElement(arguments[0]);
    if (arguments[2] != '' && arguments[2] != null) {
        var textNode = document.createTextNode(arguments[2]);
        obj.appendChild(textNode);
    }
    var len = arguments.length;
    for (var i = 3; i < len; i += 2) {
        obj.setAttribute(arguments[i], arguments[i+1]);
    }
    arguments[1].appendChild(obj);
    return obj;
}

// ----------------------------------------------------------------------------
// Cross-browser xmlhttp object
// from http://jibbering.com/2002/4/httprequest.html
// ----------------------------------------------------------------------------
var xmlhttp;
/*@cc_on @*/
/*@if (@_jscript_version >= 5)
    try {
        xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (E) {
            xmlhttp = false;
        }
    }
@else
    xmlhttp = false;
@end @*/
if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
  xmlhttp = new XMLHttpRequest();
}

// ----------------------------------------------------------------------------
// Find-position functions by PPK
// See http://www.quirksmode.org/js/findpos.html
// ----------------------------------------------------------------------------
function findPosX(obj) {
    var curleft = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curleft += obj.offsetLeft - ((isOpera) ? 0 : obj.scrollLeft);
            obj = obj.offsetParent;
        }
        // IE offsetParent does not include the top-level
        if (isIE && obj.parentElement){
            curleft += obj.offsetLeft - obj.scrollLeft;
        }
    } else if (obj.x) {
        curleft += obj.x;
    }
    return curleft;
}

function findPosY(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curtop += obj.offsetTop - ((isOpera) ? 0 : obj.scrollTop);
            obj = obj.offsetParent;
        }
        // IE offsetParent does not include the top-level
        if (isIE && obj.parentElement){
            curtop += obj.offsetTop - obj.scrollTop;
        }
    } else if (obj.y) {
        curtop += obj.y;
    }
    return curtop;
}

//-----------------------------------------------------------------------------
// Date object extensions
// ----------------------------------------------------------------------------

Date.prototype.getTwelveHours = function() {
    hours = this.getHours();
    if (hours == 0) {
        return 12;
    }
    else {
        return hours <= 12 ? hours : hours-12
    }
}

Date.prototype.getTwoDigitMonth = function() {
    return (this.getMonth() < 9) ? '0' + (this.getMonth()+1) : (this.getMonth()+1);
}

Date.prototype.getTwoDigitDate = function() {
    return (this.getDate() < 10) ? '0' + this.getDate() : this.getDate();
}

Date.prototype.getTwoDigitTwelveHour = function() {
    return (this.getTwelveHours() < 10) ? '0' + this.getTwelveHours() : this.getTwelveHours();
}

Date.prototype.getTwoDigitHour = function() {
    return (this.getHours() < 10) ? '0' + this.getHours() : this.getHours();
}

Date.prototype.getTwoDigitMinute = function() {
    return (this.getMinutes() < 10) ? '0' + this.getMinutes() : this.getMinutes();
}

Date.prototype.getTwoDigitSecond = function() {
    return (this.getSeconds() < 10) ? '0' + this.getSeconds() : this.getSeconds();
}

Date.prototype.getHourMinute = function() {
    return this.getTwoDigitHour() + ':' + this.getTwoDigitMinute();
}

Date.prototype.getHourMinuteSecond = function() {
    return this.getTwoDigitHour() + ':' + this.getTwoDigitMinute() + ':' + this.getTwoDigitSecond();
}

Date.prototype.strftime = function(format) {
    var fields = {
        c: this.toString(),
        d: this.getTwoDigitDate(),
        H: this.getTwoDigitHour(),
        I: this.getTwoDigitTwelveHour(),
        m: this.getTwoDigitMonth(),
        M: this.getTwoDigitMinute(),
        p: (this.getHours() >= 12) ? 'PM' : 'AM',
        S: this.getTwoDigitSecond(),
        w: '0' + this.getDay(),
        x: this.toLocaleDateString(),
        X: this.toLocaleTimeString(),
        y: ('' + this.getFullYear()).substr(2, 4),
        Y: '' + this.getFullYear(),
        '%' : '%'
    };
    var result = '', i = 0;
    while (i < format.length) {
        if (format.charAt(i) === '%') {
            result = result + fields[format.charAt(i + 1)];
            ++i;
        }
        else {
            result = result + format.charAt(i);
        }
        ++i;
    }
    return result;
}

// ----------------------------------------------------------------------------
// String object extensions
// ----------------------------------------------------------------------------
String.prototype.pad_left = function(pad_length, pad_string) {
    var new_string = this;
    for (var i = 0; new_string.length < pad_length; i++) {
        new_string = pad_string + new_string;
    }
    return new_string;
}

// ----------------------------------------------------------------------------
// Get the computed style for and element
// ----------------------------------------------------------------------------
function getStyle(oElm, strCssRule){
    var strValue = "";
    if(document.defaultView && document.defaultView.getComputedStyle){
        strValue = document.defaultView.getComputedStyle(oElm, "").getPropertyValue(strCssRule);
    }
    else if(oElm.currentStyle){
        strCssRule = strCssRule.replace(/\-(\w)/g, function (strMatch, p1){
            return p1.toUpperCase();
        });
        strValue = oElm.currentStyle[strCssRule];
    }
    return strValue;
}

(function($) {
	$.fn.actions = function(opts) {
		var options = $.extend({}, $.fn.actions.defaults, opts);
		var actionCheckboxes = $(this);
		var list_editable_changed = false;
		checker = function(checked) {
			if (checked) {
				showQuestion();
			} else {
				reset();
			}
			$(actionCheckboxes).attr("checked", checked)
				.parent().parent().toggleClass(options.selectedClass, checked);
		}
		updateCounter = function() {
			var sel = $(actionCheckboxes).filter(":checked").length;
			$(options.counterContainer).html(interpolate(
			ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
				sel: sel,
				cnt: _actions_icnt
			}, true));
			$(options.allToggle).attr("checked", function() {
				if (sel == actionCheckboxes.length) {
					value = true;
					showQuestion();
				} else {
					value = false;
					clearAcross();
				}
				return value;
			});
		}
		showQuestion = function() {
			$(options.acrossClears).hide();
			$(options.acrossQuestions).show();
			$(options.allContainer).hide();
		}
		showClear = function() {
			$(options.acrossClears).show();
			$(options.acrossQuestions).hide();
			$(options.actionContainer).toggleClass(options.selectedClass);
			$(options.allContainer).show();
			$(options.counterContainer).hide();
		}
		reset = function() {
			$(options.acrossClears).hide();
			$(options.acrossQuestions).hide();
			$(options.allContainer).hide();
			$(options.counterContainer).show();
		}
		clearAcross = function() {
			reset();
			$(options.acrossInput).val(0);
			$(options.actionContainer).removeClass(options.selectedClass);
		}
		// Show counter by default
		$(options.counterContainer).show();
		// Check state of checkboxes and reinit state if needed
		$(this).filter(":checked").each(function(i) {
			$(this).parent().parent().toggleClass(options.selectedClass);
			updateCounter();
			if ($(options.acrossInput).val() == 1) {
				showClear();
			}
		});
		$(options.allToggle).show().click(function() {
			checker($(this).attr("checked"));
			updateCounter();
		});
		$("div.actions span.question a").click(function(event) {
			event.preventDefault();
			$(options.acrossInput).val(1);
			showClear();
		});
		$("div.actions span.clear a").click(function(event) {
			event.preventDefault();
			$(options.allToggle).attr("checked", false);
			clearAcross();
			checker(0);
			updateCounter();
		});
		lastChecked = null;
		$(actionCheckboxes).click(function(event) {
			if (!event) { var event = window.event; }
			var target = event.target ? event.target : event.srcElement;
			if (lastChecked && $.data(lastChecked) != $.data(target) && event.shiftKey == true) {
				var inrange = false;
				$(lastChecked).attr("checked", target.checked)
					.parent().parent().toggleClass(options.selectedClass, target.checked);
				$(actionCheckboxes).each(function() {
					if ($.data(this) == $.data(lastChecked) || $.data(this) == $.data(target)) {
						inrange = (inrange) ? false : true;
					}
					if (inrange) {
						$(this).attr("checked", target.checked)
							.parent().parent().toggleClass(options.selectedClass, target.checked);
					}
				});
			}
			$(target).parent().parent().toggleClass(options.selectedClass, target.checked);
			lastChecked = target;
			updateCounter();
		});
		$('form#changelist-form table#result_list tr').find('td:gt(0) :input').change(function() {
			list_editable_changed = true;
		});
		$('form#changelist-form button[name="index"]').click(function(event) {
			if (list_editable_changed) {
				return confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
			}
		});
		$('form#changelist-form input[name="_save"]').click(function(event) {
			var action_changed = false;
			$('div.actions select option:selected').each(function() {
				if ($(this).val()) {
					action_changed = true;
				}
			});
			if (action_changed) {
				if (list_editable_changed) {
					return confirm(gettext("You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action."));
				} else {
					return confirm(gettext("You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button."));
				}
			}
		});
	}
	/* Setup plugin defaults */
	$.fn.actions.defaults = {
		actionContainer: "div.actions",
		counterContainer: "span.action-counter",
		allContainer: "div.actions span.all",
		acrossInput: "div.actions input.select-across",
		acrossQuestions: "div.actions span.question",
		acrossClears: "div.actions span.clear",
		allToggle: "#action-toggle",
		selectedClass: "selected"
	}
})(django.jQuery);
