MutationObserver = window.MutationObserver || window.WebKitMutationObserver;


//function when  value changes
var changeUI = function(){
var sh=$("#DSNameList").text()
var sh1= document.getElementById("noOfDataSources").childNodes[0].value;
var s1=sh.length;
var s2=sh1.length;
if(s1>0 && s2>0 )
{
$("#ConfigureMSA").show();
$("#newmsa").hide();
}
else
{
$("#newmsa").show();
$("#ConfigureMSA").hide();
} 
}
var target = document.getElementById("noOfDataSources").childNodes[0]

//callback is the function to trigger when target changes
var callback = function(mutations) {
    changeUI()
}

var observer = new MutationObserver(callback);
var opts = {
    childList: true, 
    attributes: true, 
    characterData: true, 
    subtree: true
}
observer.observe(target,opts);
changeUI()