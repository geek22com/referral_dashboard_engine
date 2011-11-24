package com.heymoose.old.events
{

	import flash.events.ErrorEvent;

	public class RPCErrorEvent extends ErrorEvent
	{
		public static const RPC_ERROR:String = "jsonError";


		public function RPCErrorEvent( type:String, text:String )
		{
			super( type, false, false, text );
		}
	}
}