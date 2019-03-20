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
import java.util.Iterator;
import java.util.TreeSet;

import org.lightless.heroscribe.helper.OS;

public class List {
	public LBoard board;
	
	public TreeMap list;
	public TreeSet kinds;
	
	public String version;
	public String vectorPrefix, vectorSuffix;
	public String rasterPrefix, rasterSuffix;
	public String samplePrefix, sampleSuffix;

	public List() {
		list = new TreeMap();
		kinds = new TreeSet();
	}

	public Iterator objectsIterator() {
		/* I know it's unefficient, but I need the objects ordered by value, not key
		 * (i.e. by name, not id) */
		
		return new TreeSet(list.values()).iterator();
	}

	public Iterator kindsIterator() {
		return kinds.iterator();
	}

	public LObject getObject(String id) {
		return (LObject) list.get(id);
	}

	public LBoard getBoard() {
		return board;
	}

	public Kind getKind(String id) {
		Iterator iterator = kindsIterator();
		Kind found = null;
		
		while ( iterator.hasNext() ) {
			Kind kind = (Kind) iterator.next();
			if ( id.equals(kind.id) ) {
				found = kind;
				break;
			}
		}

		return (Kind) found;
	}
	
	public String getVectorPath(String id, String region) {
		return OS.getAbsolutePath(vectorPrefix +
				getObject(id).getIcon(region).path + vectorSuffix);
	}

	public String getRasterPath(String id, String region) {
		return OS.getAbsolutePath(rasterPrefix +
				getObject(id).getIcon(region).path + rasterSuffix);
	}

	public String getSamplePath(String id, String region) {
		return OS.getAbsolutePath(samplePrefix +
					getObject(id).getIcon(region).path + sampleSuffix);
	}

	public String getVectorPath(String region) {
		return OS.getAbsolutePath(vectorPrefix +
				getBoard().getIcon(region).path + vectorSuffix);
	}

	public String getRasterPath(String region) {
		return OS.getAbsolutePath(rasterPrefix +
				getBoard().getIcon(region).path + rasterSuffix);
	}

	public String getSamplePath(String region) {
		return OS.getAbsolutePath(samplePrefix +
				getBoard().getIcon(region).path + sampleSuffix);
	}

}
