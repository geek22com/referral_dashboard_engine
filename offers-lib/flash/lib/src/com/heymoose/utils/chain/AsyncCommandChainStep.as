/*
 * Copyright 2010 Swiz Framework Contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

package com.heymoose.utils.chain
{

	import com.heymoose.utils.chain.classes.BaseChainStep;
	import com.heymoose.utils.chain.classes.IAutonomousChainStep;

	import mx.messaging.messages.HTTPRequestMessage;

	import mx.rpc.AsyncToken;
	import mx.rpc.IResponder;
	import mx.rpc.events.FaultEvent;

	public class AsyncCommandChainStep extends BaseChainStep implements IResponder, IAutonomousChainStep
	{
		// ========================================
		// protected properties
		// ========================================

		/**
		 *
		 */
		protected var asyncMethod:Function;

		/**
		 *
		 */
		protected var asyncMethodArgs:Array;

		/**
		 *
		 */
		protected var resultHandler:Function;

		/**
		 *
		 */
		protected var faultHandler:Function;

		/**
		 *
		 */
		protected var handlerArgs:Array;

		// ========================================
		// constructor
		// ========================================

		public function AsyncCommandChainStep( asyncMethod:Function, asyncMethodArgs:Array = null, resultHandler:Function = null, faultHandler:Function = null, handlerArgs:Array = null )
		{
			this.asyncMethodArgs = asyncMethodArgs;
			this.asyncMethod = asyncMethod;
			this.resultHandler = resultHandler;
			this.faultHandler = faultHandler;
			this.handlerArgs = handlerArgs;
		}


		public function execute():void
		{
			var token:AsyncToken;

			if ( asyncMethodArgs != null )
				token = asyncMethod.apply( null, asyncMethodArgs );
			else
				token = asyncMethod();

			token.addResponder( this );
		}


		public function doProceed():void
		{
			execute();
		}


		/**
		 *
		 */
		public function result( data:Object ):void
		{
			if ( resultHandler != null )
			{
				if ( handlerArgs == null )
				{
					resultHandler( data );
				}
				else
				{
					resultHandler.apply( this, [ data ].concat( handlerArgs ) );
				}
			}

			complete();
		}


		/**
		 *
		 */
		public function fault( info:Object ):void
		{
			if ( faultHandler != null )
			{
				if ( handlerArgs == null )
				{
					faultHandler( info );
				}
				else
				{
					try
					{
						faultHandler( info );
					}
					catch( e:Error )
					{
						faultHandler.apply( null, [ info ].concat( handlerArgs ) );
					}
				}
			}
			{
				// Global trace handler
				var url:String = HTTPRequestMessage( FaultEvent( info ).token.message ).url
				var body:Object = HTTPRequestMessage( FaultEvent( info ).token.message ).body
				var text:String = info.statusCode + " "+ info.fault.faultCode + "\n\n";
				text += url + "\n";
				for ( var i:String in body )
				{
					text += i + ": " + body[i] + "\n"
				}
				trace( text )
			}

			error();
		}
	}
}