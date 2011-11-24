package com.heymoose.old.ui
{

	import com.heymoose.old.events.RPCEvent;
	import com.heymoose.old.rpc.OffersService;

	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;

	public class OffersWindow extends OffersWindowBase
	{
		private var noOffers:TextField = null;


		public function OffersWindow( offersService:OffersService, rewardCallback:Function )
		{
			super( offersService, rewardCallback );
			offersService.addEventListener( RPCEvent.OFFERS_LOADED, offers_loaded );
		}


		public function getOffersService():OffersService
		{
			return this.offersService;
		}


		override protected function createWindow():void
		{
			super.createWindow();

			var tf:TextFormat = new TextFormat();
			tf.color = 0x555555;
			tf.font = OffersWindowBase.APP_FONT;
			tf.size = 15;
			tf.bold = true;
			tf.align = TextFormatAlign.CENTER;

			noOffers = new TextField();
			noOffers.text = "Нет доступных предложений";
			noOffers.x = 80;
			noOffers.y = 100;
			noOffers.width = WINDOW_WIDTH - 160;
			noOffers.height = 40;
			noOffers.setTextFormat( tf );
			noOffers.visible = false;
			frame.addChild( noOffers );

			scrollPane.visible = false;
		}


		private function offers_loaded( e:RPCEvent ):void
		{
			if ( scrollPane != null )
				fillOffers();
		}


		private function fillOffers():void
		{
			var a:Array = offersService.offers;
			var i:Object;
			var o:Object;
			var oe:OfferElement = null;
			var ea:Array = new Array();
			if ( a.length == 0 )
			{
				scrollPane.setElements( new Array() );
				noOffers.visible = true;
				scrollPane.visible = false;
			} else
			{
				for ( i in a )
				{
					o = a[i];
					var payment:int = o.payment;
					var buttonText:String = rewardCallback( payment );
					if ( buttonText != null && buttonText != "" )
					{
						oe = new OfferElement( this, o, buttonText );
						ea.push( oe );
					}
				}
				scrollPane.setElements( ea );
				noOffers.visible = false;
				scrollPane.visible = true;
			}
		}


		public static function create( offersService:OffersService, stageWidth:int, stageHeight:int, rewardCallbak:Function ):OffersWindow
		{
			var w:OffersWindow = new OffersWindow( offersService, rewardCallbak );
			w.createWindow();
			w.stageResized( stageWidth, stageHeight );
			if ( offersService.offers != null )
			{
				w.fillOffers();
			} else
			{
				w.offersService.loadOffers();
			}
			return w;
		}
	}
}