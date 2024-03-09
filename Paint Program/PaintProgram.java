import javax.swing.*;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import java.awt.event.*;
import java.awt.*;
import java.awt.geom.*;
import java.util.*;
import java.text.DecimalFormat;

public class PaintProgram extends JFrame 
{

    JButton brushButton, lineButton, ellipseButton, rectButton, strokeButton, fillButton;

    JSlider transSlider;

    JLabel transLabel;
    
    DecimalFormat dec = new DecimalFormat("#.##");

    Graphics2D graphicSettings;

    //button selection 
    int curentSelection = 1; 

    float transparicyValue = 1.0f;

    //setting up defalt colors 
    Color selectedColor = Color.BLACK; 
    Color fillColor = Color.BLACK;

    public static void main(String[] args){

        new PaintProgram();
    }

    public PaintProgram(){

        //setting up window 
        this.setSize(1000,700);
        this.setTitle("Paint Program");
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel buttonPanel = new JPanel();
        Box box1 = Box.createHorizontalBox();

        // drawing buttons
        brushButton = drawButtons("Paint Program/images/brush.png",1);
        lineButton = drawButtons("Paint Program/images/Line.png",2);
        ellipseButton = drawButtons("Paint Program/images/Ellipse.png",3);
        rectButton = drawButtons("Paint Program/images/Rectangle.png",4);

        strokeButton = drawColorButtons("Paint Program/images/Stroke.png", 5, true);
        fillButton = drawColorButtons("Paint Program/images/Fill.png", 6, false);

        box1.add(brushButton);
        box1.add(lineButton);
        box1.add(ellipseButton);
        box1.add(rectButton);
        box1.add(strokeButton);
        box1.add(fillButton);

        transLabel = new JLabel("Transparency: 1");
        transSlider = new JSlider(1,99,99);
        listenerForSlider sliderListener = new listenerForSlider();
        transSlider.addChangeListener(sliderListener);

        box1.add(transLabel);
        box1.add(transSlider);

        buttonPanel.add(box1);

        this.add(buttonPanel, BorderLayout.SOUTH);
        this.add(new DrawScreen(), BorderLayout.CENTER);
        this.setVisible(true);
    }

