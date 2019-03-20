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

package org.lightless.heroscribe.gui;

import org.lightless.heroscribe.list.LObject;
import org.lightless.heroscribe.quest.*;

import javax.swing.*;
import javax.swing.event.MouseInputListener;

import java.util.Iterator;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;

import java.awt.event.MouseEvent;

public class Board extends JPanel implements MouseInputListener {
	private Gui gui;
	
	private int lastRow, lastColumn;
	private int lastTop, lastLeft;
	private int rotation;
	
	private boolean isPaintingDark, isDark, hasAdded;

	public Board(Gui gui) throws Exception {
		super();

		this.gui = gui;

		isPaintingDark = isDark = hasAdded = false;
		
		lastRow = lastColumn = -1;
		lastTop = lastLeft = -1;

		setBackground(Color.WHITE);

		setSize();

		/* Is it possible to just addMouseInputListener() ? */
		addMouseListener(this);
		addMouseMotionListener(this);
	}

	public void setSize() {
		setPreferredSize(gui.boardPainter.framePixelSize);
		//setMaximumSize(gui.boardPainter.framePixelSize);
		
		this.revalidate();
	}

	public void paintComponent(Graphics g) {
		super.paintComponent(g);

		if ( !hasAdded &&
			"add".equals( gui.tools.getCommand() ) && 
			gui.tools.selectorPanel.getSelectedObject() != null )
			gui.boardPainter.paint(getNewObject(true),
				lastColumn, lastRow, (Graphics2D) g);
		else
			gui.boardPainter.paint(null,
				lastColumn, lastRow, (Graphics2D) g);
	}
	
	private QObject getNewObject(boolean floating) {
		QObject newObject;
		

		if ( floating ) {
			newObject = new QObject(gui.tools.selectorPanel.getSelectedObject(),
				gui.getObjects(),
				0);
			
			newObject.zorder = Integer.MAX_VALUE;
		} else {
			String id = gui.tools.selectorPanel.getSelectedObject();
			newObject = new QObject(id,	gui.getObjects());
			
			newObject.zorder = gui.getObjects().getObject(id).zorder;
		}

		newObject.rotation = rotation;
		newObject.left = lastLeft;
		newObject.top = lastTop;
			
		return newObject;
	}
	
	private Image getBoardIcon() {
		return gui.getObjects().getBoard().getIcon(getRegion()).image;
	}

	private String getRegion() {
		return gui.getQuest().getRegion();
	}

	public void resetRotation() {
		rotation = 0;
		
		repaint();
	}

	private void updatePosition(MouseEvent e) {
		int row, column;
		int top, left;

		float width, height;
		float x, y;
		
		width = gui.boardPainter.boardPixelSize.width +
			gui.getObjects().getBoard().adjacentBoardsOffset * gui.boardPainter.boxEdge;

		height = gui.boardPainter.boardPixelSize.height +
			gui.getObjects().getBoard().adjacentBoardsOffset * gui.boardPainter.boxEdge;
		
		
		x = e.getX() +
			(gui.getObjects().getBoard().adjacentBoardsOffset * gui.boardPainter.boxEdge) / 2.0f;
		if ( x < 0.0f )
			x = 0.0f;
		else if ( x > width * gui.getQuest().getWidth() )
			x = width * gui.getQuest().getWidth() - 1;
		
		
		y = e.getY() +
			(gui.getObjects().getBoard().adjacentBoardsOffset * gui.boardPainter.boxEdge) / 2.0f;
		if ( y < 0.0f )
			y = 0.0f;
		else if ( y > height * gui.getQuest().getHeight() )
			y = height * gui.getQuest().getHeight() - 1;
		
		row = (int) (y / height);
		column = (int) (x / width);
		
		top = (int) ((y % height) / gui.boardPainter.boxEdge -
			gui.getObjects().getBoard().adjacentBoardsOffset / 2.0f);
		if ( top < 0 )
			top = 0;
		else if ( top > gui.getObjects().getBoard().height + 1 )
			top = gui.getObjects().getBoard().height + 1;
		
		left = (int) ((x % width) / gui.boardPainter.boxEdge -
			gui.getObjects().getBoard().adjacentBoardsOffset / 2.0f);
		if ( left < 0 )
			left = 0;
		else if ( left > gui.getObjects().getBoard().width + 1 )
			left = gui.getObjects().getBoard().width + 1;
		
		//TODO
		//System.err.println("row: " + row + "   column: " + column + "   top: " + top + "   left: " + left);
		
		if ( top != lastTop || left != lastLeft ||
			row != lastRow || column != lastColumn ) {
			hasAdded = false;
			
			lastRow = row;
			lastColumn = column;
			lastTop = top;
			lastLeft = left;

			if ( isPaintingDark &&
				gui.getQuest().getBoard(lastColumn, lastRow).
					isDark(lastLeft, lastTop) != isDark )
				gui.getQuest().getBoard(lastColumn, lastRow).
					toggleDark(lastLeft, lastTop); 

			repaint();
			
			displayStatus();
		} else {
			lastRow = row;
			lastColumn = column;
			lastTop = top;
			lastLeft = left;
		}
	}

