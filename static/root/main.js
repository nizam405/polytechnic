function fix(){
    // Footer
    var bodyHeight = $("body").outerHeight();
    var bodyWidth = $("body").width()
    var windowHeight = window.innerHeight ||
        document.documentElement.clientHeight ||
        document.body.clientHeight;

    if (bodyHeight < windowHeight) {
        $("#footer").css("position", "absolute");
        $("#footer").css("bottom", "0");
        $("#footer").css("width", "100%");
    } 
    else {
        $("#footer").css("position", "relative");
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
        $(".info-section").css("marginTop", 60);
    }

    // $(".info-section").css("overflowY",'auto');
    // $(".info-section").css("overflowX",'hidden');
}
$(window).on("resize load", function(){
    fix();
    // console.log(window.innerWidth)
});

// function upload_img(input) {
//     if (input.files && input.files[0]) {
//         var reader = new FileReader();

//         reader.onload = function (e) {
//             $('#profile-picture').attr('src', e.target.result);
//         }

//         reader.readAsDataURL(input.files[0]);
//     }
// }

// $('#id_image').click(function () { 
//     upload_img(this)
// });
