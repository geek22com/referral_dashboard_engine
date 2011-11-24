package com.heymoose.old.events
{

	import flash.events.Event;

	public class RPCEvent extends Event
	{
		public static const OFFERS_LOADED:String = "offersLoaded";

		public static const ACCEPTANCES_LOADED:String = "acceptancesLoaded";


		public function RPCEvent( type:String )
		{
			super( type, false, false );
		}
	}
}