	private void displayStatus() {
		StringBuffer sb = new StringBuffer();
		boolean first = true;
			
		int width, height;
		
		if ( gui.getQuest().getBoard(lastColumn, lastRow).
			isDark(lastLeft, lastTop) ) {
			sb.insert(0, "Dark");
			
			first = false;
		}

		Iterator iterator = gui.getQuest().getBoard(lastColumn, lastRow).iterator();
		while (iterator.hasNext()) {
			QObject qobj = (QObject) iterator.next();
			LObject lobj = gui.getObjects().getObject(qobj.id);

			if ( qobj.rotation % 2 == 0 ) {
				width = lobj.width;
				height = lobj.height;
			} else {
				width = lobj.height;
				height = lobj.width;
			}
				
			if ( qobj.left <= lastLeft && lastLeft < qobj.left + width &&
				qobj.top <= lastTop && lastTop < qobj.top + height ) {
			 	
				if ( first )
					first = false;
				else
					sb.insert(0, ", ");		

				sb.insert(0, lobj.name);
			 }
		}

		gui.status.setText(new String(sb));
	}

	public void mouseDragged(MouseEvent e) {
		updatePosition(e);
	}

	public void mouseMoved(MouseEvent e) {
		updatePosition(e);
	}

	public void mouseExited(MouseEvent e) {
		lastRow = lastColumn = -1;
		lastTop = lastLeft = -1;

		repaint();
	}

	public void mousePressed(MouseEvent e) {
		updatePosition(e);
		
		if ( "add".equals( gui.tools.getCommand() ) ) {
			if ( SwingUtilities.isRightMouseButton(e) ||
				 e.isControlDown() ) {
				/* right click or (ctrl + click) (for mac's single button mice) */
				rotation = (rotation + 1) % 4;
			} else { 
				/* left click */
				QObject obj = getNewObject(false);
				
				if ( isWellPositioned(obj) )
					if ( gui.getQuest().getBoard(lastColumn, lastRow).addObject( obj ) )
						hasAdded = true;
			}
		} else if ( "select".equals( gui.tools.getCommand() ) ) {
			gui.tools.displayerPanel.createList(lastColumn, lastRow, lastLeft, lastTop); 
		} else if ( "darken".equals( gui.tools.getCommand() ) ) {
			QBoard board = gui.getQuest().getBoard(lastColumn, lastRow);
			
			if ( 1 <= lastLeft && lastLeft <= board.getWidth() &&
				 1 <= lastTop && lastTop <= board.getHeight() ) {
				/* Darken/Clear */
			
				if ( SwingUtilities.isRightMouseButton(e) ||
					 e.isControlDown() ) {
					/* right click or (ctrl + click) (for mac's single button mice) */
					isDark = false;
				} else { 
					/* left click */
					isDark = true;
				}

				if ( gui.getQuest().getBoard(lastColumn, lastRow).
					isDark(lastLeft, lastTop) != isDark )
					gui.getQuest().getBoard(lastColumn, lastRow).
						toggleDark(lastLeft, lastTop);

				isPaintingDark = true;
			} else if ( (1 <= lastLeft && lastLeft <= board.getWidth()) ||
				(1 <= lastTop && lastTop <= board.getHeight()) ) {
				/* Bridge */
				
				boolean value;
				int column = lastColumn;
				int row = lastRow;
				
				if ( lastLeft == 0 )
					column--;
				if ( lastTop == 0 )
					row--;

				if ( SwingUtilities.isRightMouseButton(e) ||
					 e.isControlDown() ) {
					/* right click or (ctrl + click) (for mac's single button mice) */
					
					value = false;
				} else { 
					/* left click */
					value = true;
				}

				if ( lastLeft < 1 || lastLeft > board.getWidth() ) {
					gui.getQuest().setHorizontalBridge(value, column, row, lastTop);
				} else {
					gui.getQuest().setVerticalBridge(value, column, row, lastLeft);
				}
			}
		}

		repaint();

		gui.updateTitle();
		displayStatus();
	}
	
	public void mouseReleased(MouseEvent e) {
		isPaintingDark = false;
	}
	
	public void mouseClicked(MouseEvent e) {}
	public void mouseEntered(MouseEvent e) {}
	
	public boolean isWellPositioned(QObject piece) {
		LObject obj = gui.getObjects().getObject(piece.id);
		
		int width, height;
		
		if ( piece.rotation % 2 == 0 ) {
			width = obj.width;
			height = obj.height;
		} else {
			width = obj.height;
			height = obj.width;
		}
			
		if ( obj.door ) {
			if ( piece.left < 0 || piece.top < 0 ||
				piece.left + width - 1 > gui.boardPainter.boardSize.width + 1 ||
				piece.top + height - 1 > gui.boardPainter.boardSize.height + 1 ||
				(piece.rotation % 2 == 0 &&
					(piece.left == 0 || piece.left == gui.boardPainter.boardSize.width + 1)) ||
				(piece.rotation % 2 == 1 &&
					(piece.top == 0 || piece.top == gui.boardPainter.boardSize.height + 1)) )
				return false;
		} else {
			if ( piece.left < 1 || piece.top < 1 ||
				piece.left + width - 1 > gui.boardPainter.boardSize.width ||
				piece.top + height - 1 > gui.boardPainter.boardSize.height )
				return false;
		}

		return true;
	}
}
