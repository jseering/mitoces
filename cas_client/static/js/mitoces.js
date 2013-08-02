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

	$('#id_name').keyup(function() {

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
	$('#keyword_recommendations').html(data);
}

function outcomeRecommendationSuccess(data, textStatus, jqXHR)
{
	$('#outcome_recommendations').html(data);
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
