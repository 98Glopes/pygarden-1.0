  document.getElementById("v1").onclick = function() { makeRequest('http://127.0.0.1:5000/valve/v1' , handlePump); };
  document.getElementById("v2").onclick = function() { makeRequest('http://127.0.0.1:5000/valve/v2' , handlePump); };
  document.getElementById("v3").onclick = function() { makeRequest('http://127.0.0.1:5000/valve/v3' , handlePump); };
  timer = setInterval( function() { makeRequest('http://127.0.0.1:5000/dht' , handleDHT) ;} , 500 ); 
  
  var count = 0;
  
  function makeRequest(url , callback) {
    if (window.XMLHttpRequest) { // Mozilla, Safari, ...
      httpRequest = new XMLHttpRequest();
    } else if (window.ActiveXObject) { // IE
      try {
        httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
      } 
      catch (e) {
        try {
          httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
        } 
        catch (e) {}
      }
    }

    if (!httpRequest) {
      alert('Giving up :( Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = callback;
    httpRequest.open('GET' , url);
    httpRequest.send();
  }

  function handlePump() {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200) {
//		alert(httpRequest.responseText);	
        date = JSON.parse(httpRequest.responseText);
		document.getElementById(date.valveId).setAttribute('src', date.newSrc);
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
  
   function handleDHT() {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200) {
//		alert(httpRequest.responseText);	
		date = JSON.parse(httpRequest.responseText);
		document.getElementById("temp").innerHTML = date.temperatura +'ºC';
		document.getElementById("umid").innerHTML = date.umidade + '%';
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
  
  function counter() {
	count = count + 1;
	console.log(count);	  
  }
