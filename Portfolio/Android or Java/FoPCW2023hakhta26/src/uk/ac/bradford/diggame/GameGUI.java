package uk.ac.bradford.diggame;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.geom.Rectangle2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * The GameGUI class is responsible for rendering graphics to the screen to
 * display the game level, player and moles. The GameGUI class passes keyboard
 * events to a registered GameInputHandler to be handled.
 *
 * @author prtrundl
 */
public class GameGUI extends JFrame {

    /**
     * The three final int attributes below set the size of some graphical
     * elements, specifically the display height and width of tiles in the game
     * and the height of fullness/energy bars for Entity objects in the game.
     * Tile sizes should match the size of the image files used in the game.
     */
    public static final int TILE_WIDTH = 32;
    public static final int TILE_HEIGHT = 32;
    public static final int BAR_HEIGHT = 3;

    /**
     * The canvas is the area that graphics are drawn to. It is an internal
     * class of the GameGUI class.
     */
    Canvas canvas;

    /**
     * Constructor for the GameGUI class. It calls the initGUI method to
     * generate the required objects for display.
     */
    public GameGUI() {
        initGUI();
    }

    /**
     * Registers an object to be passed keyboard events captured by the GUI.
     *
     * @param i the GameInputHandler object that will process keyboard events to
     * make the game respond to input
     */
    public void registerKeyHandler(InputHandler i) {
        addKeyListener(i);
    }

    /**
     * Method to create and initialise components for displaying elements of the
     * game on the screen.
     */
    private void initGUI() {
        add(canvas = new Canvas());     //adds canvas to this frame
        setTitle("KomeDeeper");
        setSize((GameEngine.levelWidth + 1) * TILE_WIDTH, (GameEngine.levelHeight + 1) * TILE_HEIGHT);
        setLocationRelativeTo(null);        //sets position of frame on screen
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    /**
     * Method to update the graphical elements on the screen, usually after
     * player and/or moles have moved when a keyboard event was handled. The
     * method requires three arguments and displays corresponding information on
     * the screen.
     *
     * @param tiles A 2-dimensional array of TileTypes. This is the tiles of the
     * current game level that should be drawn to the screen.
     * @param player A Player object. This object is used to draw the player in
     * the right tile and display its energy. null can be passed for this
     * argument, in which case no player will be drawn.
     * @param moles An array of Mole objects that is processed to draw moles
     * with a fullness bar in tiles. null can be passed for this argument in
     * which case no moles will be drawn. Elements in the moles array can also
     * be null, in which case nothing will be drawn for that array element.
     */
    public void updateDisplay(Tile[][] tiles, Player player, Mole[] moles) {
        canvas.update(tiles, player, moles);
        canvas.setSize((GameEngine.levelWidth + 1) * TILE_WIDTH, (GameEngine.levelHeight + 1) * TILE_HEIGHT);
        this.setSize(GameEngine.levelWidth * TILE_WIDTH, GameEngine.levelHeight * TILE_HEIGHT);
    }
}

/**
 * Internal class used to draw elements within a JPanel. The Canvas class loads
 * images from an asset folder inside the main project folder.
 *
 * @author prtrundl
 */
class Canvas extends JPanel {

    private BufferedImage empty;
    private BufferedImage dirt;
    private BufferedImage hardDirt;
    private BufferedImage rock;
    private BufferedImage player;
    private BufferedImage mole;
    private BufferedImage copper;
    private BufferedImage uranium;
    private BufferedImage silver;
    private BufferedImage damage1;
    private BufferedImage damage2;
    private BufferedImage damage3;
    private BufferedImage damage4;
    private BufferedImage damage5;
    private BufferedImage base;

    Tile[][] currentTiles;  //the current 2D array of tiles to display
    Player currentPlayer;       //the current player object to be drawn
    Mole[] currentMoles;   //the current array of moles to draw

    /**
     * Constructor that loads tile images for use in this class
     */
    public Canvas() {
        loadTileImages();
    }

