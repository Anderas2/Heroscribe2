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

package org.lightless.heroscribe;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.lightless.heroscribe.helper.OS;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class Preferences extends DefaultHandler {
	public File ghostscriptExec;
	
	public Preferences() {
		super();

		ghostscriptExec = new File("");

		if ( OS.isWindows() ) {
			File base = new File("c:\\gs\\");
			
			if ( base.isDirectory() ) {
				File[] files = base.listFiles();
				
				for ( int i = 0 ; i < files.length ; i++ ) {
					if ( files[i].isDirectory() &&
						new File(files[i], "bin\\gswin32c.exe").isFile() ) {
							ghostscriptExec = new File(files[i], "bin\\gswin32c.exe");
							
							break;
						}
				}
			}		
		} else {
			if ( new File("/usr/bin/gs").isFile() )
				ghostscriptExec = new File("/usr/bin/gs");
		}
	}
	
	public Preferences(File file) {
		this();
		
		if ( file.isFile() ) {
			try {
				SAXParserFactory factory = SAXParserFactory.newInstance();

				SAXParser saxParser = factory.newSAXParser();
				saxParser.parse(file, this);
			}
			catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	
	/* Read XML */
	
	public void startElement(String uri, String localName, String qName, Attributes attrs) throws SAXException {
		if (qName == "ghostscript") {
			File file = new File( attrs.getValue("path") );
			
			if ( file.isFile() ) {
				ghostscriptExec = file;
			}
		}
	}
	
	/* Write XML */

	public void write() throws Exception {
		PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(Constants.preferencesFile)));

		out.println("<?xml version=\"1.0\"?>");
		out.println("<preferences>");
		
		out.println("<ghostscript path=\"" +
			ghostscriptExec.getAbsoluteFile().toString().replaceAll("\"", "&quot;") +
			"\"/>");
			
		out.println("</preferences>");
		
		out.close();
	}
}