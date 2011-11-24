/**
 * Created by IntelliJ IDEA.
 * User: Sokolov Stanislav
 * Date: 11/24/11
 * Time: 8:52 AM
 */
package com.heymoose.statics
{

	public class HeyMooseBirthDate
	{
		public static function convert( value:String, platform:String ):String
		{
			if(!value) return "NULL"
			switch ( platform )
			{
				case HeyMoosePlatform.vkontakte:
					if ( value.split( '.' ).length == 3 )
					{
						return value.split( '.' )[2];
					}
					else
					{
						return "NULL"
					}
					break;
			}
			return "NULL"
		}
	}
}
