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
