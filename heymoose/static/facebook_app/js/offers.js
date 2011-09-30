(function(){
    $(function() {
        $(".b-offer__form").submit(function(e) {
            e.preventDefault();
            var data = $(this).serializeObject();
            form = this;
            if (!data.submitted){
                $.post("/facebook_do_offer", data, function(data){
                    $('input[name=submitted]',form).val(12);
                    form.submit();
                });
                return false;
            }else{
                return true;
            }
        });
    });
})();

/* For ajax form submission */
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

