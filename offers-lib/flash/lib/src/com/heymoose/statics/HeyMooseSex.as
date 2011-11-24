/**
 * Created by IntelliJ IDEA.
 * User: Sokolov Stanislav
 * Date: 11/24/11
 * Time: 12:23 AM
 */
package com.heymoose.statics
{

	public class HeyMooseSex
	{
		public static var male:String = "MALE";
		public static var female:String = "FEMALE";

		public static function convert(value:String, platform:String):String
		{
			switch(platform)
			{
				case HeyMoosePlatform.vkontakte:
						if(value == '1') return female;
						if(value == '2') return male;
				break;
			}
			return "NULL"
		}
	}
}
