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

package org.lightless.heroscribe.export;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;

import javax.imageio.ImageIO;

import org.lightless.heroscribe.helper.BoardPainter;

public class ExportRaster {
	/* format should be either "png" or "jpg" */
	public static void write(File file, String format, BoardPainter boardPainter) throws Exception {
		BufferedImage image = new BufferedImage(
			boardPainter.framePixelSize.width,
			boardPainter.framePixelSize.height,
			BufferedImage.TYPE_INT_RGB);
			
		Graphics2D g = image.createGraphics();
		
		boardPainter.paint(null, 0, 0, g);
		
		ImageIO.write(image, format, file);
	}
}