VK.init(function() {
	load_offers();
});

function load_offers(){
	var app_id = $('#happ_app_id').attr('value');
	var sig = $('#happ_sig').attr('value');
	var data = "app_id=" + app_id + "&sig=" + sig;
	$.ajax({
		type: "POST",		
		url: "http://heymoose.com:8080/get_offers",
		data : data,
		context: document.body,
		success: function(msg){
			$('#offer_list').append(msg);
		},
		error: function(){ 
			$('#offer_list').append("Извините, нет доступных предложений. Попробуйте позже");
		}
	});	
}
