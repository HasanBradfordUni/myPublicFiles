package uk.ac.bradford.diggame;

import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * The StartScreenGUI class is responsible for rendering graphics to the screen
 * to display the start screen. The StartScreenGUI class passes mouse events to
 * a registered StartInputHandler to be handled.
 *
 * @author hakhta26
 * @author prtrundl (original adapted)
 */
public class StartScreenGUI extends JFrame {

    /**
     * The two final int attributes below set the size of some graphical
     * elements, specifically the display height and width of buttons on the
     * start screen in the game. Button sizes should match the size of the image
     * files used in the game.
     */
    public static final int BUTTON_WIDTH = 100;
    public static final int BUTTON_HEIGHT = 50;
    private GameGUI gui = new GameGUI();
    private GameEngine eng = new GameEngine(gui, null);

    /**
     * The canvas is the area that graphics are drawn to. It is an internal
     * class of the GameGUI class.
     */
    Canvas2 canvas;

    /**
     * Constructor for the GameGUI class. It calls the initGUI method to
     * generate the required objects for display.
     */
    public StartScreenGUI() {
        initGUI();
    }

    /**
     * Registers an object to be passed mouse events captured by the GUI.
     *
     */
    public void registerMouseHandler() {
        canvas.mouseListenerEasy(eng, gui);
        canvas.mouseListenerMedium(eng, gui);
        canvas.mouseListenerHard(eng, gui);
        canvas.mouseListenerCustom(eng, gui);
    }

    /**
     * Method to create and initialise components for displaying elements of the
     * game on the screen.
     */
    private void initGUI() {
        add(canvas = new Canvas2());     //adds canvas to this frame
        setTitle("KomeDeeper");
        setSize(1000, 500);
        setLocationRelativeTo(null);        //sets position of frame on screen
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}

/**
 * Internal class used to draw elements within a JPanel. The Canvas class loads
 * images from an asset folder inside the main project folder.
 *
 * @author prtrundl
 */
class Canvas2 extends JPanel {

    private BufferedImage easyButton;
    private BufferedImage mediumButton;
    private BufferedImage hardButton;
    private BufferedImage customButton;
    private Point easyPoint;
    private Point mediumPoint;
    private Point hardPoint;
    private Point customPoint;

    /**
     * Constructor that loads button images for use in this class
     */
    public Canvas2() {
        loadButtons();
    }

    /**
     * Loads button images from a fixed folder location within the project
     * directory
     */
    private void loadButtons() {
        try {
            easyButton = ImageIO.read(new File("assets/EasyButton.png"));
            easyPoint = new Point(100, 300);
            mediumButton = ImageIO.read(new File("assets/MediumButton.png"));
            mediumPoint = new Point(300, 300);
            hardButton = ImageIO.read(new File("assets/HardButton.png"));
            hardPoint = new Point(500, 300);
            customButton = ImageIO.read(new File("assets/CustomButton.png"));
            customPoint = new Point(700, 300);

        } catch (IOException e) {
            System.out.println("Exception loading images: " + e.getMessage());
            e.printStackTrace(System.out);
        }
    }

    public void mouseListenerEasy(GameEngine eng, GameGUI gui) {
        Rectangle easy = new Rectangle(easyPoint,
                new Dimension(easyButton.getWidth(), easyButton.getHeight()));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                Point me = e.getPoint();
                if (easy.contains(me)) {
                    gui.setVisible(true);                 //display GUI
                    InputHandler i = new InputHandler(eng); //create input handler
                    gui.registerKeyHandler(i);              //registers handler with GUI
                    eng.startGame("Easy");
                }
            }
        });
    }

    public void mouseListenerMedium(GameEngine eng, GameGUI gui) {
        Rectangle medium = new Rectangle(mediumPoint,
                new Dimension(mediumButton.getWidth(), mediumButton.getHeight()));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                Point me = e.getPoint();
                if (medium.contains(me)) {
                    gui.setVisible(true);                 //display GUI
                    InputHandler i = new InputHandler(eng); //create input handler
                    gui.registerKeyHandler(i);
                    eng.startGame("Medium");
                }
            }
        }
        );
    }

    public void mouseListenerHard(GameEngine eng, GameGUI gui) {
        Rectangle hard = new Rectangle(hardPoint,
                new Dimension(hardButton.getWidth(), hardButton.getHeight()));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                Point me = e.getPoint();
                if (hard.contains(me)) {
                    gui.setVisible(true);                 //display GUI
                    InputHandler i = new InputHandler(eng); //create input handler
                    gui.registerKeyHandler(i);
                    eng.startGame("Hard");
                }
            }
        });
    }

    public void mouseListenerCustom(GameEngine eng, GameGUI gui) {
        Rectangle custom = new Rectangle(customPoint,
                new Dimension(customButton.getWidth(), customButton.getHeight()));
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                Point me = e.getPoint();
                if (custom.contains(me)) {
                    CustomGUI2 customScreen = new CustomGUI2();
                    customScreen.run();
                }
            }
        });
    }

    /**
     * Override of method in super class, it draws the custom elements for this
     * game such as the buttons.
     *
     * @param g Graphics drawing object
     */
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        drawButtons(g);
    }

    /**
     * Draws graphical elements to the screen to display the current game level
     * tiles, the player and the moles. If the currentTiles, currentPlayer or
     * currentMoles objects are null they will not be drawn.
     *
     * @param g
     */
    private void drawButtons(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;
        g2.drawImage(easyButton, 100, 300, null);
        g2.drawImage(mediumButton, 300, 300, null);
        g2.drawImage(hardButton, 500, 300, null);
        g2.drawImage(customButton, 700, 300, null);
        g2.dispose();
    }
}
