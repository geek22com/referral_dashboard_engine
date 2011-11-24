/**
 * Created by IntelliJ IDEA.
 * User: Sokolov Stanislav
 * Date: 9/20/11
 * Time: 8:24 PM
 */
package com.heymoose.utils.chain
{

	import com.heymoose.utils.chain.classes.BaseCompositeChain;
	import com.heymoose.utils.chain.classes.ChainType;

	import flash.events.IEventDispatcher;

	public class Chain extends BaseCompositeChain
	{
		// ========================================
		// protected properties
		// ========================================

		/**
		 * Backing variable for <code>dispatcher</code> getter/setter.
		 */
		protected var _dispatcher:IEventDispatcher;

		// ========================================
		// public properties
		// ========================================

		/**
		 * Target Event dispatcher.
		 */
		public function get dispatcher():IEventDispatcher
		{
			return _dispatcher;
		}


		public function set dispatcher( value:IEventDispatcher ):void
		{
			_dispatcher = value;
		}


		// ========================================
		// constructor
		// ========================================

		/**
		 * Constructor.
		 */
		public function Chain( dispatcher:IEventDispatcher, mode:String = ChainType.SEQUENCE, stopOnError:Boolean = true )
		{
			super( mode, stopOnError );

			this.dispatcher = dispatcher;
		}


		// ========================================
		// public methods
		// ========================================

		/**
		 * Add an CommandChainStep to this EventChain.
		 */
		public function addAsyncCommand( asyncMethod:Function, asyncMethodArgs:Array = null, resultHandler:Function = null, faultHandler:Function = null, handlerArgs:Array = null ):Chain
		{
			addStep( new AsyncCommandChainStep( asyncMethod, asyncMethodArgs, resultHandler, faultHandler, handlerArgs ) );
			return this;
		}


		/**
		 * Add an CommandChainStep to this EventChain.
		 */
		public function addFunction( functionRef:Function, functionArgArray:Array = null, functionThisArg:* = null ):Chain
		{
			addStep( new FunctionChainStep( functionRef, functionArgArray, functionThisArg ) );
			return this;
		}


		/**
		 * Add an CommandChainStep to this EventChain.
		 */
		public function addPause():Chain
		{
			addStep( new PauseChainStep() );
			return this;
		}
	}
}
