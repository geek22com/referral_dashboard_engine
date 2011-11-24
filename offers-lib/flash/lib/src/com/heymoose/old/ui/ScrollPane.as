package com.heymoose.old.ui
{

	import flash.display.DisplayObject;
	import flash.display.MovieClip;
	import flash.display.Sprite;
	import flash.events.Event;

	public class ScrollPane extends MovieClip
	{
		private var scrollBar:VScrollBar = null;
		private var elements:Array = new Array();
		private var clips:Array = new Array();
		private var areaWidth:int = 0;
		private var areaHeight:int = 0;
		private var scrollHeight:int = 0;

		private static const ITEM_HEIGHT:int = 77;
		private static const ITEM_GAP:int = 5;
		private static const SCROLL_BAR_WIDTH:int = 16;


		public function ScrollPane()
		{
		}


		public function create( x:int, y:int, width:int, height:int ):void
		{
			this.x = x;
			this.y = y;
			areaWidth = width - SCROLL_BAR_WIDTH;
			areaHeight = height;
			scrollBar = new VScrollBar();
			scrollBar.create( width - SCROLL_BAR_WIDTH, 0, SCROLL_BAR_WIDTH, height );
			addChild( scrollBar );
			scrollBar.addEventListener( Event.CHANGE, scrollBar_change );
			updateScrollBar();

		}


		public function setElements( e:Array ):void
		{
			var i:Object;
			var d:DisplayObject;
			var x:int = 0;
			var cy:int = 0;

			//Clean up
			for ( i in elements )
			{
				removeChild( elements[i] );
				removeChild( clips[i] as DisplayObject );
				clips[i] = null;
			}
			clips.length = 0;
			elements.length = 0;
			scrollHeight = 0;

			for ( i in e )
			{
				d = e[i] as DisplayObject;
				d.x = x;
				d.y = cy;
				cy += ITEM_HEIGHT;
				addChild( d );
				scrollHeight = cy;
				cy += ITEM_GAP;
				elements.push( e[i] );
				var clip:Sprite = new Sprite();
				clip.graphics.beginFill( 0xFF0000, 1 );
				clip.graphics.drawRect( 0, 0, areaWidth, areaHeight );
				clip.visible = false;
				addChild( clip );
				clips.push( clip );
				d.mask = clip;
			}
			updateScrollBar();
		}


		private function scrollBar_change( e:Event ):void
		{
			var i:Object;
			var d:DisplayObject;
			var cy:int = 0;
			for ( i in elements )
			{
				d = elements[i] as DisplayObject;
				d.y = -scrollBar.value + cy;
				cy += ITEM_HEIGHT + ITEM_GAP;
			}
		}


		private function updateScrollBar():void
		{
			if ( scrollHeight <= areaHeight )
			{
				scrollBar.min = 0;
				scrollBar.max = 0;
				scrollBar.value = 0;
			} else
			{
				scrollBar.min = 0;
				scrollBar.max = scrollHeight - areaHeight;
				var th:int = areaHeight * areaHeight / scrollHeight;
				if ( th < 50 )
					th = 50;
				scrollBar.thumbHeight = th;
			}
		}
	}
}