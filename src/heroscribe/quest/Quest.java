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
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Vector;

import org.lightless.heroscribe.list.LBoard;

public class Quest {
	private File file;

	private int width, height;
	private String name, region, speech;
	private Vector notes;

	private QBoard[][] boards;
	private boolean[][][] horizontalBridges, verticalBridges;

	private boolean modified;
	
	public Quest(int width, int height, LBoard board, File file) {
		this.width = width;
		this.height = height;
		
		boards = new QBoard[width][height];
		
		for ( int i = 0 ; i < width ; i++ )
			for ( int j = 0 ; j < height ; j++ )
				boards[i][j] = new QBoard(board.width, board.height, this);
		
		horizontalBridges = new boolean[width - 1][height][board.height];
		verticalBridges = new boolean[width][height - 1][board.width];

		notes = new Vector();
		
		region = "Europe";

		name = "";
		speech = "";

		this.file = file;
		modified = false;
	}

	public void setHorizontalBridge(boolean value, int column, int row, int top) {
		if ( 0 <= column && column < width - 1 )
			horizontalBridges[column][row][top - 1] = value;
	}

	public void setVerticalBridge(boolean value, int column, int row, int left) {
		if ( 0 <= row && row < height - 1 )
			verticalBridges[column][row][left - 1] = value;
	}

	public boolean getHorizontalBridge(int column, int row, int top) {
		return horizontalBridges[column][row][top - 1];
	}

	public boolean getVerticalBridge(int column, int row, int left) {
		return verticalBridges[column][row][left - 1];
	}

	public QBoard getBoard(int column, int row) {
		return boards[column][row];
	}

	public void setBoard(QBoard board, int column, int row) {
		boards[column][row] = board;
	}
	
	public boolean isModified() {
		return modified;
	}
	
	public void setModified(boolean mod) {
		modified = mod;
	}

	public String getName() {
		return name;
	}
	
	public void setName(String newName) {
		name = newName;
		
		modified = true;
	}

	public Iterator objectsIterator() {
		return new ObjectsIterator(boards);
	}

	public Iterator notesIterator() {
		return notes.iterator();
	}


	public void addNote(String newNote) {
		notes.add(newNote);

		modified = true;
	}

	public String getSpeech() {
		return speech;
	}
	
	public void setSpeech(String newSpeech) {
		speech = newSpeech;

		modified = true;
	}
	
	public File getFile() {
		return file;
	}

	public void setFile(File newFile) {
		file = newFile;
	}

	public int getWidth() {
		return width;
	}

	public int getHeight() {
		return height;
	}
	
	public String getRegion() {
		return region;
	}
	
	public void setRegion(String newRegion) {
		if ( !region.equals(newRegion) ) {
			region = newRegion;

			modified = true;
		}
	}
	
	public void save() throws Exception {
		Write.write(this);
		
		modified = false;	
	}
}

class ObjectsIterator implements java.util.Iterator {
	private QBoard boards[][];

	private int i, j;
	private boolean hasEnded; 
	
	private Iterator currentBoardIterator;
                                                                                                                             
	ObjectsIterator(QBoard[][] boards) {
		this.boards = boards;
		
		currentBoardIterator = null;
		
		gotoNext();
	}

	private void gotoNext() {
		if ( currentBoardIterator == null ) {
			i = j = 0;
			hasEnded = false;
		} else {
			if ( currentBoardIterator.hasNext() )
				return;
				
			j++;
		}
				
		while ( i < boards.length ) {
			while ( j < boards[i].length ) {
				if ( boards[i][j] != null ) {
					currentBoardIterator = boards[i][j].iterator();
				
					if ( currentBoardIterator.hasNext() )
						return;
				}
				
				j++;
			}
			
			i++;
			j = 0;
		}
		
		hasEnded = true;
	}

	public boolean hasNext() {
		return !hasEnded;
	}

	public Object next() throws NoSuchElementException {
		if ( hasNext() ) {
			Object obj = currentBoardIterator.next();
			
			gotoNext();
			
			return obj;
		} else
			throw new NoSuchElementException();
	}

	public void remove() throws UnsupportedOperationException {
		throw new UnsupportedOperationException();
	}
}