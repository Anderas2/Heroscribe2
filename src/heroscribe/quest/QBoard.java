package org.lightless.heroscribe.quest;

import java.util.Iterator;
import java.util.TreeSet;

public class QBoard {
	private boolean[][] dark;

	private TreeSet objects;
	
	private Quest quest;
	
	private int width, height;
	
	public QBoard(int width, int height, Quest quest) {
		this.quest = quest;
		this.width = width;
		this.height = height;
		
		objects = new TreeSet();
		
		dark = new boolean[width][height];
	}

	public int getWidth() {
		return width;
	}

	public int getHeight() {
		return height;
	}

	public boolean isDark(int left, int top) {
		if ( left == 0 || left == width + 1 ||
			top == 0 || top == height + 1 )
			return false;
		else
			return dark[left - 1][top - 1];
	}

	public void toggleDark(int left, int top) {
		if ( left == 0 || left == width + 1 ||
			top == 0 || top == height + 1 )
			return;
			
		dark[left - 1][top - 1] = !dark[left - 1][top - 1];

		quest.setModified(true);
	}

	public boolean addObject(QObject newObj) {
		Iterator iterator = iterator();
		
		while (iterator.hasNext()) {
			QObject obj = (QObject) iterator.next();

			if ( obj.left == newObj.left &&
				obj.top == newObj.top &&
				obj.rotation == newObj.rotation &&
				obj.id.equals(newObj.id) )
				return false;
		}

		objects.add(newObj);

		quest.setModified(true);

		return true;
	}
	
	public boolean removeObject(QObject obj) {
		if ( objects.remove(obj) ) {
			quest.setModified(true);
			
			return true;
		} else
			return false;
	}

	public Iterator iterator() {
		return objects.iterator();
	}
	

}
