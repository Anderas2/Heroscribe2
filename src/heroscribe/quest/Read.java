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

import java.io.File;

import org.lightless.heroscribe.helper.OS;
import org.lightless.heroscribe.list.*;

import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.parsers.*;

public class Read extends DefaultHandler {
	private Quest quest;
	private List objects;

	private StringBuffer content;

	private File file;
	private QBoard board;
	private int width, height, boardCount;

	public Read(File file, List objects) throws Exception {
		super();

		this.file = file;
		this.objects = objects;

		SAXParserFactory factory = SAXParserFactory.newInstance();
		factory.setValidating(true);

		SAXParser saxParser = factory.newSAXParser();

		saxParser.parse(file, this);
	}

	public Quest getQuest() {
		return quest;
	}

	/* --- */

	public InputSource resolveEntity(String publicId, String systemId) {
		if (publicId.equals("-//org.lightless//HeroScribe Quest 1.4//EN"))
			return new InputSource(OS.getAbsolutePath("DtdXsd/quest-1.4.dtd"));
		if (publicId.equals("-//org.lightless//HeroScribe Quest 1.3//EN"))
			return new InputSource(OS.getAbsolutePath("DtdXsd/quest-1.3.dtd"));
		if (publicId.equals("-//org.lightless//HeroScribe Quest 1.2//EN"))
			return new InputSource(OS.getAbsolutePath("DtdXsd/quest-1.2.dtd"));
		else
			return null;
	}

	public void error(SAXParseException e) throws SAXException {
		throw new SAXException(e);
	}

	public void startDocument() {
		content = new StringBuffer();
	}

	public void startElement(
		String uri,
		String localName,
		String qName,
		Attributes attrs)
		throws SAXException {
		content = new StringBuffer();

		if (qName.equals("quest")) {
			if (attrs.getValue("width") != null) {
				width = Integer.parseInt(attrs.getValue("width"));
			} else {
				width = 1;
			}

			if (attrs.getValue("height") != null) {
				height = Integer.parseInt(attrs.getValue("height"));
			} else {
				height = 1;
			}

			if ( width < 1 || height < 1 )
				throw new SAXException("Both width and height should be at least 1.");

			boardCount = 0;

			quest = new Quest(width, height, objects.getBoard(), file);

			quest.setName(attrs.getValue("name"));
			quest.setRegion(attrs.getValue("region"));

			if (!org.lightless.heroscribe.Constants
				.version.equals(attrs.getValue("version")))
				throw new SAXException("Heroscribe's and quest's version numbers don't match.");

		} else if (qName.equals("board")) {

			if (boardCount >= width * height)
				throw new SAXException("Too many boards in the quest.");

			board =
				new QBoard(
					objects.getBoard().width,
					objects.getBoard().height,
					quest);

			quest.setBoard(board, boardCount % width, boardCount / width);

			boardCount++;

		} else if (qName.equals("bridge")) {
			int column, row;
			int position;

			column = Integer.parseInt(attrs.getValue("column")) - 1;
			row = Integer.parseInt(attrs.getValue("row")) - 1;
			position = Integer.parseInt(attrs.getValue("position"));

			if ( "horizontal".equals( attrs.getValue("orientation") ) ) {
				quest.setHorizontalBridge(true, column, row, position);
			} else if ( "vertical".equals( attrs.getValue("orientation") ) ) {
				quest.setVerticalBridge(true, column, row, position);
			} else
				throw new SAXException("Orientation not understood.");			

		} else if (qName.equals("dark")) {
			int width, height;
			int left, top;

			width = Integer.parseInt(attrs.getValue("width"));
			height = Integer.parseInt(attrs.getValue("height"));
			left = Integer.parseInt(attrs.getValue("left"));
			top = Integer.parseInt(attrs.getValue("top"));

			if (left + width - 1 > objects.getBoard().width
				|| left < 1
				|| top + height - 1 > objects.getBoard().height
				|| top < 1)
				throw new SAXException("Dark: out of border");

			for (int i = 0; i < width; i++)
				for (int j = 0; j < height; j++)
					if (!board.isDark(left + i, top + j))
						board.toggleDark(left + i, top + j);

		} else if (qName.equals("object")) {
			QObject obj = new QObject(attrs.getValue("id"), objects);

			if (objects.getObject(obj.id) == null)
				throw new SAXException("Can't find icon " + obj.id);

			if (attrs.getValue("zorder") != null)
				obj.zorder = Float.parseFloat(attrs.getValue("zorder"));
			else
				obj.zorder = objects.getObject(obj.id).zorder;

			obj.left = Float.parseFloat(attrs.getValue("left"));
			obj.top = Float.parseFloat(attrs.getValue("top"));

			if (attrs.getValue("rotation").equals("downward")) {
				obj.rotation = 0;
			} else if (attrs.getValue("rotation").equals("rightward")) {
				obj.rotation = 1;
			} else if (attrs.getValue("rotation").equals("upward")) {
				obj.rotation = 2;
			} else if (attrs.getValue("rotation").equals("leftward")) {
				obj.rotation = 3;
			} else
				throw new SAXException("Rotation not understood.");

			if (board.addObject(obj) == false)
				System.err.println(
					"Ignoring an object as there's one exactly equal.");
		}
	}

	public void characters(char[] ch, int start, int length) {
		content.append(ch, start, length);
	}

	public void endElement(String uri, String localName, String qName)
		throws SAXException {
		if (qName.equals("speech")) {
			quest.setSpeech(new String(content));
		} else if (qName.equals("note")) {
			quest.addNote(new String(content));
		} else if (qName.equals("quest")) {
			if (boardCount < width * height)
				throw new SAXException("Too few boards in the quest.");
		}
	}

	public void endDocument() {
		quest.setModified(false);
		content = null;
	}
}
