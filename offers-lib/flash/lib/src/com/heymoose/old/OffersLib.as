package
com.heymoose.old
{

	import com.heymoose.old.rpc.OffersService;
	import com.heymoose.old.ui.OfferBanner;
	import com.heymoose.old.ui.OffersWindow;

	import flash.display.MovieClip;

	[SWF(width = "800", height = "600", frameRate = "30", backgroundColor = "#FF00FF")]
	public class OffersLib extends MovieClip
	{
		private var _offersService:OffersService = null;
		private var rewardCallback:Function = null;


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


		public function initOffers( appId:String, uid:String, secret:String, rewardCallback:Function, platform:String = "VKONTAKTE", userInfo:Object = null ):OffersService
		{
			this.rewardCallback = rewardCallback;
			_offersService = new OffersService( appId, uid, secret, platform, userInfo );
			return _offersService;
		}


		public function get offersService():OffersService
		{
			return this._offersService;
		}


		public function createOffersWindow( stageWidth:int, stageHeight:int ):OffersWindow
		{
			return OffersWindow.create( offersService, stageWidth, stageHeight, rewardCallback );

		}


		public function createOfferBanner( x:int, y:int, delay:int ):OfferBanner
		{
			return OfferBanner.create( x, y, delay, offersService, rewardCallback );
		}

	}
}