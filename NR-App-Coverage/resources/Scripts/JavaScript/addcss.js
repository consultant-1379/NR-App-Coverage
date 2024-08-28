$("#accordion h3").attr( 'style', 'letter-spacing:1px ; PADDING-BOTTOM: 10px; PADDING-TOP: 10px; PADDING-LEFT: 25px; PADDING-RIGHT: 20px; color: #000; background: #b4b4b4; border:1px solid #b4b4b4');
$("#accordion").accordion({heightStyle: 'content'});
var event = $( "#accordion" ).accordion( "option", "event" );

$("#accordion").on("accordionactivate", function(event, ui) {
    $("#refreshWrapper input").val(Math.random());
    $("#refreshWrapper input").focus();
    $("#refreshWrapper input").blur();
});

$("#PerfThresholdItem").click(function() {
  $("#activeAccordian input").val('0').blur();
  setTimeout(function(){
    activeAccordian = $("#activeAccordianLbl").first().text().trim()
  }, 1000);
});

$("#MSAItem").click(function() {
  $("#activeAccordian input").val('0').blur();
  setTimeout(function(){
    activeAccordian = $("#activeAccordianLbl").first().text().trim()
  }, 1000);
});


$("#accordion").accordion({
	active: parseInt(activeAccordian),
	collapsible: true,
	heightStyle: 'content'
})

$("#accordion .ui-widget-content").css('border', '1px solid #fff') 