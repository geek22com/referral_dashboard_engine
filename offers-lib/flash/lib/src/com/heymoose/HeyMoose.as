/**
 * Created by IntelliJ IDEA.
 * User: Sokolov Stanislav
 * Date: 11/23/11
 * Time: 11:29 PM
 */
package com.heymoose
{

	import com.heymoose.utils.crypto.MD5;

	import mx.rpc.AsyncToken;
	import mx.rpc.http.HTTPService;

	public class HeyMoose
	{
		public static var _instance:HeyMoose;

		private var appId:int;
		private var secret:String;

		private var uid:String;

		private var platform:String;
		private var rewardCallback:Function;

		private var services:HTTPService;


		public function HeyMoose()
		{
		}


		public static function get instance():HeyMoose
		{
			if ( !HeyMoose._instance )
				HeyMoose._instance = new HeyMoose();
			return HeyMoose._instance
		}


		public function init( appId:int, secret:String, uid:String, platform:String, rewardCallback:Function ):void
		{
			this.appId = appId;
			this.secret = secret;
			this.uid = uid;
			this.platform = platform;
			this.rewardCallback = rewardCallback;

			services = new HTTPService();
			services.method = 'GET';
			services.resultFormat = 'text';
		}


		public function introducePerformer( sex:String, year:int ):AsyncToken
		{
			var params:Object = new Object();
			params['method'] = 'introducePerformer';
			params['sex'] = sex;
			params['year'] = year;
			return send( params );
		}


		public function getOffers( filter:String ):AsyncToken
		{
			var params:Object = new Object();
			params['method'] = 'getOffers';
			params['filter'] = filter;
			return send( params );
		}


		//////////////////////////////////////////
		// Atomic send
		//////////////////////////////////////////
		private function send( params:Object ):AsyncToken
		{
			params['format'] = 'JSON';
			params['platform'] = platform;
			params['app_id'] = appId;
			params['uid'] = uid;
			params['nocache'] = Math.random();
			params['sig'] = generateSig( params );

			services.url = "http://heymoose.com/rest_api/api"

			return services.send( params );
		}


		//////////////////////////////////////////
		// SIG Generator
		//////////////////////////////////////////
		private function generateSig( params:Object ):String
		{
			return MD5.encrypt( sortedParams( params ) + this.secret );
		}


		private function sortedParams( dct:Object ):String
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
