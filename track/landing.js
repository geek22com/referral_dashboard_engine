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
	
	var domain = heymooseGetDomain();
	if (!domain) return;
	
	var matchClickId = /_hm_click_id=(\d+)/i.exec(document.location.href);
	if (matchClickId && matchClickId.length > 1) {
		var clickId = matchClickId[1];
		heymooseSetCookie('click_id', clickId, domain, 180);
	}
})();