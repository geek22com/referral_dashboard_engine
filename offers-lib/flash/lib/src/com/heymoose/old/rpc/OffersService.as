package com.heymoose.old.rpc
{

	import com.adobe.json.serialization.JSON;
	import com.heymoose.old.events.RPCErrorEvent;
	import com.heymoose.old.events.RPCEvent;
	import com.heymoose.utils.crypto.MD5;

	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLLoader;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.net.URLRequestMethod;
	import flash.net.URLVariables;

	[Event(name=RPCEvent.OFFERS_LOADED, type="com.heymoose.old.events.RPCEvent")]
	[Event(name=RPCEvent.ACCEPTANCES_LOADED, type="com.heymoose.old.events.RPCEvent")]
	[Event(name=IOErrorEvent.IO_ERROR, type="flash.events.IOErrorEvent")]
	[Event(name=SecurityErrorEvent.SECURITY_ERROR, type="flash.events.SecurityErrorEvent")]
	[Event(name=RPCErrorEvent.RPC_ERROR, type="com.heymoose.old.events.RPCErrorEvent")]
	public class OffersService extends EventDispatcher
	{
		private var baseUrl:String;
		private var fullUrl:String;
		private var appId:String;
		private var uid:String;
		private var secret_key:String;
		private var platform:String;

		//Offers
		private var _offers:Array = null;
		private var _acceptances:Array = null;
		private var userInfo:Object = null;


		public function OffersService( appId:String, uid:String, secret:String, platform:String = "VKONTAKTE", userInfo:Object = null )
		{
			this.baseUrl = "http://heymoose.com/rest_api/api";
			this.appId = appId;
			this.uid = uid;
			this.secret_key = secret;
			this.userInfo = userInfo;
			this.platform = platform;
		}


		public function get offers():Array
		{
			return this._offers;
		}


		public function get acceptances():Array
		{
			return this._acceptances;
		}


		public function execute( method:String, params:Object, cb:Function ):void
		{
			params.app_id = String( appId );
			params.method = method;
			params.uid = uid;
			params.format = "JSON";
			//params.nocache = Math.random();

			params.sig = generateSig( params );

			var request:URLRequest = new URLRequest( baseUrl );
			request.method = URLRequestMethod.GET;
			request.data = new URLVariables();
			for ( var k:String in params )
			{
				request.data[k] = params[k];
			}

			var loader:URLLoader = new URLLoader();
			loader.dataFormat = URLLoaderDataFormat.TEXT;

			var completeHandler:Function = function( event:Event ):void
			{
				var jsonObj:Object = null;
				try
				{
					trace( "Received : " + loader.data );
					jsonObj = JSON.decode( loader.data );
				} catch ( e:* )
				{
					dispatchEvent( new RPCErrorEvent( RPCErrorEvent.RPC_ERROR, "Error while parsing response" ) );
				}
				if ( cb != null )	cb( jsonObj );
				cleanup();
			};
			var ioErrorHandler:Function = function( event:IOErrorEvent ):void
			{
				dispatchEvent( event );
				cleanup();
			};
			var securityErrorHandler:Function = function( event:SecurityErrorEvent ):void
			{
				dispatchEvent( event );
				cleanup();
			};
			var cleanup:Function = function():void
			{
				loader.removeEventListener( Event.COMPLETE, completeHandler );
				loader.removeEventListener( IOErrorEvent.IO_ERROR, ioErrorHandler );
				loader.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler );
			};
			loader.addEventListener( Event.COMPLETE, completeHandler );
			loader.addEventListener( IOErrorEvent.IO_ERROR, ioErrorHandler );
			loader.addEventListener( SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler );
			loader.load( request );
		}


		public function loadOffers():void
		{
			var userInfo:Object = new Object;
			if ( this.userInfo != null )
			{
				if ( this.userInfo.user_sex != null )
				{
					userInfo.user_sex = this.userInfo.user_sex;
				}
				if ( this.userInfo.user_birthyear != null )
				{
					userInfo.user_birthyear = this.userInfo.user_birthyear;
				}
			}
			var cb:Function = function( response:Object ):void
			{
				if ( response == null )
				{
					dispatchEvent( new RPCErrorEvent( RPCErrorEvent.RPC_ERROR,
							"getOffers returned null" ) );
					return;
				}
				if ( response.exception != null )
				{
					dispatchEvent( new RPCErrorEvent( RPCErrorEvent.RPC_ERROR,
							"exception in getOffers : " + response.exception ) );
					return;
				}
				if ( response.result is Array )
				{
					_offers = response.result as Array;
					dispatchEvent( new RPCEvent( RPCEvent.OFFERS_LOADED ) );
				} else
				{
					dispatchEvent( new RPCErrorEvent( RPCErrorEvent.RPC_ERROR,
							"getOffers must return array" ) );
				}
			};
			execute( "getOffers", userInfo, cb );
		}


		/*
		 public function loadAcceptances() : void
		 {

		 var cb : Function = function(response : Object) : void {
		 if (response == null) {
		 dispatchEvent(new RPCErrorEvent(RPCErrorEvent.RPC_ERROR,
		 "getAcceptedOffers returned null"));
		 return;
		 }
		 if (response.exception != null) {
		 dispatchEvent(new RPCErrorEvent(RPCErrorEvent.RPC_ERROR,
		 "exception in getAcceptedOffers : " + response.exception));
		 return;
		 }
		 if (response.result is Array) {
		 _acceptances = response.result as Array;
		 dispatchEvent(new RPCEvent(RPCEvent.ACCEPTANCES_LOADED));
		 } else {
		 dispatchEvent(new RPCErrorEvent(RPCErrorEvent.RPC_ERROR,
		 "getAcceptedOffers must return array"));
		 }
		 };
		 execute("getAcceptedOffers", {}, cb);
		 }*/

		public function loadSingleOffer( onSuccess:Function, onError:Function ):void
		{
			var params:Object = new Object;
			if ( this.userInfo != null )
			{
				if ( this.userInfo.user_sex != null )
				{
					params.user_sex = this.userInfo.user_sex;
				}
				if ( this.userInfo.user_birthyear != null )
				{
					params.user_birthyear = this.userInfo.user_birthyear;
				}
				params.limit = 1;
			}
			var cb:Function = function( response:Object ):void
			{
				var errorEvent:RPCErrorEvent;
				if ( response == null )
				{
					errorEvent = new RPCErrorEvent( RPCErrorEvent.RPC_ERROR,
							"getOffers returned null" );
					onError( errorEvent );
					return;
				}
				if ( response.exception != null )
				{
					errorEvent = new RPCErrorEvent( RPCErrorEvent.RPC_ERROR,
							"exception in getOffers : " + response.exception );
					onError( errorEvent );
					return;
				}
				if ( response.result is Array && response.result.length > 0 )
				{

					onSuccess( (response.result as Array)[0] );
				} else
				{
					errorEvent = new RPCErrorEvent( RPCErrorEvent.RPC_ERROR,
							"getOffers must return array" );
					onError( errorEvent );
				}
			};
			execute( "getOffers", params, cb );
		}


		public function generateSig( params:Object ):String
		{
			return MD5.encrypt( sortedParams( params ) + this.secret_key );
		}


		public function do_offer_for( offer_id:String ):String
		{
			var request:URLRequest = new URLRequest( this.baseUrl );
			request.method = URLRequestMethod.GET;
			request.data = new URLVariables();

			request.data['method'] = "doOffer";
			request.data['app_id'] = this.appId;
			request.data['offer_id'] = offer_id;
			request.data['uid'] = this.uid;
			request.data['platform'] = this.platform;
			request.data['sig'] = generateSig( request.data );

			var url:String = this.baseUrl + "?" + request.data.toString();
			return url;
		}


		public function sortedParams( dct:Object ):String
		{
			var Keys:Array = this.extractKeysFrom( dct );
			Keys.sort();

			var res:String = "";
			for each ( var thisKey:* in Keys )
			{
				res += thisKey.toString();
				res += "=";
				res += dct[thisKey].toString();
			}
			return res;
		}


		private function extractKeysFrom( source:Object ):Array
		{
			var output:Array = [];

			for ( var prop:* in source )
			{
				output.push( prop );
			}
			return output;
		}

	}
}
