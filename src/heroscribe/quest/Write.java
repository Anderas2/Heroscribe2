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

package org.lightless.heroscribe.quest;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Iterator;

import org.lightless.heroscribe.quest.Quest;

public class Write {
	private static String xmlEscape(String in) {
		if (in != null)
			return in
				.replaceAll("&", "&amp;")
				.replaceAll("<", "&lt;")
				.replaceAll(">", "&gt;")
				.replaceAll("\"", "&quot;")
				.replaceAll("'", "&apos;");
		else
			return "";
	}

	public static void write(Quest quest) throws Exception {

		quest.getFile().delete();

		PrintWriter out =
			new PrintWriter(
				new BufferedWriter(new FileWriter(quest.getFile())));

		out.println("<?xml version=\"1.0\"?>");
		out.println("<!DOCTYPE quest PUBLIC");
		out.println("\"-//org.lightless//HeroScribe Quest 1.4//EN\"");
		out.println("\"http://lightless.org/files/xml/quest-1.4.dtd\">");

		out.println();

		out.println(
			"<quest name=\""
				+ xmlEscape(quest.getName())
				+ "\" region=\""
				+ xmlEscape(quest.getRegion())
				+ "\" version=\""
				+ xmlEscape(org.lightless.heroscribe.Constants.version)
				+ "\" width=\""
				+ quest.getWidth()
				+ "\" height=\""
				+ quest.getHeight()
				+ "\">");

		for (int row = 0; row < quest.getHeight(); row++)
			for (int column = 0; column < quest.getWidth(); column++) {
				QBoard board = quest.getBoard(column, row);

				out.println("<board>");

				for (int left = 1; left <= board.getWidth(); left++)
					for (int top = 1; top <= board.getHeight(); top++)
						if (board.isDark(left, top))
							out.println(
								"<dark left=\"" + left + "\" top=\"" + top +
								"\" width=\"1\" height=\"1\" />");

				Iterator iterator = board.iterator();
				while (iterator.hasNext()) {
					QObject obj = (QObject) iterator.next();

					out.print("<object id=\"" + obj.id + "\" ");
					out.print(
						"left=\"" + obj.left + "\" top=\"" + obj.top + "\" ");
					out.print("rotation=\"");

					switch (obj.rotation) {
						case 0 :
							out.print("downward");
							break;
						case 1 :
							out.print("rightward");
							break;
						case 2 :
							out.print("upward");
							break;
						case 3 :
							out.print("leftward");
							break;
					}

					out.println("\" zorder=\"" + obj.zorder + "\" />");
				}

				out.println("</board>");
			}

		for (int row = 0; row < quest.getHeight(); row++)
			for (int column = 0; column < quest.getWidth(); column++) {
				QBoard board = quest.getBoard(column, row);

				if ( column < quest.getWidth() - 1 )
					for (int top = 1 ; top <= board.getHeight() ; top++ )
						if ( quest.getHorizontalBridge(column, row, top) )
							out.println("<bridge column=\"" + (column + 1) + 
								"\" row=\"" + (row + 1) +
								"\" position=\"" +
								top + "\" orientation=\"horizontal\"/>");
				
				if ( row < quest.getHeight() - 1 )
					for (int left = 1 ; left <= board.getWidth() ; left++ )	
						if ( quest.getVerticalBridge(column, row, left) )
							out.println("<bridge column=\"" + (column + 1) + 
								"\" row=\"" + (row + 1) +
								"\" position=\"" +
								left + "\" orientation=\"vertical\"/>");
			}

		out.println("<speech>" + xmlEscape(quest.getSpeech()) + "</speech>");

		Iterator iterator = quest.notesIterator();
		while (iterator.hasNext())
			out.println(
				"<note>" + xmlEscape((String) iterator.next()) + "</note>");

		out.println("</quest>");

		out.close();
	}
}