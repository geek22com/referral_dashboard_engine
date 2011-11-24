package com.heymoose.old.ui
{

	import flash.display.GradientType;
	import flash.display.MovieClip;
	import flash.display.Shape;
	import flash.display.SpreadMethod;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Matrix;

	[Event(name=Event.CHANGE, type="flash.events.Event")]
	public class VScrollBar extends MovieClip
	{
		private static const TRACK_WIDTH:int = 4;
		private static const THUMB_ARROW_SIZE:int = 4;
		private static const THUMB_ARROW_OFFSET:int = 10;
		private static const THUMB_CORNER_SIZE:int = 10;

		private var _min:Number = 0;
		private var _max:Number = 0;
		private var _thumbHeight:Number = 300;
		private var _thumbWidth:Number = 16;
		private var _value:Number = 0;

		private var track:Shape = null;
		private var thumb:Sprite = null;
		private var thumbUp:Shape = null;
		private var thumbOver:Shape = null;
		private var thumbDown:Shape = null;

		private static const STATE_UP:int = 1;
		private static const STATE_OVER:int = 2;
		private static const STATE_DOWN:int = 3;

		private var thumbState:int = STATE_UP;

		private var dragging:Boolean = false;
		private var dragStartY:int = 0;
		private var dragStartThumbY:int = 0;
		private var dragStartValue:Number = 0;

		private var _width:int = 0;
		private var _height:int = 0;


		public function VScrollBar()
		{
		}


		public function create( x:int, y:int, width:int, height:int ):void
		{
			this.x = x;
			this.y = y;
			_width = width;
			_height = height;
			_thumbWidth = width;
			//_thumbHeight
			track = new Shape();
			track.graphics.beginFill( 0xCBCBCB );
			track.graphics.drawRoundRect( width / 2 - TRACK_WIDTH / 2, y,
					TRACK_WIDTH, height, TRACK_WIDTH, TRACK_WIDTH );
			addChild( track );
			createThumb();
			updateThumbPos();
		}


		public function createThumb():void
		{
			thumb = new Sprite();
			addChild( thumb );
			thumb.addEventListener( MouseEvent.MOUSE_OVER, thumb_MouseOver );
			thumb.addEventListener( MouseEvent.MOUSE_OUT, thumb_MouseOut );
			thumb.addEventListener( MouseEvent.MOUSE_DOWN, thumb_MouseDown );
			thumb.addEventListener( MouseEvent.MOUSE_UP, thumb_MouseUp );
			thumb.addEventListener( MouseEvent.MOUSE_MOVE, thumb_MouseMove );
			recreateThumbStates();
			updateThumbPos();

		}


		private function thumb_MouseOver( e:MouseEvent ):void
		{
			thumbState = STATE_OVER;
			updateThumbState();
		}


		private function thumb_MouseOut( e:MouseEvent ):void
		{
			thumbState = STATE_UP;
			updateThumbState();
			dragging = false;
		}


		private function thumb_MouseDown( e:MouseEvent ):void
		{
			thumbState = STATE_DOWN;
			updateThumbState();
			dragging = true;
			dragStartY = e.stageY;
			dragStartThumbY = thumb.y;
			dragStartValue = _value;
		}


		private function thumb_MouseUp( e:MouseEvent ):void
		{
			thumbState = STATE_UP;
			updateThumbState();
			dragging = false;
		}


		private function thumb_MouseMove( e:MouseEvent ):void
		{
			if ( dragging )
			{
				var move:int = e.stageY - dragStartY;
				var newThumbY:int = dragStartThumbY + move;

				var heightInterval:int = height - thumbHeight;
				if ( newThumbY < 0 ) newThumbY = 0;
				if ( newThumbY > heightInterval ) newThumbY = heightInterval;

				var newValue:int = (heightInterval > 0) ? newThumbY * (_max - _min) / heightInterval + min : 0;
				value = newValue;
				dispatchEvent( new Event( Event.CHANGE ) );
			}
			//thumbState = STATE_UP;
			//updateThumbState();
		}


		private function recreateThumbStates():void
		{
			if ( thumbUp != null ) thumb.removeChild( thumbUp );
			//thumbUp = new Shape();
			thumbUp = createThumbState( STATE_UP );
			thumb.addChild( thumbUp );
			thumbUp.visible = false;

			if ( thumbOver != null ) thumb.removeChild( thumbOver );
			//thumbOver = new Shape();
			thumbOver = createThumbState( STATE_OVER );
			thumb.addChild( thumbOver );
			thumbOver.visible = false;

			if ( thumbDown != null ) thumb.removeChild( thumbDown );
			//thumbDown = new Shape();
			thumbDown = createThumbState( STATE_DOWN );
			thumb.addChild( thumbDown );
			thumbDown.visible = false;

			updateThumbState();
		}


		private function createThumbState( state:int ):Shape
		{
			var shape:Shape = new Shape();
			var fillType:String = GradientType.LINEAR;
			var colors:Array;
			if ( state == STATE_UP )
			{
				colors = [0x8d8d8d, 0x727272];
			} else if ( state == STATE_OVER )
			{
				colors = [0x959595, 0x7c7c7c];
			} else if ( state == STATE_DOWN )
			{
				colors = [0x7c7c7c, 0x959595];
			}
			var alphas:Array = [1, 1];
			var ratios:Array = [0x00, 0xFF];
			var matr:Matrix = new Matrix();
			matr.createGradientBox( _thumbWidth, _thumbHeight, 0, 0, 0 );
			var spreadMethod:String = SpreadMethod.PAD;
			shape.graphics.beginGradientFill( fillType, colors, alphas, ratios, matr, spreadMethod );
			shape.graphics.drawRoundRect( 0, 0, _thumbWidth, _thumbHeight, THUMB_CORNER_SIZE, THUMB_CORNER_SIZE );

			var thumbCenter:int = _thumbWidth / 2;
			shape.graphics.beginFill( 0xCCCCCC );
			shape.graphics.moveTo( thumbCenter, THUMB_ARROW_OFFSET );
			shape.graphics.lineTo( thumbCenter + THUMB_ARROW_SIZE, THUMB_ARROW_OFFSET + THUMB_ARROW_SIZE );
			shape.graphics.lineTo( thumbCenter - THUMB_ARROW_SIZE, THUMB_ARROW_OFFSET + THUMB_ARROW_SIZE );
			shape.graphics.lineTo( thumbCenter, THUMB_ARROW_OFFSET );

			shape.graphics.moveTo( thumbCenter, _thumbHeight - THUMB_ARROW_OFFSET );
			shape.graphics.lineTo( thumbCenter + THUMB_ARROW_SIZE, _thumbHeight - THUMB_ARROW_OFFSET - THUMB_ARROW_SIZE );
			shape.graphics.lineTo( thumbCenter - THUMB_ARROW_SIZE, _thumbHeight - THUMB_ARROW_OFFSET - THUMB_ARROW_SIZE );
			shape.graphics.lineTo( thumbCenter, _thumbHeight - THUMB_ARROW_OFFSET );
			shape.graphics.endFill();
			return shape;
		}


		public function get min():Number
		{
			return _min;
		}


		public function set min( newValue:Number ):void
		{
			_min = newValue;
			updateThumbPos();
		}


		public function get max():Number
		{
			return _max;
		}


		public function set max( newValue:Number ):void
		{
			_max = newValue;
			updateThumbPos();
		}


		public function get value():Number
		{
			return _value;
		}


		public function set value( newValue:Number ):void
		{
			_value = newValue;
			updateThumbPos();
		}


		public function get thumbHeight():Number
		{
			return _thumbHeight;
		}


		public function set thumbHeight( newValue:Number ):void
		{
			_thumbHeight = newValue;
			recreateThumbStates();
		}


		private function updateThumbState():void
		{
			if ( thumbState == STATE_UP )
			{
				thumbUp.visible = true;
				thumbDown.visible = false;
				thumbOver.visible = false;
			} else if ( thumbState == STATE_OVER )
			{
				thumbOver.visible = true;
				thumbUp.visible = false;
				thumbDown.visible = false;
			} else if ( thumbState == STATE_DOWN )
			{
				thumbDown.visible = true;
				thumbUp.visible = false;
				thumbOver.visible = false;
			}
		}


		private function updateThumbPos():void
		{
			var interval:Number = max - min;

			if ( interval <= 0 )
			{
				thumb.visible = false;
			} else
			{
				thumb.visible = true;
			}

			if ( _value < _min )
				_value = min;

			if ( _value > max )
				_value = max;

			//XXX
			var heightInterval:int = height - thumbHeight;
			thumb.y = heightInterval * (_value - _min) / (_max - _min);
		}
	}
}