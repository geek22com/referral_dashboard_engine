package com.heymoose.old.ui
{

	import com.heymoose.old.events.OfferEvent;
	import com.heymoose.old.rpc.OffersService;

	import flash.display.MovieClip;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.net.*;

	[Event(name = OfferEvent.OFFER_CLICKED, type = "com.heymoose.old.events.OfferEvent")]
	[Event(name = Event.CLOSE, type = "flash.events.Event")]
	public class OffersWindowBase extends MovieClip
	{
		//Window size
		protected static const WINDOW_WIDTH:int = 580;
		protected static const WINDOW_HEIGHT:int = 460;

		//Buttons
		protected static const BUTTON_AREA_HEIGHT:int = 35;
		protected static const BUTTON_HEIGHT:int = 30;
		protected static const SUPPORT_BUTTON_WIDTH:int = 200;
		protected static const CLOSE_BUTTON_WIDTH:int = 120;
		protected static const BUTTON_CORNER_SIZE:int = 8;
		protected static const BUTTON_FONT_SIZE:int = 12;

		//Main panel
		protected static const MAIN_PANEL_INDENT:int = 5;
		protected static const MAIN_PANEL_MARGIN:int = 5;
		protected static const MAIN_PANEL_CORNER_SIZE:int = 12;

		protected static const MAIN_PANEL_WIDTH:int = WINDOW_WIDTH - MAIN_PANEL_INDENT * 2;
		protected static const MAIN_PANEL_HEIGHT:int = WINDOW_HEIGHT - MAIN_PANEL_INDENT * 2 - BUTTON_AREA_HEIGHT;

		//Fonts
		public static const APP_FONT:String = "Verdana";

		protected var stageWidth:int = WINDOW_WIDTH;
		protected var stageHeight:int = WINDOW_HEIGHT;

		protected var glassPane:Sprite = null;
		protected var frame:Sprite = null;
		protected var mainPanel:Sprite = null;

		protected var supportButton:CustomButton = null;
		protected var closeButton:CustomButton = null;

		protected var offersService:OffersService = null;
		protected var scrollPane:ScrollPane = null;
		protected var rewardCallback:Function = null;


		public function OffersWindowBase( offersService:OffersService, rewardCallback:Function )
		{
			this.offersService = offersService;
			this.rewardCallback = rewardCallback;
		}


		public function stageResized( stageWidth:int, stageHeight:int ):void
		{
			this.stageWidth = stageWidth;
			this.stageHeight = stageHeight;
			glassPane.graphics.clear();
			glassPane.graphics.beginFill( 0xFFFF00, 0 );
			glassPane.graphics.drawRect( 0, 0, stageWidth, stageHeight );
			var x:int = (stageWidth - WINDOW_WIDTH) / 2;
			var y:int = (stageHeight - WINDOW_HEIGHT) / 2;
			frame.x = x;
			frame.y = y;
		}


		protected function createWindow():void
		{
			createGlassPane();
			createFrame();
			createMainPanel();
			createScrollPane();
			createButtonsPane();
		}


		private function createGlassPane():void
		{
			glassPane = new Sprite();
			glassPane.x = 0;
			glassPane.y = 0;
			addChild( glassPane );
			glassPane.graphics.beginFill( 0xFFFF00, 0 );
			glassPane.graphics.drawRect( 0, 0, stageWidth, stageHeight );
		}


		private function createFrame():void
		{
			frame = new Sprite();
			frame.graphics.beginFill( 0xFFFFFF, 1 );
			frame.graphics.drawRoundRect( 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 20, 20 );
			addChild( frame );

		}


		private function createMainPanel():void
		{
			mainPanel = new Sprite();
			mainPanel.x = MAIN_PANEL_INDENT;
			mainPanel.y = MAIN_PANEL_INDENT;
			mainPanel.graphics.beginFill( 0xC7C7C7, 1 );
			mainPanel.graphics.drawRoundRect( 0, 0,
					MAIN_PANEL_WIDTH, MAIN_PANEL_HEIGHT, MAIN_PANEL_CORNER_SIZE, MAIN_PANEL_CORNER_SIZE );
			mainPanel.graphics.beginFill( 0xCFCFCF, 1 );
			mainPanel.graphics.drawRoundRect( 1, 1,
					MAIN_PANEL_WIDTH - 2, MAIN_PANEL_HEIGHT - 2, MAIN_PANEL_CORNER_SIZE - 2, MAIN_PANEL_CORNER_SIZE - 2 );
			mainPanel.graphics.beginFill( 0xD7D7D7, 1 );
			mainPanel.graphics.drawRoundRect( 2, 2,
					MAIN_PANEL_WIDTH - 4, MAIN_PANEL_HEIGHT - 4, MAIN_PANEL_CORNER_SIZE - 4, MAIN_PANEL_CORNER_SIZE - 4 );
			mainPanel.graphics.beginFill( 0xDDDDDD, 1 );
			mainPanel.graphics.drawRoundRect( 3, 3,
					MAIN_PANEL_WIDTH - 6, MAIN_PANEL_HEIGHT - 6, MAIN_PANEL_CORNER_SIZE - 6, MAIN_PANEL_CORNER_SIZE - 6 );
			mainPanel.graphics.beginFill( 0xE0E0E0, 1 );
			mainPanel.graphics.drawRoundRect( 4, 4,
					MAIN_PANEL_WIDTH - 8, MAIN_PANEL_HEIGHT - 8, MAIN_PANEL_CORNER_SIZE - 8, MAIN_PANEL_CORNER_SIZE - 8 );
			frame.addChild( mainPanel );
		}


		private function createScrollPane():void
		{
			scrollPane = new ScrollPane();
			mainPanel.addChild( scrollPane );
			scrollPane.create( MAIN_PANEL_MARGIN, MAIN_PANEL_MARGIN,
					MAIN_PANEL_WIDTH - MAIN_PANEL_MARGIN * 2, MAIN_PANEL_HEIGHT - MAIN_PANEL_MARGIN * 2 );
		}


		private function createButtonsPane():void
		{

			supportButton = new CustomButton( "Техническая поддержка",
					MAIN_PANEL_INDENT, WINDOW_HEIGHT - BUTTON_HEIGHT - MAIN_PANEL_INDENT,
					SUPPORT_BUTTON_WIDTH, BUTTON_HEIGHT, 10, ButtonState.GRAY, BUTTON_FONT_SIZE );
			frame.addChild( supportButton );
			supportButton.addEventListener( MouseEvent.CLICK, helpButton_click );

			closeButton = new CustomButton( "Закрыть",
					WINDOW_WIDTH - CLOSE_BUTTON_WIDTH - MAIN_PANEL_INDENT, WINDOW_HEIGHT - BUTTON_HEIGHT - MAIN_PANEL_INDENT,
					CLOSE_BUTTON_WIDTH, BUTTON_HEIGHT, 10, ButtonState.GRAY, BUTTON_FONT_SIZE );
			frame.addChild( closeButton );
			closeButton.addEventListener( MouseEvent.CLICK, closeButton_click );
		}


		private function helpButton_click( e:MouseEvent ):void
		{
			navigateToURL( new URLRequest( "http://heymoose.com/contacts" ), "_blank" );
		}


		private function closeButton_click( e:MouseEvent ):void
		{
			this.visible = true;
			dispatchEvent( new Event( Event.CLOSE ) );
		}

	}
}