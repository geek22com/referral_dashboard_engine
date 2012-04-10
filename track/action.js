;(function() {
	function heymooseGetDomain() {
		var match = /((?:\.?[^\.\s]+){2})$/.exec(document.domain);
		if (match && match.length > 1) {
			var domain2 = match[1];
			if (domain2.substring(0, 1) != '.')
				domain2 = '.' + domain2;
			return domain2;
		}
	}
	
	function heymooseGetCookie(name) {
		var cookie = ' ' + document.cookie;
		var search = ' ' + name + '=';
		var offset = cookie.indexOf(search);
		var end = 0;
		
		if (offset != -1) {
			offset += search.length;
			end = cookie.indexOf(';', offset);
			if (end == -1)
				end = cookie.length;
			return cookie.substring(offset, end);
		}
	}
	
	function heymooseSetCookie(name, value, domain, days) {
		if (days) {
			var date = new Date();
			date.setTime(date.getTime() + (days*24*60*60*1000));
			var expires = date.toGMTString();
		}
		else
			var expires = '';
			
		document.cookie = name + '=' + value +
			(expires ? '; expires=' + expires : '') +
			'; path=/' +
			(domain ? '; domain=' + domain : '');
	}
	
	function heymooseDeleteCookie(name, domain) {
		heymooseSetCookie(name, '', domain, -1);
	}
	
	function heymooseGetParam(name) {
		var scriptName = 'action.js';
		var regexParam = new RegExp(name + '=([^&]+)');
		var scripts = document.getElementsByTagName('script');
		
		for (var i = 0; i < scripts.length; ++i) {
			var script = scripts[i];
			var src = script.getAttribute('src');
			if (!src || src.indexOf(scriptName) < 0) continue;
			
			var match = src.match(regexParam);
			if (match && match.length > 1)
				return match[1];
		}
	}
	
	function heymooseUrlNoCache(url) {
		var delim = url.indexOf('?') < 0 ? '?' : '&';
		return url + delim + 'nocache=' + Math.round(Math.random()*100000);
	}
	
	function heymooseCreatePixel(url) {
		if (!url) return;
		try {
			var d = document, b = d.body;
			var img = d.createElement('img');
			img.src = heymooseUrlNoCache(url);
			with (img.style) { position = 'absolute'; width = '0px'; height = '0px'; }
			b.insertBefore(img, b.firstChild);
		} catch(e) { }
	}
	
	function heymooseCreateScript(url) {
		if (!url) return;
		try {
			var d = document;
			var script = d.createElement('script');
			script.type = 'text/javascript'; script.async = true;
			script.src = heymooseUrlNoCache(url);
			var firstScript = d.getElementsByTagName('script')[0];
			firstScript.parentNode.insertBefore(script, firstScript);
		} catch(e) { }
	}
	
	var domain = heymooseGetDomain();
	if (!domain) return;
	
	var token = heymooseGetCookie('heymoose_token');
	if (!token) return;
	
	var offer = heymooseGetParam('offer');
	var transactionId = heymooseGetParam('transaction_id');
	if (!offer || !transactionId) return;
	
	//var host = 'http://localhost:8989';
	var host = 'http://partner.heymoose.com';
	var url = host + '/api/?method=reportAction' +
		'&token=' + token +
		'&offer=' + offer +
		'&transaction_id=' + transactionId;
	heymooseCreateScript(url);
	//heymooseDeleteCookie('heymoose_token', domain);
})();