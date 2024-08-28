//sript params
fixedElementSelector = "#masthead"

//remember starting position
fixedElement = document.querySelector(fixedElementSelector);
fixedElementRect = fixedElement.getBoundingClientRect();
fixedElement.style.top = fixedElementRect.y+"px";
fixedElement.style.left = fixedElementRect.x+"px";
fixedElement.style.width = fixedElementRect.width+"px";
fixedElement.style.height = fixedElementRect.height+"px";
initialPosition = fixedElement.style.position;

//scrollable elements
elementsWithOverflowStyle = document.querySelectorAll('[style*="overflow"]');

//update position
function setFixedPosition(overflowElement){
  fixedElement.style.position = overflowElement.scrollTop>0?"fixed":initialPosition;
}

elementsWithOverflowStyle.forEach(overflowElement => {
    overflowElement.addEventListener('scroll', ()=>setFixedPosition(overflowElement));
});