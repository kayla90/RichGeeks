var req;
    	function getMessageNumber() {
    	    if (window.XMLHttpRequest) {
    	        req = new XMLHttpRequest();
    	    } else {
    	        req = new ActiveXObject("Microsoft.XMLHTTP");
    	    }
    	    req.onreadystatechange = handleResponse;
    	    req.open("GET", "/message/number", true);
    	    req.send(); 
    	}
    	function handleResponse() {
    	    if (req.readyState != 4 || req.status != 200) {
    	        return;
    	    }
    	    $("#message-number").html(req.responseText)
    	}
    	getMessageNumber()
    	window.setInterval(getMessageNumber, 10000);