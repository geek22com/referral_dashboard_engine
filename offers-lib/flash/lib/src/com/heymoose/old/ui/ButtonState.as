package com.heymoose.old.ui
{

	import flash.display.GradientType;
	import flash.display.MovieClip;
	import flash.display.Shape;
	import flash.display.SpreadMethod;
	import flash.geom.Matrix;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;

	public class ButtonState extends MovieClip
	{

		private var upColor:uint = 0xFFCC00;
		private var overColor:uint = 0xCCFF00;
		private var downColor:uint = 0x00CCFF;

		public static const DOWN:String = "down";
		public static const OVER:String = "over";
		public static const UP:String = "up";
		public static const HIT_TEST:String = "hitTest";
		public static const GRAY:String = "gray";
		public static const GREEN:String = "green";

		private var w:uint = 0;
		private var h:uint = 0;


		public function ButtonState( lbl:String, x:Number, y:Number, width:Number, height:Number, cornerSize:Number, state:String, palette:String, fontSize:Number = 12 )
		{
			this.x = x;
			this.y = y;
			this.w = width;
			this.h = height;

			var bg:Shape = new Shape()
			var fillType:String = GradientType.LINEAR;
			var colors:Array = [0x000000, 0xffffff];
			if ( palette == GREEN )
			{
				colors = [0x9ee50e, 0x74ae04];
				if ( state == OVER )
				{
					colors = [0xa4ec0f, 0x80c104];
				} else if ( state == DOWN )
				{
					colors = [0x74ae04, 0x9ee50e];
				}
			} else if ( palette == GRAY )
			{
				colors = [0xf0f0f0,0xcbcbcb];
				if ( state == OVER )
				{
					colors = [0xfbfbfb, 0xe0e0e0];
				} else if ( state == DOWN )
				{
					colors = [0xcbcbcb, 0xf0f0f0]
				}
			}
			var alphas:Array = [1, 1];
			var ratios:Array = [0x00, 0xFF];
			var matr:Matrix = new Matrix();
			matr.createGradientBox( width, height, Math.PI / 2, 0, 0 );
			var spreadMethod:String = SpreadMethod.PAD;
			bg.graphics.beginGradientFill( fillType, colors, alphas, ratios, matr, spreadMethod );
			if ( palette == GRAY )
			{
				bg.graphics.lineStyle( 1, 0xd3d3d3, 1.0, true );
			}
			bg.graphics.drawRoundRect( 0, 0, this.w, this.h, cornerSize );
			bg.graphics.endFill();
			this.addChild( bg );

			var tf:TextFormat = new TextFormat();
			if ( palette == GREEN )
			{
				tf.color = 0xffffff;
			} else if ( palette == GRAY )
			{
				tf.color = 0x555555;
			}
			tf.font = OffersWindowBase.APP_FONT;
			tf.size = fontSize;
			tf.align = TextFormatAlign.CENTER;
			//tf.

			var txt:TextField = new TextField();
			txt.text = lbl;
			var textHeight:Number = fontSize + fontSize / 2;
			var topIndent:Number = (height - textHeight) / 2;
			txt.x = 0;
			txt.y = topIndent;
			txt.width = bg.width;
			txt.height = bg.height - topIndent;
			txt.setTextFormat( tf );
			this.addChild( txt );
		}
	}

}

