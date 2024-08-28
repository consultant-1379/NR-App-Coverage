MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

var targetDomId = "tpType"
var onLoadVal=$('#'+targetDomId+' .ComboBoxTextDivContainer').text();
 
if(onLoadVal=="Uplink"){
	$("#performanceTargetDLDiv").hide();
	$("#performanceTargetULDiv").show();
}else if(onLoadVal=="Downlink"){
	$("#performanceTargetULDiv").hide();
	$("#performanceTargetDLDiv").show();
}

var myFunction = function(oldValue,newValue){
  if(newValue=="Uplink"){
		$("#performanceTargetDLDiv").hide();
		$("#performanceTargetULDiv").show();
	}
	else if(newValue=="Downlink"){
		$("#performanceTargetULDiv").hide();
		$("#performanceTargetDLDiv").show();
	}
}

var target = document.getElementById(targetDomId)
var oldVal = target.innerText.trim()

var callback = function(mutations) {
 newVal=$('#'+targetDomId+' .ComboBoxTextDivContainer').text()
 if(newVal!=oldVal) myFunction(oldVal,newVal)
 oldVal = newVal;
}

var observer = new MutationObserver(callback);

var opts = {
    childList: true, 
    attributes: true, 
    characterData: true, 
    subtree: true
}

observer.observe(target,opts);