package
{
    import flash.display.DisplayObjectContainer;
    import flash.display.MovieClip;
    import flash.display.Sprite;
    import flash.events.Event;
    import flash.events.IOErrorEvent;
    import flash.events.SecurityErrorEvent;
    
    import ru.dai2.events.RPCErrorEvent;
    import ru.dai2.events.RPCEvent;
    import ru.dai2.rpc.OffersService;
    import ru.dai2.ui.OfferBanner;
    import ru.dai2.ui.OffersWindow;
    import ru.dai2.ui.OffersWindowBase;
    
    [SWF(width = "800", height = "600", frameRate = "30", backgroundColor = "#FF00FF")]	
    public class OffersLib extends MovieClip
    {
        private var _offersService : OffersService = null;
        private var rewardCallback : Function = null;
        
        public function OffersLib()
        {
            this.visible = false;
            //XXX
            /*var rewardCallback : Function = function(payment : int) : String {
            //return (String)(payment);
            return "Шоколадка";
            };
            initOffers("8", "111555", rewardCallback);
            var w : OffersWindow = createOffersWindow(800, 600);
            addChild(w);*/
        }
        
        public function initOffers(appId : String, uid : String, secret: String, rewardCallback : Function, platform : String = "VKONTAKTE", userInfo : Object = null) : OffersService 
        {
            this.rewardCallback = rewardCallback;
            _offersService = new OffersService(appId, uid, secret, platform, userInfo);
            return _offersService;
        }
        
        public function get offersService() : OffersService
        {
            return this._offersService;
        }
        
        public function createOffersWindow(stageWidth : int, stageHeight : int) : OffersWindow
        {
            return OffersWindow.create(offersService, stageWidth, stageHeight, rewardCallback);
            
        }
        
        public function createOfferBanner(x : int, y : int, delay : int) : OfferBanner
        {
            return OfferBanner.create(x, y, delay, offersService, rewardCallback);
        }

    }
}