(function() {
    $(function() {
        $("#b-help__form").submit(function(e) {
            $(".b-help_error__text").addClass("i-hidden");
            e.preventDefault();
            var data = $(this).serializeObject();
            if (!data.email || !data.comment)
                return;
            $.post("/facebook_help", data,
                function(data) {
                    obj = $.parseJSON(data);
                    if (obj){
                        for(var key in  obj){
                            $(".b-help_error__text").text(obj[key].toString());
                            $(".b-help_error__text").removeClass("i-hidden");
                            break;
                        }
                    }else{
                        $(".b-help_error__text").text("Спасибо, мы вам ответим.");
                        $(".b-help__email__input").val("");
                        $(".b-help__message__input").val("");
                        $(".b-help_error__text").removeClass("i-hidden");
                    }
            });
        });
    });
})();

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
