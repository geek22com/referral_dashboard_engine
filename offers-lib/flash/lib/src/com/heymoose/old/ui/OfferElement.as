package com.heymoose.old.ui
{

	import com.heymoose.old.events.OfferEvent;
	import com.heymoose.old.ext.Base64;

	import flash.display.DisplayObject;
	import flash.display.GradientType;
	import flash.display.Loader;
	import flash.display.MovieClip;
	import flash.display.Shape;
	import flash.display.SpreadMethod;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.MouseEvent;
	import flash.events.SecurityErrorEvent;
	import flash.geom.Matrix;
	import flash.net.*;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;

	public class OfferElement extends Sprite
	{
		//Element
		private static const WIDTH:int = 540;
		private static const HEIGHT:int = 77;
		private static const CORNER_SIZE:int = 10;
		private static const FRAME_THICKNESS:int = 1;
		private static const INDENT:int = 5;

		//Icon
		private static const ICON_SIZE:int = 75;

		//Button
		private static const BUTTON_WIDTH:int = 90;
		private static const BUTTON_HEIGHT:int = 28;
		private static const BUTTON_CORNER_SIZE:int = 6;
		private static const BUTTON_LEFT:int = WIDTH - FRAME_THICKNESS - INDENT - BUTTON_WIDTH;
		private static const BUTTON_FONT_SIZE:int = 12;

		private var frame:Shape = null;
		private var clip:Sprite = null;
		private var icon:DisplayObject = null;
		private var iconLoader:Loader = null;
		private var url:String = "";

		private var window:MovieClip = null;
		private var offer:Object = null;
		private var buttonText:String = null;
		private var key:String = null;


		public function OfferElement( window:MovieClip, offer:Object, buttonText:String, key:String = null )
		{
			this.window = window;
			this.offer = offer;
			this.buttonText = buttonText;
			this.key = key;
			//Frame
			frame = new Shape();
			frame.graphics.beginFill( 0xCECECE, 1 );
			frame.graphics.drawRoundRect( 0, 0, WIDTH, HEIGHT, CORNER_SIZE, CORNER_SIZE );
			//Gradient fill
			var matrix:Matrix = new Matrix();
			matrix.createGradientBox( width, height, Math.PI / 2, 0, 0 );
			frame.graphics.beginGradientFill( GradientType.LINEAR,
					[0xffffff, 0xf8f8f8], [1, 1], [0x00, 0xFF], matrix, SpreadMethod.PAD );
			frame.graphics.drawRoundRect( FRAME_THICKNESS, FRAME_THICKNESS,
					WIDTH - FRAME_THICKNESS * 2, HEIGHT - FRAME_THICKNESS * 2,
					CORNER_SIZE - FRAME_THICKNESS * 2, CORNER_SIZE - FRAME_THICKNESS * 2 );
			frame.graphics.endFill();
			addChild( frame );

			//Clip
			clip = new Sprite();
			clip.graphics.beginFill( 0xFF0000, 1 );
			clip.graphics.drawRoundRect( FRAME_THICKNESS, FRAME_THICKNESS,
					WIDTH - FRAME_THICKNESS * 2, HEIGHT - FRAME_THICKNESS * 2,
					CORNER_SIZE - FRAME_THICKNESS * 2, CORNER_SIZE - FRAME_THICKNESS * 2 );
			clip.visible = false;
			addChild( clip );
			//Icon
			/*
			 var iconUrl : String;
			 if (offer.icon != null && offer.icon != "") {
			 iconUrl = offer.icon;
			 } else {
			 iconUrl = "http://static.dai2.ru/img/default_offer.png";
			 }*/

			iconLoader = new Loader();

			iconLoader.contentLoaderInfo.addEventListener( Event.COMPLETE, offersLoader_complete );
			iconLoader.contentLoaderInfo.addEventListener( IOErrorEvent.IO_ERROR, offersLoader_onIoError );
			iconLoader.contentLoaderInfo.addEventListener( SecurityErrorEvent.SECURITY_ERROR, offersLoader_onSecurityError );
			//var context:LoaderContext = new LoaderContext(true, new ApplicationDomain());
			//iconLoader.load(new URLRequest(iconUrl), context);
			iconLoader.loadBytes( Base64.decode( offer.image ) );

			// Name
			var tf:TextFormat = new TextFormat();
			tf.color = 0x0097e0;
			tf.font = OffersWindowBase.APP_FONT;
			tf.size = 11;
			tf.bold = true;
			tf.align = TextFormatAlign.LEFT;

			var name:TextField = new TextField();
			name.text = offer.title;
			name.x = FRAME_THICKNESS + INDENT + ICON_SIZE;
			name.y = FRAME_THICKNESS * 2;
			name.width = BUTTON_LEFT - name.x - INDENT;
			name.height = 19;
			name.setTextFormat( tf );
			name.wordWrap = true;

			this.addChild( name );

			//Description
			tf = new TextFormat();
			tf.color = 0x555555;
			tf.font = OffersWindowBase.APP_FONT;
			tf.size = 10;
			tf.bold = false;
			tf.align = TextFormatAlign.LEFT;
			tf.leading = -1;

			var descr:TextField = new TextField();
			descr.text = offer.description;
			descr.x = FRAME_THICKNESS + INDENT + ICON_SIZE;
			descr.y = 16;
			descr.width = BUTTON_LEFT - descr.x - INDENT;
			descr.height = 55;
			descr.setTextFormat( tf );
			descr.wordWrap = true;

			this.addChild( descr );

			//Disclaimer
			/*
			 tf = new TextFormat();
			 tf.color = 0xcc4000;
			 tf.font = OffersWindowBase.APP_FONT;
			 tf.size = 10;
			 tf.bold = false;
			 tf.align = TextFormatAlign.LEFT;

			 var disc : TextField = new TextField();
			 disc.text = offer.disclaimer;
			 disc.x = FRAME_THICKNESS + INDENT + ICON_SIZE;
			 disc.y = 60;
			 disc.width = WIDTH - disc.x - FRAME_THICKNESS - INDENT;
			 disc.height = 17;
			 disc.setTextFormat(tf);
			 disc.wordWrap = true;
			 this.addChild(disc);
			 */

			var goButton:CustomButton = new CustomButton( buttonText,
					WIDTH - BUTTON_WIDTH - FRAME_THICKNESS - INDENT, FRAME_THICKNESS + INDENT,
					BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_CORNER_SIZE, ButtonState.GREEN, BUTTON_FONT_SIZE );
			addChild( goButton );

			var offersWindow:OffersWindow = window as OffersWindow;
			if ( offersWindow != null )
			{
				url = offersWindow.getOffersService().do_offer_for( offer.id );
			} else
			{
				var offersBanner:OfferBanner = window as OfferBanner;
				url = offersBanner.getOffersService().do_offer_for( offer.id );
			}
			goButton.addEventListener( MouseEvent.CLICK, goButton_clickHandler );
			//Placeholders for flag icons
			//frame.graphics.beginFill(0xcccccc,1);
			//frame.graphics.drawRoundRect(BUTTON_LEFT, 38, 26, 24, 3);
			//frame.graphics.drawRoundRect(BUTTON_LEFT + 32, 38, 26, 24, 3);
			//frame.graphics.drawRoundRect(BUTTON_LEFT + 64, 38, 26, 24, 3);
			//frame.graphics.endFill();

		}


		private function goButton_clickHandler( event:MouseEvent ):void
		{
			navigateToURL( new URLRequest( url ), "_blank" );
			if ( key == null )
			{
				window.dispatchEvent( new OfferEvent( OfferEvent.OFFER_CLICKED, offer ) );
			} else
			{
				window.dispatchEvent( new OfferEvent( OfferEvent.ACCEPTANCE_CLICKED, offer, key ) );
			}
		}


		private function offersLoader_complete( e:Event ):void
		{
			icon = iconLoader.content;
			addChild( icon );
			icon.x = FRAME_THICKNESS;
			icon.y = FRAME_THICKNESS;
			icon.width = ICON_SIZE;
			icon.height = ICON_SIZE;
			icon.mask = clip;
		}


		private function offersLoader_onIoError( e:IOErrorEvent ):void
		{
			trace( "Error!", e.type );
		}


		private function offersLoader_onSecurityError( e:SecurityErrorEvent ):void
		{
			trace( "Error!", e.type );
		}

	}
}