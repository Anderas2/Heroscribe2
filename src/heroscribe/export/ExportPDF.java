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

package org.lightless.heroscribe.export;

import java.io.File;

import org.lightless.heroscribe.list.List;
import org.lightless.heroscribe.quest.Quest;

public class ExportPDF {
	public static void write(File ghostscript, File file, Quest quest, List objects) throws Exception {
		File eps = File.createTempFile("hsb", ".eps");
		File pdf = File.createTempFile("hsb", ".pdf");
		
		int exitValue;
		
		ExportEPS.write(eps, quest, objects);
		
		exitValue = Runtime.getRuntime().exec(new String[] {
			ghostscript.getAbsoluteFile().toString(),
			"-dBATCH",
			"-dNOPAUSE",
			"-sDEVICE=pdfwrite",
			"-sOutputFile=" + pdf.getAbsolutePath().toString(),
			eps.getAbsoluteFile().toString()
		}).waitFor();

		eps.delete();

		if ( exitValue == 0 ) {
			file.delete();
			
			pdf.renameTo(file);
		} else {
			pdf.delete();
			
			throw new Exception("Process returned " + exitValue + ".");
		}
	}
	
}