$(document).ready(function() {
	$('.item-body').readmore();
	
	$('.uvote').click(function() {
		vote($(this).attr('value'), 'upvote');
	});
	$('.dvote').click(function() {
		vote($(this).attr('value'), 'downvote');
	});
});

function vote(id, vote) {
	$.get('/vote/' + id + '/' + vote, function(res) {
		res = $.parseJSON(res);

		var v = res.vote;
		$('#uvote-' + id).removeClass('clicked');
		$('#dvote-' + id).removeClass('clicked');

		console.log(v);
		if (v == 1) $('#uvote-' + id).addClass('clicked');
		if (v == -1) $('#dvote-' + id).addClass('clicked');

		$('#score-' + id).text(res.count);
	}).fail(function() {
    	alert('You need to login to do that :/');
	});
}