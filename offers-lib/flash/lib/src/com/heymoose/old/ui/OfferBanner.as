package com.heymoose.old.ui
{

	import com.heymoose.old.events.OfferEvent;
	import com.heymoose.old.rpc.OffersService;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.TimerEvent;
	import flash.utils.Timer;

	[Event(name = OfferEvent.OFFER_CLICKED, type = "com.heymoose.old.events.OfferEvent")]
	public class OfferBanner extends MovieClip
	{
		private var timer:Timer;
		private var interval:int;
		private var offersService:OffersService;
		private var rewardCallBack:Function;
		private var buttonText:String;
		private var offerElem:OfferElement;
		private var offer:Object;
		private var active:Boolean = false;


		public function OfferBanner( x:int, y:int, interval:int, offersService:OffersService, rewardCallBack:Function )
		{
			this.offersService = offersService;
			this.x = x;
			this.y = y;
			this.interval = interval;
			this.buttonText = buttonText;
			this.rewardCallBack = rewardCallBack;
			this.timer = new Timer( interval, 0 );
			this.timer.addEventListener( TimerEvent.TIMER, onTimer );
			this.addEventListener( Event.ADDED_TO_STAGE, onAddedToStage );
			this.addEventListener( Event.REMOVED_FROM_STAGE, onRemovedFromStage );
		}


		public function getOffersService():OffersService
		{
			return this.offersService;
		}


		private function onAddedToStage( e:Event ):void
		{
			active = true;
			loadOffer();
			timer.start();
		}


		private function onRemovedFromStage( e:Event ):void
		{
			//Reset offer
			active = false;
			timer.stop();
			this.offer = null;
			setOffer( null );
		}


		private function onTimer( e:Event ):void
		{
			loadOffer();
		}


		private function loadOffer():void
		{
			offersService.loadSingleOffer(
					function( o:Object ):void
					{
						setOffer( o );
					},
					function( e:Event ):void
					{
						setOffer( null );
					} );
		}


		private function setOffer( o:Object ):void
		{
			if ( offerElem != null )
			{
				removeChild( offerElem );
				offerElem = null;
			}

			if ( o != null )
			{
				var payment:int = o.payment;
				var buttonText:String = this.rewardCallBack( payment );
				offerElem = new OfferElement( this, o, buttonText, null );
				addChild( offerElem );
			}
		}


		public static function create( x:int, y:int, delay:int, offersService:OffersService, rewardCallbak:Function ):OfferBanner
		{
			var b:OfferBanner = new OfferBanner( x, y, delay, offersService, rewardCallbak );
			return b;
		}

	}
}