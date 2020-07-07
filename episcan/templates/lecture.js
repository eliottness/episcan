var title = document.title;

var pages = {{ images_id }}

var next_chapter =  "{{ next_chap_url }}" ;
var prev_chapter =  "{{ prev_chap_url }}" ;


var current_page = 1;

var base_url = "{{ images_route }}";

var initialized = false;

jQuery(document).ready(function () {
    $('.selectpicker').selectpicker();
    if ($("div#all").is(":visible"))
        $("div#all img").unveil(300);
});

// refresh test
function changePage(value) {
    document.getElementById("page-img").src = pages[value - 1];
}

function nextPage() {
    // refresh test
    nextPageVal = $('#page-list option:selected').next().val();

    if (typeof nextPageVal != 'undefined') {
        $("#page-list").val(nextPageVal);
        $("#page-list").change();
    } else {
        nextChap();
    }
}

function prevPage() {
    // refresh test
    prevPageVal = $('#page-list option:selected').prev().val();

    if (typeof prevPageVal != 'undefined') {
        $("#page-list").val(prevPageVal);
        $("#page-list").change();
    } else {
        prevChap();
    }
}

function nextChap(){
    window.location = next_chapter;
}

function prevChap(){
    window.location = prev_chapter;
}

$('a#modePPP').click(function (e) {
    e.preventDefault();
    $('.pager-cnt .page-nav').show();
    $('div#ppp').show();
    $('div#all').hide();
    $(document).on('keyup', function (e) {
        KeyCheck(e);
    });
});

$('a#modeALL').click(function (e) {
    e.preventDefault();
    $('.pager-cnt .page-nav').hide();
    $('div#ppp').hide();
    $('div#all').show();
    $(document).off('keyup');
    $("div#all img").unveil(300);
});

$('select#page-list').on('change', function () {
    changePage(this.value);
});

$('#ppp a').on('click', nextPage);
$('#prev-page').on('click', prevPage);
$('#next-page').on('click', nextPage);

$(document).on('keyup', function (e) {
    KeyCheck(e);
});

function KeyCheck(e) {
    var ev = e || window.event;
    ev.preventDefault();
    var KeyID = ev.keyCode;
    switch (KeyID) {
        case 36:
            window.location = "{{ manga_home_url }}";
            break;
        case 33:
        case 37:
            prevPage();
            break;
        case 34:
        case 39:
            nextPage();
            break;
    }
}
