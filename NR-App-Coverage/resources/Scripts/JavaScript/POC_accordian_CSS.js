
var css = `
div.accordion-container ul {
    list-style: none;
    padding: 0;
}

div.accordion-container ul .inner-visible {
	display: block !important;
	visible: visible;
	padding-left: 1em;
	overflow: hidden;
}

div.accordion-container ul .inner-hidden {
	visibility:hidden !important;
	padding:0px !important;
	border:0px !important;
	height:0px !important;
}
  
div.accordion-container li {
	margin: .5em 0;
}
  
div.accordion-container li div.toggle {
	width: 98%;
	background-color:lightgrey;
	display: block;
	padding: .75em;
	border-radius: 0.15em;
	transition: background .3s ease;
	cursor: pointer;
	height:40px;
}

div.accordion-container li div.toggle:hover {
	background-color: lightgrey;
}

`;

$("<style/>").text(css).appendTo($("#styleDiv"));