    /**
     * Loads tiles images from a fixed folder location within the project
     * directory
     */
    private void loadTileImages() {
        try {
            empty = ImageIO.read(new File("assets/empty.png"));
            assert empty.getHeight() == GameGUI.TILE_HEIGHT
                    && empty.getWidth() == GameGUI.TILE_WIDTH;
            dirt = ImageIO.read(new File("assets/dirt.png"));
            assert dirt.getHeight() == GameGUI.TILE_HEIGHT
                    && dirt.getWidth() == GameGUI.TILE_WIDTH;
            hardDirt = ImageIO.read(new File("assets/harddirt.png"));
            assert hardDirt.getHeight() == GameGUI.TILE_HEIGHT
                    && hardDirt.getWidth() == GameGUI.TILE_WIDTH;
            rock = ImageIO.read(new File("assets/rock.png"));
            assert rock.getHeight() == GameGUI.TILE_HEIGHT
                    && rock.getWidth() == GameGUI.TILE_WIDTH;
            player = ImageIO.read(new File("assets/player.png"));
            assert player.getHeight() == GameGUI.TILE_HEIGHT
                    && player.getWidth() == GameGUI.TILE_WIDTH;
            copper = ImageIO.read(new File("assets/copper.png"));
            assert copper.getHeight() == GameGUI.TILE_HEIGHT
                    && copper.getWidth() == GameGUI.TILE_WIDTH;
            silver = ImageIO.read(new File("assets/silver.png"));
            assert silver.getHeight() == GameGUI.TILE_HEIGHT
                    && silver.getWidth() == GameGUI.TILE_WIDTH;
            uranium = ImageIO.read(new File("assets/uranium.png"));
            assert uranium.getHeight() == GameGUI.TILE_HEIGHT
                    && uranium.getWidth() == GameGUI.TILE_WIDTH;
            damage1 = ImageIO.read(new File("assets/damage1.png"));
            assert damage1.getHeight() == GameGUI.TILE_HEIGHT
                    && damage1.getWidth() == GameGUI.TILE_WIDTH;
            damage2 = ImageIO.read(new File("assets/damage2.png"));
            assert damage2.getHeight() == GameGUI.TILE_HEIGHT
                    && damage2.getWidth() == GameGUI.TILE_WIDTH;
            damage3 = ImageIO.read(new File("assets/damage3.png"));
            assert damage3.getHeight() == GameGUI.TILE_HEIGHT
                    && damage3.getWidth() == GameGUI.TILE_WIDTH;
            damage4 = ImageIO.read(new File("assets/damage4.png"));
            assert damage4.getHeight() == GameGUI.TILE_HEIGHT
                    && damage4.getWidth() == GameGUI.TILE_WIDTH;
            damage5 = ImageIO.read(new File("assets/damage5.png"));
            assert damage5.getHeight() == GameGUI.TILE_HEIGHT
                    && damage5.getWidth() == GameGUI.TILE_WIDTH;
            mole = ImageIO.read(new File("assets/mole.png"));
            assert mole.getHeight() == GameGUI.TILE_HEIGHT
                    && mole.getWidth() == GameGUI.TILE_WIDTH;
            base = ImageIO.read(new File("assets/base.png"));
            assert base.getHeight() == GameGUI.TILE_HEIGHT
                    && base.getWidth() == GameGUI.TILE_WIDTH;

        } catch (IOException e) {
            System.out.println("Exception loading images: " + e.getMessage());
            e.printStackTrace(System.out);
        }
    }

    /**
     * Updates the current graphics on the screen to display the tiles, player
     * and moles
     *
     * @param t The 2D array of TileTypes representing the current level of the
     * game
     * @param player The current player object, used to draw the player and its
     * energy
     * @param moles The array of moles to display on the level with their
     * fullness bar
     */
    public void update(Tile[][] t, Player player, Mole[] moles) {
        currentTiles = t;
        currentPlayer = player;
        currentMoles = moles;
        repaint();
    }

    /**
     * Override of method in super class, it draws the custom elements for this
     * game such as the tiles, player and moles.
     *
     * @param g Graphics drawing object
     */
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        drawLevel(g);
    }

