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

package org.lightless.heroscribe.list;

public class Kind implements Comparable{
	public String id, name;

	private int order;
	private static int count = 0;
	
	public Kind(String id, String name) {
		this.order = getOrder();
		
		this.id = id;
		this.name = name;
	}

	synchronized private static int getOrder() {
		return count++;
	}
	
	public int compareTo(Object o) {
		Kind that = (Kind) o;
		
		if ( this.order < that.order )
			return -1;
		else if ( this.order > that.order )
			return 1;

		return 0;
	}

	public String toString() {
		return name;
	}
}