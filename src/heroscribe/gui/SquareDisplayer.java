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

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Iterator;
import java.util.TreeSet;

import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

import org.lightless.heroscribe.list.LObject;
import org.lightless.heroscribe.quest.QObject;

class SquareDisplayer extends JPanel implements ListSelectionListener, ActionListener {
	Gui gui;
	
	JTextField zorder;
	JButton set, remove, rotate;
	
	TreeSet selected;
	
	JList list;
	JPanel panel;
	
	int lastColumn, lastRow;
	int lastLeft, lastTop;

	public SquareDisplayer(Gui gui) {
		super();
		
		this.gui = gui;
		
		setLayout(new BorderLayout());

		selected = new TreeSet();

		list = new JList(new DefaultListModel());
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		list.addListSelectionListener(this);
		
		panel = new JPanel();
		panel.setLayout(new GridLayout(2, 2));
		panel.setBorder(BorderFactory.createEmptyBorder(2, 0, 0, 0));

		zorder = new JTextField();
		set = new JButton("Set zorder");
		remove = new JButton("Remove");
		rotate = new JButton("Rotate");
		
		zorder.setEnabled(false);
		set.setEnabled(false);
		remove.setEnabled(false);
		rotate.setEnabled(false);
		
		set.addActionListener(this);
		remove.addActionListener(this);
		rotate.addActionListener(this);

		panel.add(zorder);
		panel.add(set);
		panel.add(rotate);
		panel.add(remove);

		this.add(new JScrollPane(list));
		this.add(panel, BorderLayout.SOUTH);
	}
	
	public void clearList() {
		((DefaultListModel) list.getModel()).clear();
	}
	
	public void createList(int column, int row, int left, int top) {
		int width, height;
		
		lastColumn = column;
		lastRow = row;
		lastLeft = left;
		lastTop = top;

		selected.clear();
		
		Iterator iterator = gui.getQuest().getBoard(column, row).iterator();
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
			
			if ( qobj.left <= left && left < qobj.left + width &&
				qobj.top <= top && top < qobj.top + height ) {
					selected.add(qobj);
			}
		}
	
		updateList();
	}

	public void updateList() {
		clearList();
		
		Iterator iterator = selected.iterator();
		while ( iterator.hasNext() ) {
			QObject qobj = (QObject) iterator.next();
			
			((DefaultListModel) list.getModel()).add(0, qobj);
		}

		if ( ((DefaultListModel) list.getModel()).size() > 0 )
			list.setSelectedIndex(0);
	}

	public void valueChanged(ListSelectionEvent e) {
		JList list = (JList) e.getSource();
		
		QObject obj = (QObject) list.getSelectedValue();
		
		if ( obj != null ) {
			zorder.setText(Float.toString(obj.zorder));
			
			zorder.setEnabled(true);
			set.setEnabled(true);
			remove.setEnabled(true);
			rotate.setEnabled(true);
		} else {
			zorder.setText("");
			
			zorder.setEnabled(false);
			set.setEnabled(false);
			remove.setEnabled(false);
			rotate.setEnabled(false);
		}
	}

	public void actionPerformed(ActionEvent e) {
		QObject obj = (QObject) list.getSelectedValue();
		JButton button = (JButton) e.getSource();
			
		if ( obj != null ) {
			gui.getQuest().getBoard(lastColumn, lastRow).removeObject(obj);
			selected.remove(obj);
		}

		if ( button == set ) {
			obj.zorder = Float.parseFloat(zorder.getText());
			zorder.setText(Float.toString(obj.zorder));
		} else if ( button == remove ) {
			obj = null;
		} else if ( button == rotate ) {
			obj.rotation = (obj.rotation + 1) % 4;
		}

		if ( obj != null ) {
			gui.getQuest().getBoard(lastColumn, lastRow).addObject(obj);
			selected.add(obj);
		}
		
		gui.updateTitle();
		gui.board.repaint();
		
		updateList();
		
		if ( obj != null )
			list.setSelectedValue(obj, true);
	}
	
	
}