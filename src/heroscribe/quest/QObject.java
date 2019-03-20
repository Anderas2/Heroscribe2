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

import org.lightless.heroscribe.list.List;

public class QObject implements Comparable {
	public String id;
	public int rotation;
	public float top, left, zorder;
	
	private int order;
	private static int count = 0;

	private List objects;
	
	public QObject(String id, List objects) {
		this.id = id;
		this.objects = objects;
		
		if ( objects.list.containsKey(id) )
			order = getOrder();
	}
	
	public QObject(String id, List objects, int order) {
		this.id = id;
		this.objects = objects;
		
		this.order = order; 
	}
	
	synchronized private static int getOrder() {
		return ++count;
	}
	
	public int compareTo(Object o) {
		QObject that = (QObject) o;
		
		if ( this.zorder < that.zorder )
			return -1;
		else if ( this.zorder > that.zorder )
			return 1;
		else if ( this.order < that.order )
			return -1;
		else if ( this.order > that.order )
			return 1;
		
		return 0;
	}
	
	public String toString() {
		return objects.getObject(id).toString() + " ( " + Float.toString(zorder) + " )";
	}
}