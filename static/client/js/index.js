/*
*/
$(function(){
	// iFrameHeight();
	// setMainHeight();
})

function setMainHeight(){
	var bodyHeight = $(window).height();
	var navHeight = $(".nav").height();
	var mainDocument = $(".main");
	mainDocument.css({
		"height":bodyHeight-navHeight+"px"
	})
}

function iFrameHeight(){
        var ifm = document.getElementBy("boxContent");
        var subWeb = document.frames ? document.frames["boxContent"].document : ifm.contentDocument;
        if (ifm != null && subWeb != null) {
            ifm.height = subWeb.body.scrollHeight;
        }
}

// $("body").on("click",".right",function(){
// 	$(this).animate({
// 		"right":"0px",
// 	},500,function(){
// 	})
// })
// $("body").on("mouseout",".right",function() {
// 	$(this).animate({
// 		"right":"-275px",
// 	},500,function(){
//  	})
//  })
// $("body").on("click",".upData",function(){
// 	$.post("/myNoteApp/login",function  (data) {

// 		}
// 	})

// })