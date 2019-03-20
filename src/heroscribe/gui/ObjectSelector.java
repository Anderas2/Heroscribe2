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

import org.lightless.heroscribe.list.Kind;
import org.lightless.heroscribe.list.LObject;

import java.awt.CardLayout;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.util.Iterator;
import java.util.TreeMap;

import javax.swing.*;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;

class ObjectSelector extends JPanel implements ItemListener, ListSelectionListener {
	private Gui gui;

	private JPanel objectsPanel;
	private CardLayout cardLayout;	
	private JComboBox kindsComboBox;
	private TreeMap kindList;	
	
	private String selectedObject;
	private int objectRotation;

	public ObjectSelector(Gui gui) {
		super();
		
		this.gui = gui;

		objectsPanel = new JPanel();
		cardLayout = new CardLayout();
		kindsComboBox = new JComboBox();
		kindList = new TreeMap();
		
		Iterator iterator;

		selectedObject = null;

		setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
		objectsPanel.setLayout(cardLayout);

		add(kindsComboBox);
		add(objectsPanel);

		iterator = gui.getObjects().kindsIterator();
		while ( iterator.hasNext() ) {
			Kind kind = (Kind) iterator.next();

			JList list = new JList(new DefaultListModel());

			list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

			kindList.put(kind.id, list);

			kindsComboBox.addItem(kind);

			objectsPanel.add(new JScrollPane(list), kind.id);

			list.addListSelectionListener( this );
		}
		
		iterator = gui.getObjects().objectsIterator();
		while ( iterator.hasNext() ) {
			LObject obj = (LObject) iterator.next();
			
			JList list = (JList) kindList.get( obj.kind );
			DefaultListModel listModel = (DefaultListModel) list.getModel();
			
			listModel.addElement(obj);
		}

		kindsComboBox.addItemListener( this );
	}
	
	public String getSelectedObject() {
		return selectedObject;
	}

	public int getSelectedObjectRotation() {
		return objectRotation;
	}

	private void setSelectedObject(LObject obj) {
		if ( obj != null ) {
			selectedObject = obj.id;
		} else {
			selectedObject = null;
		}

		gui.board.resetRotation();
	}

	/* -- */
	
	public void itemStateChanged(ItemEvent e) {
		if ( e.getStateChange() == ItemEvent.SELECTED ) {
			Kind selected;
			JList list;
			LObject obj;
				
			selected = (Kind) ((JComboBox) e.getSource()).getSelectedItem();
			cardLayout.show(objectsPanel, selected.id);
			list = (JList) kindList.get(selected.id);
				
			setSelectedObject((LObject) list.getSelectedValue());
			
			gui.updateHint();
		}
	}
		
	public void valueChanged(ListSelectionEvent e) {
		JList list;
				
		list = (JList) e.getSource();

		setSelectedObject((LObject) list.getSelectedValue());

		gui.updateHint();
	}
}

