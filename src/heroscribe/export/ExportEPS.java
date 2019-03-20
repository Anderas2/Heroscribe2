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

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.Iterator;
import java.util.TreeSet;
import java.util.zip.GZIPInputStream;

import org.lightless.heroscribe.list.List;
import org.lightless.heroscribe.quest.QBoard;
import org.lightless.heroscribe.quest.QObject;
import org.lightless.heroscribe.quest.Quest;

public class ExportEPS {
	private static int linesPerBlock = 500;

	private static int[] appendPS(
		String inPath,
		PrintWriter out,
		boolean printComments,
		boolean divideInBlocks)
		throws Exception {

		BufferedReader in =
			new BufferedReader(
				new InputStreamReader(
					new GZIPInputStream(new FileInputStream(inPath))));

		int[] boundingBox = null;

		String data = in.readLine();
		int lines = 0;

		while (data != null) {
			if (printComments ||
				(data.trim().length() > 0 && data.trim().charAt(0) != '%') ) {
				if (divideInBlocks && lines % linesPerBlock == 0) {
					if (lines != 0)
						out.write(" } exec ");
					out.write(" { ");
				}

				lines++;
				out.println(data);
			}

			if (data.trim().startsWith("%%BoundingBox:")
				&& boundingBox == null) {
				String[] bit = data.split(" ");
				boundingBox = new int[4];

				for (int i = 0; i < 4; i++) {
					boundingBox[i] = Integer.parseInt(bit[bit.length - 4 + i]);
				}
			}

			data = in.readLine();
		}

		if (divideInBlocks && lines > 0)
			out.write(" } exec ");

		in.close();

		return boundingBox;

	}

