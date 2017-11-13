$(document).ready(function() {
    $('.item-body').readmore();
    
    $('.uvote').click(function() {
        vote($(this).attr('value'), 'upvote');
    });
    $('.dvote').click(function() {
        vote($(this).attr('value'), 'downvote');
    });

    $('.reply').click(function() {
        var cid = $(this).attr('cid');
        var box = $('#reply-box-' + cid);
        if (box.hasClass('hidden')) box.removeClass('hidden');
        else box.addClass('hidden');
    });

    $('.collapse').click(function() {
        var cid = $(this).attr('cid');
        var div = $('#children-of-' + cid);
        if (div.hasClass('hidden')) {
            div.removeClass('hidden');
            $(this).text('[-]');
        }
        else {
            div.addClass('hidden');
            $(this).text('[+]');
        }
    })
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