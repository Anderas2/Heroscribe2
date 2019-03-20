/*
  HeroScribe
  Copyright (C) 2002-2004 Flavio Chierichetti and Valerio Chierichetti
   
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License version 2 (not
  later versions) as published by the Free Software Foundation.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

package org.lightless.heroscribe.helper;

import java.io.File;
import java.lang.reflect.Method;

public class OS {
	public static void openURL(File file, String ref) {
		try {
			if ( ref != null)
				openURL(file.toURI().toURL().toString() + "#" + ref);
			else
				openURL(file.toURI().toURL().toString());
			
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void openURL(String url) {
		try {
			if ( isWindows() ) {
				Runtime.getRuntime().exec("rundll32 url.dll,FileProtocolHandler \"" + url + "\"");
			} else if ( isMacOsX() ) {
				Class utils = Class.forName("com.apple.mrj.MRJFileUtils");
				Method openURL = utils.getDeclaredMethod("openURL",
					new Class[] { String.class } );
					
				openURL.invoke(null, new String[] { url } );
			} else {
				/* sadly, can't think of anything better for gnu/linux, *bsd,
				 * etc...
				 * If the (physical :) reader want to suggest something better,
				 * I'm all ears :)
				 */
				 
				Runtime.getRuntime().exec("mozilla " + url);
			}
		}	
		catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static boolean isWindows() {
		return System.getProperty("os.name").startsWith("Win");
	}

	public static boolean isMacOsX() {
		return System.getProperty("mrj.version") != null;
	}
	
	public static String getAbsolutePath(String relative) {
		return new File(System.getProperty("user.dir"), relative).getAbsolutePath();
	}
}