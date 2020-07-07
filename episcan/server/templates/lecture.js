var title = document.title;
//var pages = [{"page_image":"01.jpg","page_slug":1,"external":0},{"page_image":"02.jpg","page_slug":2,"external":0},{"page_image":"03.jpg","page_slug":3,"external":0},{"page_image":"04.jpg","page_slug":4,"external":0},{"page_image":"05.jpg","page_slug":5,"external":0},{"page_image":"06.jpg","page_slug":6,"external":0},{"page_image":"07.jpg","page_slug":7,"external":0},{"page_image":"08.jpg","page_slug":8,"external":0},{"page_image":"09.jpg","page_slug":9,"external":0},{"page_image":"10.jpg","page_slug":10,"external":0},{"page_image":"11.jpg","page_slug":11,"external":0},{"page_image":"12.jpg","page_slug":12,"external":0},{"page_image":"13.jpg","page_slug":13,"external":0},{"page_image":"14.jpg","page_slug":14,"external":0},{"page_image":"15.jpg","page_slug":15,"external":0},{"page_image":"16.jpg","page_slug":16,"external":0},{"page_image":"17.jpg","page_slug":17,"external":0},{"page_image":"18.jpg","page_slug":18,"external":0},{"page_image":"19.jpg","page_slug":19,"external":0},{"page_image":"20.jg","page_slug":20,"external":0},{"page_image":"21.jpg","page_slug":21,"external":0},{"page_image":"22.jpg","page_slug":22,"external":0},{"page_image":"23.jpg","page_slug":23,"external":0},{"page_image":"24.jpg","page_slug":24,"external":0}];

var pages = {{ images_id }}

var next_chapter =  "{{ next_chap_url }}" ;
var prev_chapter =  "{{ prev_chap_url }}" ;

//var preload_next = 3;
//var preload_back = 2;
var current_page = {{ page_num }};

var base_url = "/static/images";

var initialized = false;

jQuery(document).ready(function () {
    $('.selectpicker').selectpicker();
    if ($("div#all").is(":visible"))
        $("div#all img").unveil(300);

    // refresh test
    //preload(current_page);
});

// refresh test
function changePage(value) {
    tab= Array();
    tab[0]=base_url;
    tab[1]="/";
    tab[2]=pages[value - 1];
    document.getElementById("page-img").src = tab.join("");

    var selectElement = document.getElementById("page-list");
    var selectOptions = selectElement.options;
    selectElement.selectedIndex = value;
}

function nextPage() {
    // refresh test
    nextPageVal = $('#page-list option:selected').next().val();
    nextChapterVal = $('#chapter-list li.active').prev().val();

    if (typeof nextPageVal != 'undefined') {
        changePage(nextPageVal);
    }

    if (typeof nextPageVal == 'undefined' && typeof nextChapterVal != 'undefined') {
        window.location = next_chapter;
    }

    if (typeof nextPageVal == 'undefined' && typeof nextChapterVal == 'undefined') {
        alert('Vous êtes à la dernière page du dernier chapitre.');
    }
}

function prevPage() {
    // refresh test
    prevPageVal = $('#page-list option:selected').prev().val();
    prevChapterVal = $('#chapter-list li.active').next().val();

    if (typeof prevPageVal != 'undefined') {
        changePage(prevPageVal);
    }

    if (typeof prevPageVal == 'undefined' && typeof prevChapterVal != 'undefined') {
        window.location = prev_chapter;
    }

    if (typeof prevPageVal == 'undefined' && typeof prevChapterVal == 'undefined') {
        alert('Vous êtes à la dernière page du dernier chapitre.');
    }

function nextChap(){
    window.location = next_chapter;
}

function prevChap(){
    window.location = prev_chapter;
}

/*function preload(id) {
    var array = [];
    var arraydata = [];
    for (i = -preload_back; i < preload_next; i++) {
        if (id + i >= 0 && id + i < pages.length) {
            if (pages[(id + i)].external == 0) {
                array.push('https://lelscan-vf.com/uploads/manga/a-returners-magic-should-be-special/chapters/110/' + pages[(id + i)].page_image);
            } else {
                array.push(pages[(id + i)].page_image);
            }
            arraydata.push(id + i);
        }
    }

    jQuery.preload(array, {
        threshold: 40,
        enforceCache: true,
        onComplete: function (data) {
        }
    });
}*/

function update_numberPanel() {
    $('#page-list').selectpicker('val', current_page);
    $('.pagenumber').text(current_page);
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

//$('#ppp a').on('click', nextPage);
//$('#ppp a').on('click', nextPage);

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
