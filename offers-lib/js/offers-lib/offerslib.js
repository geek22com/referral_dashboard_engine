(function(){
	var base_url = "http://heymoose.com/rest_api/api";
	var secret = "26c10b40-47ae-416d-9788-b106c64a57d9";
	function getSortedParams(arr){
		// Setup Arrays
		var sortedKeys = new Array();

		// Separate keys and sort them
		for (var i in arr){
			sortedKeys.push(i);
		}
		sortedKeys.sort();

		// Reconstruct sorted obj based on keys
		var res = "";
		for (var i in sortedKeys){
			res += sortedKeys[i];
			res += "=";
			res += arr[sortedKeys[i]];
		}
		return res;
	};

 	function signedParams(params, secret){
		var sorted = getSortedParams(params);
		return calcMD5(sorted + secret);
		
	};

	function do_offer_for(offer_id, app_id, uid, platform)
	{
		params = {
			method : "doOffer",
			app_id : app_id,
			offer_id : offer_id,
			uid : uid,
			platform : platform
		};
		params.sig = signedParams(params, secret);
		var url = base_url + "?" + $.param(params);
		return url;

	};
	
	(function load_offers(appId, extId, user_info){
		var params = {
			method : "getOffers",
			app_id : appId,
			uid : extId,
			format : "HTML"
		};
		params.nocache = Math.random();
		if (user_info){
			params.user_sex = user_info.sex;
			params.user_birthdate = user_info.birthdate;
		}
		params.sig = signedParams(params, secret);

		var url = base_url + "?" + $.param(params); 
    	$('.b-maincontent').load(url);
	})(1,1,{'sex' : 1, 'birthdate' : "123213"});

})();