	public static void write(File file, Quest quest, List objects)
		throws Exception {
		PrintWriter out =
			new PrintWriter(new BufferedWriter(new FileWriter(file)));
		TreeSet set = new TreeSet();
		Iterator iterator;

		float bBoxWidth, bBoxHeight;

		bBoxWidth = (quest.getWidth() * (quest.getBoard(0, 0).getWidth() + 2) +
			(quest.getWidth() - 1) * objects.getBoard().adjacentBoardsOffset) * 19.2f;

		bBoxHeight = (quest.getHeight() * (quest.getBoard(0, 0).getHeight() + 2) +
			(quest.getHeight() - 1) * objects.getBoard().adjacentBoardsOffset) * 19.2f;

		out.println("%!PS-Adobe-3.0 EPSF-3.0");
		out.println("%%LanguageLevel: 2");
		out.println("%%BoundingBox: 0 0 "
			+ Math.round(Math.ceil(bBoxWidth))
			+ " "
			+ Math.round(Math.ceil(bBoxHeight)));
		out.println("%%HiResBoundingBox: 0 0 " + bBoxWidth + " " + bBoxHeight);
		
		out.println("/adjacentBoardsOffset " +
			objects.getBoard().adjacentBoardsOffset + " def");
		
		appendPS(objects.getVectorPath(quest.getRegion()), out, false, false);

		out.println(
			quest.getWidth() + " " + quest.getHeight() + " BoundingBox");
		out.println(
			"2 dict dup dup /showpage {} put /setpagedevice {} put begin");

		for (int i = 0; i < quest.getWidth(); i++)
			for (int j = 0; j < quest.getHeight(); j++) {
				iterator = quest.getBoard(i, j).iterator();

				while (iterator.hasNext())
					set.add(((QObject) iterator.next()).id);
			}

		iterator = set.iterator();
		while (iterator.hasNext()) {
			String id = (String) iterator.next();
			int[] boundingBox;

			out.println("/Icon" + id + " << /FormType 1 /PaintProc { pop");

			/* the postscript is divided in "{ } exec" blocks to broaden
			 * compatibility
			 */
			boundingBox =
				appendPS(
					objects.getVectorPath(id, quest.getRegion()),
					out,
					false,
					true);

			out.println(
				" } bind /Matrix [1 0 0 1 0 0] /BBox ["
					+ boundingBox[0]
					+ " "
					+ boundingBox[1]
					+ " "
					+ boundingBox[2]
					+ " "
					+ boundingBox[3]
					+ "] >> def");
		}

		for (int column = 0; column < quest.getWidth(); column++)
			for (int row = 0; row < quest.getHeight(); row++) {
				QBoard board = quest.getBoard(column, row);

				out.println(column + " " +
					(quest.getHeight() - row - 1) + " StartBoard");

				for (int i = 1; i <= board.getWidth(); i++)
					for (int j = 1; j <= board.getHeight(); j++)
						if (objects.board.corridors[i][j])
							out.println(
								i
									+ " "
									+ (board.getHeight() - j + 1)
									+ " 1 1 Corridor");

				for (int i = 1; i <= board.getWidth(); i++)
					for (int j = 1; j <= board.getHeight(); j++)
						if (board.isDark(i, j))
							out.println(
								i
									+ " "
									+ (board.getHeight() - j + 1)
									+ " 1 1 Dark");

				out.println("Grid");

				out.println("EndBoard");
			}
			

		/* Bridges */		
		for (int column = 0; column < quest.getWidth(); column++)
			for (int row = 0; row < quest.getHeight(); row++) {
				QBoard board = quest.getBoard(column, row);

				out.println(column + " " +
					(quest.getHeight() - row - 1) + " StartBoard");
				
				if ( column < quest.getWidth() - 1 )
					for (int top = 1 ; top <= board.getHeight() ; top++ )
						if ( quest.getHorizontalBridge(column, row, top) )
							out.println((board.getHeight() - top + 1) + " HorizontalBridge");
				
				if ( row < quest.getHeight() - 1 )
					for (int left = 1 ; left <= board.getWidth() ; left++ )	
						if ( quest.getVerticalBridge(column, row, left) )
							out.println(left + " VerticalBridge");

				out.println("EndBoard");
			}

			
		for (int column = 0; column < quest.getWidth(); column++)
			for (int row = 0; row < quest.getHeight(); row++) {
				QBoard board = quest.getBoard(column, row);

				out.println(column + " " +
					(quest.getHeight() - row - 1) + " StartBoard");

				iterator = board.iterator();
				while (iterator.hasNext()) {
					QObject obj = (QObject) iterator.next();
					int width, height;
					float x, y, xoffset, yoffset;

					if (obj.rotation % 2 == 0) {
						width = objects.getObject(obj.id).width;
						height = objects.getObject(obj.id).height;
					} else {
						width = objects.getObject(obj.id).height;
						height = objects.getObject(obj.id).width;
					}

					x = obj.left + width / 2.0f;
					y = obj.top + height / 2.0f;

					if (objects.getObject(obj.id).trap) {
						out.println(
							obj.left
								+ " "
								+ (board.getHeight() - obj.top - height + 2)
								+ " "
								+ width
								+ " "
								+ height
								+ " Trap");
					} else if (objects.getObject(obj.id).door) {
						if (obj.rotation % 2 == 0) {
							if (obj.top == 0)
								y -= objects.getBoard().borderDoorsOffset;
							else if (obj.top == board.getHeight())
								y += objects.getBoard().borderDoorsOffset;
						} else {
							if (obj.left == 0)
								x -= objects.getBoard().borderDoorsOffset;
							else if (obj.left == board.getWidth())
								x += objects.getBoard().borderDoorsOffset;
						}
					}

					xoffset =
						objects.getObject(obj.id).getIcon(
							quest.getRegion()).xoffset;
					yoffset =
						objects.getObject(obj.id).getIcon(
							quest.getRegion()).yoffset;

					switch (obj.rotation) {
						case 0 :
							x += xoffset;
							y += yoffset;
							break;

						case 1 :
							x += yoffset;
							y -= xoffset;
							break;

						case 2 :
							x -= xoffset;
							y -= yoffset;
							break;

						case 3 :
							x -= yoffset;
							y += xoffset;
							break;
					}

					y = objects.getBoard().height - y + 2;

					out.println("gsave");
					out.println(x + " Unit " + y + " Unit translate");
					out.println((obj.rotation * 90) + " rotate");
					out.println("Icon" + obj.id + " execform");
					out.println("grestore");
					out.println();

				}

				out.println("EndBoard");
			}
		out.println("end");
		out.println("%%EOF");

		out.close();
	}
}