    // function to draw buttons
    public JButton drawButtons(String fileName, final int selection){

        JButton but = new JButton();
        Icon setIcon = new ImageIcon(fileName);
        but.setIcon(setIcon);

        //defining button action 
        but.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                curentSelection = selection;
                System.out.println("actionNum: " + curentSelection);
            }
        });
        return but;
    }

    // function to draw color buttons
    public JButton drawColorButtons(String fileName, final int selection, final boolean stroke){

        JButton but = new JButton();
        Icon setIcon = new ImageIcon(fileName);
        but.setIcon(setIcon);

        //defining button action 
        but.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                if(stroke)
                {
                    selectedColor = JColorChooser.showDialog(null, "Pick a stroke color", Color.BLACK);
                }
                else
                {
                    fillColor = JColorChooser.showDialog(null, "Pick a fill color", Color.BLACK);
                }
            }
        });
        return but;
    }

    private class DrawScreen extends JComponent{

        //lists of shapes drawn 
        ArrayList<Shape> shapes = new ArrayList<Shape>();
        ArrayList<Color> shapefill = new ArrayList<Color>();
        ArrayList<Color> shapestroke = new ArrayList<Color>();
        ArrayList<Float> shapesTrans = new ArrayList<Float>();
        Point drawStart, drawEnd;

        //gets events  on the screen 
        public DrawScreen(){

            //mouse button listener
            this.addMouseListener(new MouseAdapter()
            {
                //mouse click
                public void mousePressed(MouseEvent e)
                {
                    if(curentSelection != 1)
                    {
                        drawStart = new Point(e.getX(),e.getY());
                        drawEnd = drawStart;
                        repaint();
                    }
                }
                //mouse relesed
                public void mouseReleased(MouseEvent e)
                {
                    if(curentSelection != 1)
                    {
                        Shape newShape = null; 

                        //Line selected
                        if(curentSelection == 2)
                        {
                            newShape = drawLine(drawStart.x, drawStart.y, e.getX(), e.getY());
                        }
                        else
                        //Ellipse selected
                        if(curentSelection == 3)
                        {
                            newShape = drawEllipse(drawStart.x, drawStart.y, e.getX(), e.getY());
                        }
                        else
                        //Rectangle seleceted
                        if(curentSelection == 4)
                        {
                            newShape = drawRect(drawStart.x, drawStart.y, e.getX(), e.getY());
                        }
                        
                        shapes.add(newShape);
                        shapefill.add(fillColor);
                        shapestroke.add(selectedColor);
                        shapesTrans.add(transparicyValue);
                        

                        drawStart = null;
                        drawEnd = null;
                        repaint();
                    }

                }
            });

            //mouse movement listener
            this.addMouseMotionListener(new MouseMotionAdapter()
            {
                public void mouseDragged(MouseEvent e)
                {
                    //brush is selected 
                    if(curentSelection == 1)
                    {
                        int x = e.getX();
                        int y = e.getY();
                        Shape newShape = null;
                        selectedColor = fillColor;
                        newShape = drawBrush(x,y,2,2);
                        shapes.add(newShape);
                        shapefill.add(fillColor);
                        shapestroke.add(selectedColor);
                        shapesTrans.add(transparicyValue);
                    }
                    drawEnd = new Point(e.getX(),e.getY());
                    repaint();
                }

            });
        }

        public void paint(Graphics g)
        {
            graphicSettings = (Graphics2D)g;
            graphicSettings.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            //width of the stroke
            graphicSettings.setStroke(new BasicStroke(2));

            //iterators for the fill transparacy and stroke of the shapes 
            Iterator<Color> strokeIterator = shapestroke.iterator();
            Iterator<Color> fillIterator = shapefill.iterator();
            Iterator<Float> transIterator = shapesTrans.iterator();

          

            //drawing shapes 
            for(Shape s : shapes)
            {
                //looping through transparicy stroke and fill
                graphicSettings.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,transIterator.next()));
                graphicSettings.setPaint(strokeIterator.next());
                graphicSettings.draw(s);
                graphicSettings.setPaint(fillIterator.next());
                graphicSettings.fill(s);
            }

            //when drawing the shape 
            if (drawStart != null && drawEnd != null)
            {
                //ajusting transparicy 
                graphicSettings.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,0.4f));
                //setting color for outline
                graphicSettings.setPaint(Color.GRAY);

                Shape newShape = null; 

                 //Line selected
                 if(curentSelection == 2)
                 {
                     newShape = drawLine(drawStart.x, drawStart.y, drawEnd.x, drawEnd.y);
                 }
                 else
                 //Ellipse selected
                 if(curentSelection == 3)
                 {
                     newShape = drawEllipse(drawStart.x, drawStart.y, drawEnd.x, drawEnd.y);
                 }
                 else
                 //Rectangle seleceted
                 if(curentSelection == 4)
                 {
                     newShape = drawRect(drawStart.x, drawStart.y, drawEnd.x, drawEnd.y);
                 }

                
                graphicSettings.draw(newShape);
            }
        }
    }

    //drawing a rectangle 
    private Rectangle2D.Float drawRect(int x1, int y1, int x2, int y2)
    {
        int x = Math.min(x1,x2);
        int y = Math.min(y2, y1);
        int width = Math.abs(x1 - x2);
        int height = Math.abs(y1 - y2);

        return new Rectangle2D.Float(x, y, width, height);

    }

    //drawing a Ellipse
    private Ellipse2D.Float drawEllipse(int x1, int y1, int x2, int y2)
    {
        int x = Math.min(x1,x2);
        int y = Math.min(y2, y1);
        int width = Math.abs(x1 - x2);
        int height = Math.abs(y1 - y2);

        return new Ellipse2D.Float(x, y, width, height);
    }

    //drawing line 
    private Line2D.Float drawLine(int x1, int y1, int x2, int y2)
    {
        return new Line2D.Float(x1,y1,x2,y2);
    }

    //draw brush 
    private Ellipse2D.Float drawBrush(int x, int y, int brushHeight, int brushWidth)
    {
        return new Ellipse2D.Float(x,y,brushHeight,brushWidth);
    }

    // listener for the slider 
    private class listenerForSlider implements ChangeListener
    {
        public void stateChanged(ChangeEvent e)
        {
            if(e.getSource() == transSlider)
            {
                transLabel.setText("Transparency: " + dec.format(transSlider.getValue() * .01));
                transparicyValue = transSlider.getValue() * 0.01f;
            }
        }
    }

}