    /**
     * Draws graphical elements to the screen to display the current game level
     * tiles, the player and the moles. If the currentTiles, currentPlayer or
     * currentMoles objects are null they will not be drawn.
     *
     * @param g
     */
    private void drawLevel(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;
        if (currentTiles != null) {
            for (int i = 0; i < currentTiles.length; i++) {
                for (int j = 0; j < currentTiles[i].length; j++) {
                    switch (currentTiles[i][j].getType()) {
                        case EMPTY:
                            g2.drawImage(empty, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case DIRT:
                            g2.drawImage(dirt, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case HARD_DIRT:
                            g2.drawImage(hardDirt, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case ROCK:
                            g2.drawImage(rock, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case COPPER:
                            g2.drawImage(copper, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case SILVER:
                            g2.drawImage(silver, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case URANIUM:
                            g2.drawImage(uranium, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                        case BASE:
                            g2.drawImage(base, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                            break;
                    }

                    if (currentTiles[i][j].getMaxDurability() > 0) {
                        double ratio = (double) currentTiles[i][j].getDurability() / (double) currentTiles[i][j].getMaxDurability();
                        if (ratio >= 1) {
                            continue;
                        } else if (ratio > 0.8) {
                            g2.drawImage(damage1, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                        } else if (ratio > 0.6) {
                            g2.drawImage(damage2, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                        } else if (ratio > 0.4) {
                            g2.drawImage(damage3, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                        } else if (ratio > 0.2) {
                            g2.drawImage(damage4, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                        } else {
                            g2.drawImage(damage5, i * GameGUI.TILE_WIDTH, j * GameGUI.TILE_HEIGHT, null);
                        }
                    }
                }
            }
        }
        if (currentMoles != null) {
            for (Mole m : currentMoles) {
                if (m != null) {
                    g2.drawImage(mole, m.getX() * GameGUI.TILE_WIDTH, m.getY() * GameGUI.TILE_HEIGHT, null);
                    drawFullnessBar(g2, m);
                }
            }
        }
        if (currentPlayer != null) {
            g2.drawImage(player, currentPlayer.getX() * GameGUI.TILE_WIDTH, currentPlayer.getY() * GameGUI.TILE_HEIGHT, null);
            drawEnergyBar(g2, currentPlayer);
        }
        g2.dispose();
    }

    /**
     * Draws a fullness bar for the given Mole at the bottom of the tile that
     * the Mole is located in.
     *
     * @param g2 The graphics object to use for drawing
     * @param g The mole that the patience bar will be drawn for
     */
    private void drawFullnessBar(Graphics2D g2, Mole g) {
        g2.setColor(Color.GREEN);
        g2.fill(new Rectangle2D.Double(g.getX() * GameGUI.TILE_WIDTH, g.getY() * GameGUI.TILE_HEIGHT + 29, GameGUI.TILE_WIDTH, GameGUI.BAR_HEIGHT));
        if (g.getFullness() > 0) {
            double fullRatio = (double) g.getFullness() / (double) g.getMaxFullness();
            g2.setColor(Color.RED);
            g2.fill(new Rectangle2D.Double(g.getX() * GameGUI.TILE_WIDTH, g.getY() * GameGUI.TILE_HEIGHT + 29, GameGUI.TILE_WIDTH * fullRatio, GameGUI.BAR_HEIGHT));
        }
    }

    /**
     * Draws an energy bar for the given Player at the bottom of the tile that
     * the Player is located in.
     *
     * @param g2 The graphics object to use for drawing
     * @param p The Player that the energy bar will be drawn for
     */
    private void drawEnergyBar(Graphics2D g2, Player p) {
        double remainingEnergy = (double) p.getEnergy() / (double) p.getMaxEnergy();
        g2.setColor(Color.BLUE);
        g2.fill(new Rectangle2D.Double(p.getX() * GameGUI.TILE_WIDTH, p.getY() * GameGUI.TILE_HEIGHT + 29, GameGUI.TILE_WIDTH, GameGUI.BAR_HEIGHT));
        g2.setColor(Color.CYAN);
        g2.fill(new Rectangle2D.Double(p.getX() * GameGUI.TILE_WIDTH, p.getY() * GameGUI.TILE_HEIGHT + 29, GameGUI.TILE_WIDTH * remainingEnergy, GameGUI.BAR_HEIGHT));
    }
}
