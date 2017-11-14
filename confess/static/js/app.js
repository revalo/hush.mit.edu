$(document).ready(function() {
    $('.item-body').readmore();
    
    $('.uvote').click(function() {
        vote($(this).attr('value'), 'upvote', $(this).hasClass('commentv'));
    });
    $('.dvote').click(function() {
        vote($(this).attr('value'), 'downvote', $(this).hasClass('commentv'));
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
    });

    $('.sb').click(function() {
        var myB = $(this);
        window.onSubmit = function(token) {
            myB.closest('form').submit();
        };
    });
});

function vote(id, vote, comment) {
    var api = comment ? '/comment/vote/' : '/vote/';
    var v_s = comment ? 'comment-' : '';

    $.get(api + id + '/' + vote, function(res) {
        res = $.parseJSON(res);

        var v = res.vote;
        $('#uvote-' + v_s + id).removeClass('clicked');
        $('#dvote-' + v_s + id).removeClass('clicked');

        console.log(v);
        if (v == 1) $('#uvote-' + v_s + id).addClass('clicked');
        if (v == -1) $('#dvote-' + v_s + id).addClass('clicked');

        $('#score-' + v_s + id).text(res.count);
    }).fail(function() {
        alert('You need to login to do that :/');
    });
}
