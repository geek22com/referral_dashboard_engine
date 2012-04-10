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
	
	var domain = heymooseGetDomain();
	if (!domain) return;
	
	var matchToken = /_hm_token=([a-z0-9]{32})/i.exec(document.location.href);
	var token = (matchToken && matchToken.length > 1) ? matchToken[1] : null;
	if (!token) return;
	
	var matchTtl = /_hm_ttl=(\d+)/i.exec(document.location.href);
	var ttl = (matchTtl && matchTtl.length > 1) ? matchTtl[1] : 180;
	
	heymooseSetCookie('heymoose_token', token, domain, ttl);
})();