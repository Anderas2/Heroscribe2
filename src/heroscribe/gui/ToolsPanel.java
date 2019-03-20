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
import java.awt.CardLayout;
import java.awt.GridLayout;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;

import javax.swing.*;
import javax.swing.border.EtchedBorder;

class ToolsPanel extends JPanel implements ItemListener {
	Gui gui;
	ObjectSelector selectorPanel;
	SquareDisplayer displayerPanel;
	
	ButtonGroup commands;
	ItemListener listener;
	JToggleButton add, select, dark, none;
	
	JPanel extraPanel;
	
	String selected;

	public ToolsPanel(Gui gui) {
		this.gui = gui;

		setLayout(new BorderLayout());
		setBorder(BorderFactory.createEtchedBorder(EtchedBorder.LOWERED));

		selected = null;

		extraPanel = new JPanel();

		commands = new ButtonGroup();
		
		add = new JToggleButton("Add object");
		select = new JToggleButton("Select/Remove object");
		dark = new JToggleButton("Dark/Bridge");
		none = new JToggleButton();
		
		commands.add(add);
		commands.add(select);
		commands.add(dark);
		commands.add(none);
		
		JPanel modePanel = new JPanel();
		modePanel.setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		modePanel.setLayout(new GridLayout(3, 1));
		
		modePanel.add(add);
		modePanel.add(select);
		modePanel.add(dark);
		
		selectorPanel = new ObjectSelector(gui);
		selectorPanel.setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		
		displayerPanel = new SquareDisplayer(gui);
		displayerPanel.setBorder(BorderFactory.createEmptyBorder(2, 2, 2, 2));
		
		this.add(modePanel, BorderLayout.NORTH);
		this.add(extraPanel);
		
		extraPanel.setLayout(new CardLayout());
		
		extraPanel.add(new JPanel(), "empty");
		extraPanel.add(selectorPanel, "add");
		extraPanel.add(displayerPanel, "select");

		add.addItemListener(this);
		select.addItemListener(this);
		dark.addItemListener(this);
	}

	public void deselectAll() {
		add.setSelected(false);
		select.setSelected(false);
		dark.setSelected(false);
	}

	public String getCommand() {
		return selected;
	}

	public void itemStateChanged(ItemEvent e) {
		JToggleButton source = (JToggleButton) e.getSource();
				
		if ( e.getStateChange() == ItemEvent.SELECTED ) {
			if ( source == add ) {
				selected = "add";
				((CardLayout) extraPanel.getLayout()).show(extraPanel, selected);
			} else if (source == select) {
				selected = "select";
				displayerPanel.clearList();
				((CardLayout) extraPanel.getLayout()).show(extraPanel, selected);
			} else if (source == dark) {
				selected = "darken";
			} else if (source == none) {
				selected = null;
			}

			gui.updateHint();
		} else {
			selected = null;
			((CardLayout) extraPanel.getLayout()).show(extraPanel, "empty");
		}
	}
}

