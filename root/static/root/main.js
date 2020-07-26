function fix(){
    // Footer
    var bodyHeight = $("body").outerHeight();
    var bodyWidth = $("body").width()
    var windowHeight = window.innerHeight ||
        document.documentElement.clientHeight ||
        document.body.clientHeight;

    if (bodyHeight < windowHeight) {
        $('#footer').addClass('absolute-footer')
        $('#footer').removeClass('relative-footer')
    } 
    else {
        $('#footer').removeClass('absolute-footer')
        $('#footer').addClass('relative-footer')
    }
    var footerHeight = $("#footer").outerHeight()
    var headerHeight = $("#header").outerHeight();
    var allowedHeight = windowHeight-headerHeight-footerHeight-20
    if (bodyWidth > 768) {
        $("#admission-info").css("maxHeight", allowedHeight);
        $(".info-section").css("minHeight", allowedHeight);
    } else {
        $("#admission-info").css("minHeight", 'auto');
        $(".info-section").css("minHeight", 'auto');
        // $(".info-section").css("marginTop", 60);
    }
}

function responsiveCollapse() {
    let desktopView = $(document).width();
    if(desktopView >= "1200"){
        $('.show-xl, .show-lg, .show-md, .show-sm').addClass('show')
    }
    else if(desktopView >= "992"){
        $('.show-lg, .show-md, .show-sm').addClass('show')
        $('.show-xl').removeClass('show')
    }
    else if(desktopView >= "768"){
        $('.show-md, .show-sm').addClass('show')
        $('.show-xl, .show-lg').removeClass('show')
    }
    else if(desktopView >= "576"){
        $('.show-sm').addClass('show')
        $('.show-xl, .show-lg, .show-md').removeClass('show')
    }
    else{
        $('.show-xl, .show-lg, .show-md, .show-sm').removeClass('show')
    }
}

$(function(){
    fix();
    responsiveCollapse();
    $(window).resize(function(){
        fix();
        responsiveCollapse();
    })
})
