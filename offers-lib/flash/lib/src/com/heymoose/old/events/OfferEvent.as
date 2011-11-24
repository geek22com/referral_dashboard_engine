package com.heymoose.old.events
{

	import flash.events.Event;

	public class OfferEvent extends Event
	{
		public static const OFFER_CLICKED:String = "offerClicked";
		public static const ACCEPTANCE_CLICKED:String = "acceptanceClicked";

		private var _offer:Object = null;
		private var _key:String = null;


		public function OfferEvent( type:String, offer:Object, key:String = null )
		{
			super( type, false, false );
			this._offer = offer;
			this._key = key;
		}


		public function get offer():Object
		{
			return this._offer;
		}


		public function get key():String
		{
			return this._key;
		}
	}
}