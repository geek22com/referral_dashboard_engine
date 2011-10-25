package 
{
  import flash.display.DisplayObject;
  import flash.display.Sprite;
  import flash.display.Stage;
  import flash.events.Event;
  import flash.events.MouseEvent;
  import flash.system.Security;
  import flash.text.TextField;
  
  import ru.dai2.events.OfferEvent;
  import ru.dai2.events.RPCErrorEvent;
  import ru.dai2.rpc.OffersService;
  
  import vk.*;
  
  public class VkGuiExample extends Sprite 
  {
    private var wrapper:* = null;
    private var menu_item1:* = null;
    private var menu_item2:* = null;
    private var menu_item3:* = null;
    private var menu_item4:* = null;
    private var menu_item5:* = null;
    private var last_y_1:uint = 290;
    private var last_y_2:uint = 330;
    private var last_y_4:uint = 300;
    private var last_y_5:uint = 330;
    private var box1:* = null;
    private var box2:* = null;
    

    public function VkGuiExample():void 
    {
      if (stage) init();
      else addEventListener(Event.ADDED_TO_STAGE, init);
    }
    
    private function init(e:Event = null):void 
    {
      removeEventListener(Event.ADDED_TO_STAGE, init);

      Security.allowDomain( "*" );
      VK.init( this, "http://api.vkontakte.ru/swf/vk_gui-0.5.swf" );
      //VK.init( this, "../../../bin/vk_gui-0.5.swf" );
    }

    public function onVKLoaded():void
    {
      var i:uint;
      
      wrapper = Object(parent.parent);
      if ( wrapper.external == null )
        wrapper = stage; // Local
      
      // A background for entire application
      var bg:Sprite = new Sprite();
      VK.Utils.fillRect( bg, 0, 0, 627, 4050, VK.Utils.BK_COL );
      addChild( bg );
      
      // Main menu with three items (and three associated pages)
      // Associated pages are accessible as:  main_menu.page( idx )
      var main_menu:* = VK.createMainMenu( wrapper );
      menu_item1 = main_menu.addItem( "Menu Item 1", "loc1" );
      menu_item2 = main_menu.addItem( "Menu Item 2", "loc2" );
      menu_item3 = main_menu.addItem( "Primitives drawing", "loc3" );
      menu_item4 = main_menu.addItem( "Paginations", "loc4" );
      menu_item5 = main_menu.addItem( "InputFields", "loc5" );
      addChild( main_menu );
      
      main_menu.addEventListener( Event.CHANGE, onMenuNavigate );

      main_menu.selectedItem = menu_item5;
      menu_item2.label = "This Menu Label is Changed";
      
      
      // -----------------------------------------------------------------------------------
      // --- The first page ---
      
      // Two round buttontons
      var button1:* = VK.createRoundButton( "Blue Round Button", 10, 20 );
      menu_item1.panel.addChild( button1 );
      button1.addEventListener( MouseEvent.CLICK, onButClicked );

      var button2:* = VK.createRoundButton( "Gray Round Button", 10, 60, VK.GRAY_BUTTON );
      menu_item1.panel.addChild( button2 );
      button2.addEventListener( MouseEvent.CLICK, onButClicked );
      
      // Two rectangle buttontons
      var button3:* = VK.createSquareButton( "Blue Square Button", 10, 100 );
      menu_item1.panel.addChild( button3 );
      button3.height = 33;
      button3.addEventListener( MouseEvent.CLICK, onButClicked );

      var button4:* = VK.createSquareButton( "Gray Square Button", 10, 140, VK.GRAY_BUTTON );
      menu_item1.panel.addChild( button4 );
      button4.width = 200;
      button4.addEventListener( MouseEvent.CLICK, onButClicked );

      var button5:* = VK.createLinkButton( "Link Button", 10, 180 );
      menu_item1.panel.addChild( button5 );
      button5.addEventListener( MouseEvent.CLICK, onButClicked );
      
      var button6:* = VK.createRoundButton( "Show Box with text", 300, 20 );
      menu_item1.panel.addChild( button6 );
      button6.addEventListener( MouseEvent.CLICK, onShowBox1 );
      
      var button7:* = VK.createRoundButton( "Show Box with sprite", 300, 60 );
      menu_item1.panel.addChild( button7 );
      button7.addEventListener( MouseEvent.CLICK, onShowBox2 );
      
      var button8:* = VK.createLightButton( "Blue HighLight Button", 10, 210, 150, VK.Utils.BK_COL, VK.Utils.BLUE_BK_COL, VK.Utils.BUT1_TXT_COL, VK.Utils.BUT1_TXT_COL, VK.LightButton.RIGHT, 10 );
      menu_item1.panel.addChild( button8 );
      button8.addEventListener( MouseEvent.CLICK, onButClicked );
      
      var button9:* = VK.createLightButton( "Red HighLight Button", 10, 240, 0, 0xf4ebbd, 0xf6f0d6, 0x908851, 0x908851, VK.LightButton.CENTER, 10 );
      menu_item1.panel.addChild( button9 );
      button9.addEventListener( MouseEvent.CLICK, onButClicked );
      
      // CheckBox
      var checkBox:* = VK.createCheckBox( "Check Box", 300, 100 );
      menu_item1.panel.addChild( checkBox );
      checkBox.addEventListener( Event.CHANGE, onCheckBox );
      
      // RadioButtons
      var group:* = VK.createRadioButtonsGroup( 300, 140 );
      menu_item1.panel.addChild( group );
      group.addEventListener( Event.CHANGE, onRadioButton );
      
      var radioButton1:* = group.addRadioButton( "Radio Button 1", 0, 0 );
      var radioButton2:* = group.addRadioButton( "Radio Button 2", 0, 20 );
      var radioButton3:* = group.addRadioButton( "Radio Button 3", 0, 40 );
      radioButton3.label = "Some another label";
      
      //group.selectedIndex = 2;
      group.selectedItem = radioButton3;
      

      // -----------------------------------------------------------------------------------
      // --- The second page ---
      
      // ComboBox samples
      var combo1:* = VK.createComboBox( wrapper, 10, 10, 200 );
      var itemsArr:Array = new Array( 1000 );
      for ( i = 0; i < itemsArr.length; ++i )
        itemsArr[i] = "Item " + i;
      combo1.addItemsArray( itemsArr );
      menu_item2.panel.addChild( combo1 );
      combo1.addEventListener( Event.CHANGE, onComboChanged );
      combo1.selectedIndex = 456;

      var combo2:* = VK.createComboBox( wrapper, 350, 260, 200 );
      for ( i = 0; i < 20; ++i )
        combo2.addItem( "This item will be deleted" );
      combo2.clear();
      for ( i = 0; i < 12; ++i )
        combo2.addItem( "Item " + i );
      menu_item2.panel.addChild( combo2 );
      combo2.addEventListener( Event.CHANGE, onComboChanged );
      
      // ListBox samples
      var list1:* = VK.createListBox( 350, 10, 200 );
      for ( i = 0; i < 500; ++i )
        list1.addItem( "Item " + i );
      list1.selectedIndex = 123;
      menu_item2.panel.addChild( list1 );
      list1.addEventListener( Event.CHANGE, onComboChanged );

      var list2:* = VK.createListBox( 350, 300, 200 );
      for ( i = 0; i < 5; ++i )
        list2.addItem( "Item " + i );
      list2.selectedIndex = 3;
      menu_item2.panel.addChild( list2 );
      list2.addEventListener( Event.CHANGE, onComboChanged );

      // Useful TextField creation
      var long_text:String = "";
      for ( i = 0; i < 120; ++i )
        long_text += i + " Some long text. ";
      menu_item2.panel.addChild( VK.addText( long_text, 10, 65, 0x2B587A, VK.Utils.TXT_MULTILINE, 300, 260, 11 ) );
      
      // Another text field
      var textField:TextField = VK.addText( "Some text", 10, 40, 0x2B587A, VK.Utils.TXT_BOLD | VK.Utils.TXT_UNDERLINE )
      menu_item2.panel.addChild( textField );
      VK.Utils.setText( textField, "This text is changed using vk.gui.Utils.setText" );

      
      // -----------------------------------------------------------------------------------
      // --- The 3-rd page ---
      
      // Primitives drawing sample
      VK.Utils.rect      ( menu_item3.panel,  20,  20, 150, 150, 0xf2f2f2, 0xcccccc );
      VK.Utils.fillRect  ( menu_item3.panel,  50, 150, 100, 100, 0x2B587A );
      VK.Utils.hollowRect( menu_item3.panel, 100, 100, 220, 100, 0xd8dfea );
      VK.Utils.dashRect  ( menu_item3.panel, 350,  50, 250, 110, 0x777777 );
      
      
      // -----------------------------------------------------------------------------------
      // --- The 4-th page ---
      
      // Paginations example
      var pagination1:* = VK.createPagination( 123, 10, 10, 50 );
      pagination1.addEventListener( Event.CHANGE, onPagination );
      menu_item4.panel.addChild( pagination1 );

      var pagination2:* = VK.createPagination( 82029, 10, 200, 50, VK.Pagination.RECT_AS_SEL, 4, 10 );
      pagination2.addEventListener( Event.CHANGE, onPagination );
      menu_item4.panel.addChild( pagination2 );

      var pagination3:* = VK.createPagination( 79021, 600, 10, 50, VK.Pagination.RIGHT_ALIGNED, 5, 5 );
      pagination3.addEventListener( Event.CHANGE, onPagination );
      menu_item4.panel.addChild( pagination3 );

      var pagination4:* = VK.createPagination( 40, 600, 200, 50, VK.Pagination.RIGHT_ALIGNED | VK.Pagination.RECT_AS_SEL, 2, 10 );
      pagination4.addEventListener( Event.CHANGE, onPagination );
      menu_item4.panel.addChild( pagination4 );


      // -----------------------------------------------------------------------------------
      // --- The 5-th page ---
      
      // InputFields
      var inputField1:* = VK.createInputField( 10, 10, 250 );
      inputField1.value = "Single line InputField";
      inputField1.addEventListener( VK.InputField.EVENT_MODIFIED, onInputFieldChanged );
      menu_item5.panel.addChild( inputField1 );

      var inputField2:* = VK.createInputField( 300, 10, 200, 5 );
      inputField2.value = "Please enter a text here";
      //inputField2.addEventListener( VK.InputField.EVENT_MODIFIED, onInputFieldChanged );
      menu_item5.panel.addChild( inputField2 );

      var inputField3:* = VK.createInputField( 10, 100, 250, 15, false, false );
      inputField3.value = long_text + "\n------\n" + long_text;
      //inputField3.addEventListener( VK.InputField.EVENT_MODIFIED, onInputFieldChanged );
      menu_item5.panel.addChild( inputField3 );

      var inputField4:* = VK.createInputField( 300, 100, 200, 15 );
      var s:String = "";
      for ( i = 0; i < 50; ++i )
        s += (i == 0 ? "" : "\n") + (i + 1);
      inputField4.value = s;
      //inputField4.addEventListener( VK.InputField.EVENT_MODIFIED, onInputFieldChanged );
      menu_item5.panel.addChild( inputField4 );


      // -----------------------------------------------------------------------------------
      // --- Boxes ---
      VK.Box.STAGE_WIDTH = 627;
        
      box1 = VK.createBox( "Box with text as content", long_text + long_text, 70, 500, ["Yes", "No", "Cancel", "Retry", "Abort"] );
      addChild( box1 );
      box1.addEventListener( Event.SELECT, onBoxButtonClicked );
      
      var sprite:Sprite = new Sprite();
      VK.Utils.rect( sprite, 0, 0, 250, 550, 0xf2f2f2, 0x777777 );
      VK.Utils.rect( sprite, 50, 50, 150, 100, 0xf7f7f7, 0xcccccc );
      VK.Utils.rect( sprite, 50, 400, 150, 100, 0xf7f7f7, 0xcccccc );
      var inputField5:* = VK.createInputField( 25, 200, 200, 12 );
      inputField5.value = long_text + "\n------\n" + long_text;
      sprite.addChild( inputField5 );

      box2 = VK.createBox( "Box with sprite as content", sprite, 70, 0, ["Yes", "No", "Cancel"] );
      addChild( box2 );
      box2.addEventListener( Event.SELECT, onBoxButtonClicked );
	  
	  
	  var rewardCallback : Function = function(payment : int) : String {
		  if (payment == 0) 
			  return "Тест";
		  
		  var coins : int = payment;
		  var str : String
		  if (coins % 10 == 1) {
			  str = " Золотой";
		  } else {
			  str = " Золотых";
		  }
		  return coins.toString() + str;
	  };

	  // Offers-lib integration
	  var offersLib : OffersLib = new OffersLib();
	  var offersService : OffersService = offersLib.initOffers("1", "1", "26c10b40-47ae-416d-9788-b106c64a57d9",rewardCallback, "FACEBOOK", null);
	  
	  
	  if (offersLib != null) {
		  var w : DisplayObject = offersLib.createOffersWindow(500, 200);
		  //var w : DisplayObject = offersLib.createOfferBanner(0, 0, 10 * 1000);
		  w.addEventListener(OfferEvent.OFFER_CLICKED, 
			  function(e : OfferEvent) : void {
				  trace("clicked offer ", e.offer.id);
				  //Пользователь выбрал оффер и перешел на сайт рекламодателя
			  });
		  w.addEventListener(RPCErrorEvent.RPC_ERROR,
			  function(e: RPCErrorEvent) : void {
				  trace("error ", e.text);
			  });
		  addChild(w);
	  }
    }

    
    // ---------------------------------------------------------------------------- Event handlers
    private function onMenuNavigate( e:Event ):void
    {
      if ( e.target is VK.MainMenu )
      {
        menu_item2.panel.addChild( VK.addText( "Menu Item Navigated: " + e.target.selectedItem.label, 20, last_y_2 ) );
        last_y_2 += 18;
        resizeStage( menu_item2.panel.y + last_y_2 );
      }
    }

    private function onButClicked( e:MouseEvent ):void
    {
      menu_item1.panel.addChild( VK.addText( "Button clicked: " + e.target.label, 20, last_y_1 ) );
      last_y_1 += 18;
      resizeStage( menu_item1.panel.y + last_y_1 );
    }

    private function onBoxButtonClicked( e:Event ):void
    {
      menu_item1.panel.addChild( VK.addText( "Box button clicked: " + e.target.buttonClickedIndex, 20, last_y_1 ) );
      last_y_1 += 18;
      resizeStage( menu_item1.panel.y + last_y_1 );
    }

    private function onCheckBox( e:Event ):void
    {
      menu_item1.panel.addChild( VK.addText( "CheckBox state: " + e.target.checked, 20, last_y_1 ) );
      last_y_1 += 18;
      resizeStage( menu_item2.panel.y + last_y_1 );
    }

    private function onRadioButton( e:Event ):void
    {
      menu_item1.panel.addChild( VK.addText( "RadioButton selected: " + e.target.selectedIndex, 20, last_y_1 ) );
      last_y_1 += 18;
      resizeStage( menu_item2.panel.y + last_y_1 );
    }

    private function onComboChanged( e:Event ):void
    {
      menu_item2.panel.addChild( VK.addText( "Item selected: " + e.target.selectedIndex, 20, last_y_2 ) );
      last_y_2 += 18;
      resizeStage( menu_item2.panel.y + last_y_2 );
    }

    private function onShowBox1( e:MouseEvent ):void
    {
      box1.setVisible( true );
    }
    
    private function onShowBox2( e:MouseEvent ):void
    {
      box2.setVisible( true );
    }
    
    private function onPagination( e:Event ):void
    {
      menu_item4.panel.addChild( VK.addText( "Current page: " + e.target.curPage, 20, last_y_4 ) );
      last_y_4 += 18;
      resizeStage( menu_item2.panel.y + last_y_4 );
    }
    
    private function onInputFieldChanged( e:Event ):void
    {
      if ( e.target is VK.InputField )
      {
        menu_item5.panel.addChild( VK.addText( "InputField text: " + e.target.value, 20, last_y_5 ) );
        last_y_5 += 18;
        resizeStage( menu_item2.panel.y + last_y_5 );
      }
    }
    
    // ---------------------------------------------------------------------------- Private helper methods
    private function resizeStage( h:uint ):void
    {
      if ( h < 650 )
        h = 650;
      
      if ( !(wrapper is Stage) )
        wrapper.external.resizeWindow( 627, h );
    }

    
  }
  
}