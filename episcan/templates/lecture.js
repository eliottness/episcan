var title = document.title;

var img_ext = ".jpg"
var pages   = {{ images_id }}

var next_chapter =  "{{ next_chap_url }}" ;
var prev_chapter =  "{{ prev_chap_url }}" ;

var nb_pages        = {{ chapter_nb_pages }};
window.current_page = 1;

var base_url = "{{ images_route }}";

// refresh test
function changePage() {
    document.getElementById("page-img").src = base_url + pages[window.current_page - 1] + img_ext;
}

function nextPage() {

    if (window.current_page + 1 <= nb_pages) {
        window.current_page += 1;
        changePage();
    } else {
        nextChap();
    }
}

function prevPage() {

    if (window.current_page - 1 >= 1) {
        window.current_page -= 1;
        changePage();
    } else {
        prevChap();
    }
}

function nextChap(){
    if (next_chapter == "None") {
         alert("Vous êtes a la dernière page du dernier chapitre");
     } else {
         window.location = next_chapter;
     }
}

function prevChap(){
    if (prev_chapter == "None") {
        alert("Vous êtes a la première page du premier chapitre");
    } else {
        window.location = prev_chapter;
    }
}

/*$('a#modePPP').click(function (e) {
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

$('#page-list').on('change', function () {
    changePage(this.value);
});

$('#page-list').twbsPagination({
  totalPages: {{ chapter_nb_pages }},
  visiblePages: 7,
  onPageClick: function (event, page) {
    changePage(parseInt(this.value));
  }
});*/

$('#ppp').on('click', nextPage);
$('#prev-page').on('click', prevPage);
$('#next-page').on('click', nextPage);
$('#prev-chap').on('click', prevChap);
$('#next-chap').on('click', nextChap);

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
