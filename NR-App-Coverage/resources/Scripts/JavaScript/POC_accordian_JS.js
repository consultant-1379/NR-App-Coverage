$(function() {
  
  // react to click event of any .toggle class
  $('.toggle').click(function(e) {
  	e.preventDefault();
  
    // grab what was clicked
    var $this = $(this);

    // flip style to show or hide content
    $this.next().toggleClass("inner-visible");
    $this.next().toggleClass("inner-hidden");
	
    // change symbol beside header text
    if($this.find("span").text().trim() == ">"){
        $this.find("span").text(" ^     ");
    } else{
        $this.find("span").text(" >     ");
    }
  });
});

