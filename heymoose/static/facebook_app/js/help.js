(function() {
    $(function() {
        $("#b-help__form").submit(function(e) {
            e.preventDefault();
            var data = $(this).serializeObject();
            var params = {
                message: data.message,
                name: data.giftName,
                caption: "HeyMoose",
                description: "sent you a gift. Click 'like' to show your appreciation!",
                picture: data.gift,
                method: "post",
                link: app_domain,
                actions: [{"name":"Send a Gift", "link": ""}]
            };
            $.post("/facebook_help", data);
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
