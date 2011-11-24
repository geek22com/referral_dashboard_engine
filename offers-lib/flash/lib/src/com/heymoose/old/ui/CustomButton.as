package com.heymoose.old.ui
{

	import flash.display.SimpleButton;

	public class CustomButton extends SimpleButton
	{

		public function CustomButton( label:String, x:Number, y:Number, width:Number, height:Number, cornerSize:Number, palette:String, textSize:uint = 12 )
		{
			downState = new ButtonState( label, x, y, width, height, cornerSize, ButtonState.DOWN, palette, textSize );
			overState = new ButtonState( label, x, y, width, height, cornerSize, ButtonState.OVER, palette, textSize );
			upState = new ButtonState( label, x, y, width, height, cornerSize, ButtonState.UP, palette, textSize );
			hitTestState = upState;
			useHandCursor = true;
		}
	}
}