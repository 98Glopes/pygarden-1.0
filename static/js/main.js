 

  document.getElementById("v1").onclick = function() { makeRequest('/valve/v1' , handlePump); };
  document.getElementById("v2").onclick = function() { makeRequest('/valve/v2' , handlePump); };
  document.getElementById("v3").onclick = function() { makeRequest('/valve/v3' , handlePump); };
  timer = setInterval( function() { makeRequest('/timer' , handleTimer) ;} , 4000 ); 
  var img = ['imgv1','imgv2','imgv3']
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
//		console.log(httpRequest.responseText);	
        date = JSON.parse(httpRequest.responseText);
		document.getElementById(date.valveId).setAttribute('src', date.newSrc);
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
  
   function handleTimer() {
    if (httpRequest.readyState === 4) {
      if (httpRequest.status === 200) {
//		console.log(httpRequest.responseText);	
		date = JSON.parse(httpRequest.responseText);
		document.getElementById("temp").innerHTML = date.temperatura +'ºC';
		document.getElementById("umid").innerHTML = date.umidade + '%';
		for(var i=0; i<=2 ; i++)
		{
			var pump = document.getElementById(img[i]);
			if (pump.getAttribute('src')!=date.img_links[i])
			{
				pump.setAttribute('src', date.img_links[i]);
			}
		}
		
      } else {
        alert('There was a problem with the request.');
      }
    }
  }
  
  function counter() {
	count = count + 1;
	console.log(count);	  
  }
