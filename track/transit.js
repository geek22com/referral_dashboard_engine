;(function() {
	if(document.getElementsByClassName) {
		heymooseGetElementsByClass = function(classList, node) {    
			return (node || document).getElementsByClassName(classList)
		}
	} else {
		heymooseGetElementsByClass = function(classList, node) {
			var node = node || document,
			list = node.getElementsByTagName('*'), 
			length = list.length,
			classArray = classList.split(/\s+/), 
			classes = classArray.length,
			result = [], i,j
			for(i = 0; i < length; i++) {
				for(j = 0; j < classes; j++)  {
					if(list[i].className.search('\\b' + classArray[j] + '\\b') != -1) {
						result.push(list[i])
						break
					}
				}
			}
			return result
		}
	};
	
	function heymooseAddHandler(object, event, handler) {
		if (typeof object.addEventListener != 'undefined')
			object.addEventListener(event, handler, false);
		else if (typeof object.attachEvent != 'undefined')
			object.attachEvent('on' + event, handler);
	}
	
	heymooseAddHandler(window, 'load', function() {
		try {
			var matchToken = /_hm_token=([a-z0-9]{32})/i.exec(document.location.href);
			var token = (matchToken && matchToken.length > 1) ? matchToken[1] : null;
			if (!token) return;
			
			var matchTtl = /_hm_ttl=(\d+)/i.exec(document.location.href);
			var ttl = (matchTtl && matchTtl.length > 1) ? matchTtl[1] : 180;
			
			var params = '_hm_token=' + token + '&_hm_ttl=' + ttl;
			
			var links = heymooseGetElementsByClass('heymoose-transit-link', document.body);
			for (var i = 0; i < links.length; ++i) {
				var href = links[i].href;
				var pos = href.indexOf('#');
				if (pos < 0) pos = href.length;
				var delim = href.indexOf('?') < 0 ? '?' : '&';
				links[i].href = href.substring(0, pos) + delim + params + href.substring(pos);
			}
		}
		catch (e) { }
	});
})();