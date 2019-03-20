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

import java.util.TreeMap;

public class LObject implements Comparable {
	public TreeMap region;
	
	public String id, name, kind, note;

	public int height, width;
	
	public float zorder;
	
	public boolean door, trap;
	
	public LObject() {
		region = new TreeMap();
	}
	
	public void putIcon(Icon icon, String region) {
		this.region.put(region, icon);
	}

	public Icon getIcon(String region) {
		return (Icon) this.region.get(region);
	}
	
	public int compareTo(Object o) {
		LObject that = (LObject) o;
		
		return name.compareTo(that.name);
	}

	public String toString() {
		return name;
	}
}