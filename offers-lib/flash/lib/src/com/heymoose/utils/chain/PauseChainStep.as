/**
 * Created by IntelliJ IDEA.
 * User: Sokolov Stanislav
 * Date: 9/13/11
 * Time: 11:36 AM
 */
package com.heymoose.utils.chain
{

	import com.heymoose.utils.chain.classes.BaseChainStep;
	import com.heymoose.utils.chain.classes.IAutonomousChainStep;

	import flash.utils.setTimeout;

	public class PauseChainStep extends BaseChainStep implements IAutonomousChainStep
	{
		public function PauseChainStep()
		{
		}


		public function doProceed():void
		{
			setTimeout( complete, 200 );
		}
	}
}
