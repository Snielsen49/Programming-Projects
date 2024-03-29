# Overview

This Java program is a simple paint application I created using the Swing framework. It provides a graphical user interface (GUI) where users can draw different shapes and lines, and paint with a brush tool. Here are the main components and functionalities of the program:

Main Window Setup: The PaintProgram class creates the main window, setting its size, title, and close operation. It organizes the layout with a drawing area in the center and a panel containing drawing tools at the bottom.

Tool Buttons: There are buttons for selecting drawing tools like a brush, line, ellipse, and rectangle. Additionally, there are buttons for choosing stroke and fill colors. These buttons are equipped with icons and are set up to change the current drawing mode when clicked.

Color Selection: The stroke and fill color buttons trigger a color chooser dialog, allowing the user to select colors for drawing outlines and filling shapes.

Transparency Control: A slider is provided for adjusting the transparency level of the drawing elements. This transparency affects how the shapes and brush strokes are rendered on the canvas.

Drawing Logic: The DrawScreen inner class extends JComponent and serves as the canvas for drawing.
Mouse listeners detect drag and drop actions to draw shapes or use the brush tool based on the selected mode.
The shapes and their attributes (stroke color, fill color, and transparency) are stored in arrays, allowing for dynamic drawing and rendering.

Rendering: The painting logic uses Java 2D graphics (Graphics2D) for rendering shapes with the specified properties like color and transparency.

[Software Demo Video](https://youtu.be/6ulf6aGDc4k)

# Development Environment

I used VS code to make this program. 

libraries included: 
javax.swing: Provides classes and interfaces for creating and managing graphical user interface (GUI) components like buttons, sliders, and windows.

javax.swing.event: Contains interfaces and classes for handling events in Swing components, such as changes in state or value.

java.awt.event: Defines classes and interfaces for handling different types of events generated by AWT components, such as mouse and keyboard events.

java.awt: Provides classes for creating and managing basic GUI components, layout managers, and graphics, including drawing shapes and text.

java.awt.geom: Offers classes for defining and performing operations on 2D geometry objects like shapes, points, lines, and areas.

java.util: Includes utility classes that are commonly used in Java programming, such as collections (lists, sets, maps) and date/time functions.

java.text.DecimalFormat: A class for formatting decimal numbers into strings with a specific pattern, often used for display purposes.

# Useful Websites

* [Youtube](https://www.youtube.com/)
For research purposes
* [Chat GPT](https://chat.openai.com/)
For asking questions and getting help


# Future Work

- Add a slider for brush thickness 
- A way to save Files 
- Undo button 
