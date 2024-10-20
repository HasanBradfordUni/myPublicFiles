package uk.ac.bradford.diggame;

import java.util.Arrays;
import java.util.Random;
import uk.ac.bradford.diggame.Tile.TileType;

/**
 * The GameEngine class is responsible for managing information about the game,
 * creating levels, the player and moles, as well as updating information when a
 * key is pressed (processed by the InputHandler) while the game is running.
 *
 * @author prtrundl
 */
public class GameEngine {

    /**
     * The width of the level, measured in tiles. Changing this may cause the
     * display to draw incorrectly, and as a minimum the size of the GUI would
     * need to be adjusted.
     */
    public static int levelWidth;

    /**
     * The height of the level, measured in tiles. Changing this may cause the
     * display to draw incorrectly, and as a minimum the size of the GUI would
     * need to be adjusted.
     */
    public static int levelHeight;

    /**
     * A random number generator that can be used to include randomised choices
     * in the creation of levels, in choosing places to place the player and
     * moles, and to randomise movement etc. Passing an integer (e.g. 123) to
     * the constructor called here will give fixed results - the same numbers
     * will be generated every time WHICH CAN BE VERY USEFUL FOR TESTING AND
     * BUGFIXING!
     */
    private final Random rng = new Random();

    /**
     * The current level number for the game. As the player completes levels the
     * level number should be increased and can be used to increase the
     * difficulty e.g. by creating additional moles and reducing patience etc.
     */
    private int levelNumber = 1;  //current level

    /**
     * The current turn number. Increased by one every turn. Used to control
     * effects that only occur on certain turn numbers.
     */
    private int turnNumber = 0;

    /**
     * The current score in this game.
     */
    private int score = 0;

    /**
     * The current mining strength of the player, used to calculate durability
     * reductions when the player mines a tile.
     */
    private int miningStrength = 5;

    /**
     * The GUI associated with this GameEngine object. This link allows the
     * engine to pass level and entity information to the GUI to be drawn.
     */
    private GameGUI gui;

    /**
     * The 2 dimensional array of tiles that represent the current level. The
     * size of this array should use the LEVEL_HEIGHT and LEVEL_WIDTH attributes
     * when it is created. This is the array that is used to draw images to the
     * screen by the GUI class.
     */
    private Tile[][] level;

    /**
     * A Player object that is the current player. This object stores the state
     * information for the player, including energy and the current position
     * (which is a pair of co-ordinates that corresponds to a tile in the
     * current level - see the Entity class for more information on the
     * co-ordinate system used as well as the coursework specification
     * document).
     */
    private Player player;

    /**
     * An array of Mole objects that represents the moles in the current level
     * of the game. Elements in this array should be either an object of the
     * type Mole or should be null (which means nothing is drawn or processed
     * for movement). null values in this array are skipped during drawing and
     * movement processing. Moles that "explode" can be replaced with the value
     * null in this array which removes them from the game, using syntax such as
     * moles[i] = null
     */
    private Mole[] moles;

    /**
     * A variable used for checking when the game dimensions should be made
     * smaller when mining Uranium tiles. If the Uranium tile is not yet
     * destroyed then the value will continue to decrease. If it is destroyed,
     * the dimensions of the game will decrease and the value will be 'reset' to 12.
     */
    private static int minesLeft = 12;
    
    /**
     * A String variable used for setting and checking the difficulty of the game.
     * It is checked when generating levels and adding moles as to how many moles
     * should spawn and what the level should roughly look like. It is set when 
     * starting the game and the value is passed from the start screen
     */
    private String gameDifficulty;
    
    /**
     * An integer variable for setting the number of Moles in CUSTOM mode.
     */
    private int molesNum;
    
    private int playerX;
    private int playerY;
    private int playerMaxEnergy;

    /**
     * Constructor that creates a GameEngine object and connects it with a
     * GameGUI object.
     *
     * @param gui The GameGUI object that this engine will pass information to
     * in order to draw levels and entities to the screen.
     * @param gameAttributes The attributes of the game. Usually null but if it's
     * custom mode then it's full.
     */
    public GameEngine(GameGUI gui, int[] gameAttributes) {
        this.gui = gui;
        if (gameAttributes != null) {
            System.out.println(Arrays.toString(gameAttributes));
            levelHeight = gameAttributes[0];
            levelWidth = gameAttributes[1];
            molesNum = gameAttributes[2];
            miningStrength = gameAttributes[3];
            playerX = gameAttributes[4];
            playerY = gameAttributes[5];
            playerMaxEnergy = gameAttributes[6];
        } else {
            levelHeight = 18;
            levelWidth = 35;
        }
    }

    public void mineAll() {
        for (int i = 0; i < level.length; i++) {
            for (int j = 0; j < level[i].length; j++) {
                level[i][j].mine(100);
            }
        }

    }

    public void spawnBase() {
        int playerX = player.getX();
        int playerY = player.getY();
        level[playerX][playerY] = new Tile(TileType.BASE);
    }

    /**
     * Generates a new level. This method should instantiate the level array,
     * which is an attribute of the GameEngine class and is declared above, and
     * then fill it with Tile objects that are created inside this method. It is
     * recommended that for your first version of this method you fill the 2D
     * array using for loops, and create new Tile objects inside the inner loop,
     * assigning them to an element in the array. For the first version you
     * should use just Tile objects with the type EMPTY. You will need to check
     * the constructor from the Tile class in order to create new Tile objects
     * inside your nested loops.
     *
     * Later tasks will require additions to this method to add new content, see
     * the specification document for more details.
     */
    private void generateLevel() {
        //First, the array for the level is instantiated
        level = new Tile[levelWidth][levelHeight];
        //Initialise variables for the chances that a tile will be different to empty
        int dirtChance = 0;
        int hardDirtChance = 0;
        int rockChance = 0;
        int baseChance = 0;
        int copperChance = 0;
        int silverChance = 0;
        int uraniumChance = 0;
        System.out.println(gameDifficulty);
        switch (gameDifficulty) {
            case "Easy":
                dirtChance = 65;
                hardDirtChance = 50;
                rockChance = 40;
                baseChance = 32;
                copperChance = 25;
                silverChance = 15;
                uraniumChance = 5;
                break;
            case "Medium":
                dirtChance = 55;
                hardDirtChance = 40;
                rockChance = 36;
                baseChance = 34;
                copperChance = 30;
                silverChance = 20;
                uraniumChance = 10;
                break;
            case "Hard":
                dirtChance = 50;
                hardDirtChance = 37;
                rockChance = 32;
                baseChance = 30;
                copperChance = 35;
                silverChance = 25;
                uraniumChance = 15;
                break;
            default:
                dirtChance = 75;
                hardDirtChance = 57;
                rockChance = 42;
                baseChance = 35;
                copperChance = 30;
                silverChance = 25;
                uraniumChance = 20;
        }

        //Next, using a nested FOR loop to iterate over the array
        for (int i = 0; i < level.length; i++) {
            for (int j = 0; j < level[i].length; j++) {
                //Generate a random number between 0 and 99 (inclusive) to be used for the tile chance 
                int randomChance = rng.nextInt(100);
                //Uses an if-elseif-else structure to define which tile type will be in that position of the array
                if (uraniumChance > randomChance) {
                    level[i][j] = new Tile(TileType.URANIUM);
                } else if (silverChance > randomChance) { //checks if the chance (random number) is less than silverChance
                    //Fills the current element of the array with a Tile of type COPPER
                    level[i][j] = new Tile(TileType.SILVER);
                } else if (copperChance > randomChance) { //checks if the chance (random number) is less than copperChance
                    //Fills the current element of the array with a Tile of type COPPER
                    level[i][j] = new Tile(TileType.COPPER);
                } else if (baseChance > randomChance) { //checks if the chance (random number) is less than copperChance
                    //Fills the current element of the array with a Tile of type COPPER
                    level[i][j] = new Tile(TileType.BASE);
                } else if (rockChance > randomChance) { //checks if the chance (random number) is less than copperChance
                    //Fills the current element of the array with a Tile of type COPPER
                    level[i][j] = new Tile(TileType.ROCK);
                } else if (hardDirtChance > randomChance) { //checks if the chance (random number) is less than copperChance
                    //Fills the current element of the array with a Tile of type COPPER
                    level[i][j] = new Tile(TileType.HARD_DIRT);
                } else if (dirtChance > randomChance) { //checks if the chance (random number) is less than dirtChance
                    //Fills the current element of the array with a Tile of type DIRT
                    level[i][j] = new Tile(TileType.DIRT);
                } else { //if all the above conditions aren't met then executes this
                    //Fills the current element of the array with a Tile of type EMPTY
                    level[i][j] = new Tile(TileType.EMPTY);
                }
            }
        }
    }

    /**
     * Adds moles in suitable locations in the current level. The first version
     * of this method should picked fixed positions for moles by calling the
     * constructor for the Mole class and using fixed values for the fullness, X
     * and Y positions of the Mole to be added.
     *
     * Mole objects created this way should then be added into the moles array
     * that is part of the GameEngine class. Mole objects added to the moles
     * array will then be drawn to the screen using the existing code in the
     * GameGUI class.
     *
     * The second version of this method (described in a later task) should
     * improve the placement of moles by generating random values for the X and
     * Y position of the mole before instantiating the Mole object. You may like
     * to use a loop to do this.
     */
    private void addMoles() {
        moles = new Mole[10];
        int maxFullness = 0; int moleNum = 0; 
        maxFullness = switch (levelNumber) {
            case 1 ->
                100;
            case 2 ->
                50;
            case 3 ->
                25;
            default ->
                10;
        };
        System.out.println(gameDifficulty);
        moleNum = switch (gameDifficulty) {
            case "Easy" -> 3;
            case "Medium" -> 5;
            case "Hard" -> 7;
            case "Custom" -> molesNum;
            default -> 5;
        };
        for (int i = 0; i < moleNum; i++) {
            int moleX = rng.nextInt(levelWidth);
            int moleY = rng.nextInt(levelHeight);
            moles[i] = new Mole(maxFullness, moleX, moleY); 
        }
        if (levelNumber > 1) {
            moles[6] = new Mole(maxFullness, 15, 14);
        }
        if (levelNumber > 2) {
            moles[8] = new Mole(maxFullness, 21, 32);
        }
        if (levelNumber > 3) {
            moles[9] = new Mole(maxFullness, 10, 4);
        }
    }

    /**
     * Creates a Player object in the game. The method instantiates the Player
     * class and assigns values for the energy and position.
     *
     * The first version of this method should use a fixed position for the
     * player to start, by setting fixed X and Y values when calling the
     * constructor in the Player class. The object created should be assigned to
     * the player attribute of this class.
     *
     * The second version of this method should use a suitable method to
     * determine where the BASE in the level is and place the Player on the tile
     * representing the BASE.
     *
     */
    private void createPlayer() {
        //finally the Player class will be instantiated with all 3 values
        if (gameDifficulty.equals("Custom")) {
            player = new Player(playerMaxEnergy, playerX, playerY);
        } else {
            player = new Player(100, 10, 5);
        }
    }

    /**
     * Handles the movement of the player when attempting to move in the game.
     * This method is automatically called by the GameInputHandler class when
     * the user has pressed one of the arrow keys on the keyboard. The method
     * should check which direction for movement is required, by checking which
     * character was passed to this method (see parameter description below).
     * Your code should alter the X and Y position of the player to place them
     * in the correct tile based on the direction of movement.
     *
     * If the target tile is not EMPTY then the player should not be moved, but
     * other effects may happen such as mining. To achieve this, the target tile
     * should be checked to determine the type of tile and appropriate methods
     * called or attribute values changed.
     *
     * @param direction A char representing the direction that the player should
     * move. N is up, S is down, W is left and E is right.
     */
    public void movePlayer(char direction) {
        //First the current X and Y co-ordinates of the Player will be taken
        int playerX = player.getX();
        int playerY = player.getY();
        TileType minedTileType;
        //next a series of switch-case statements will be used to check the direction and implement the movement accordingly
        switch (direction) {
            case 'N': //The case is N which means the player will be moving up
                //uses the setPosition() method of player with the updated X and Y values and checks if the player is going off the screen
                if (!(playerY - 1 < 0)) {
                    Tile currentTile = level[playerX][playerY - 1];
                    if (currentTile.getType() == TileType.EMPTY) {
                        player.setPosition(playerX, playerY - 1);
                    } else if (currentTile.getType() == TileType.BASE) {
                        player.refillEnergy();
                        player.setPosition(playerX, playerY - 1);
                    } else {
                        if (currentTile.getType() == TileType.SILVER) {
                            explode(playerX, playerY - 1, 100);
                            score += 2;
                        } if (currentTile.getType() == TileType.COPPER) {
                            score++;
                        }
                        minedTileType = currentTile.mine(miningStrength);
                        player.changeEnergy(-5);
                        if (minedTileType == TileType.URANIUM) {
                            miningStrength += 5;
                            score += 5;
                        }
                    }
                }
                break; //makes sure the player doesn't move multiple directions so breaks it
            case 'S': //The case is S which means the player will be moving down
                //uses the setPosition() method of player with the updated X and Y values
                if (!(playerY + 1 > levelHeight - 1)) {
                    Tile currentTile = level[playerX][playerY + 1];
                    if (currentTile.getType() == TileType.EMPTY) {
                        player.setPosition(playerX, playerY + 1);
                    } else if (currentTile.getType() == TileType.BASE) {
                        player.refillEnergy();
                        player.setPosition(playerX, playerY + 1);
                    } else {
                        if (currentTile.getType() == TileType.SILVER) {
                            explode(playerX, playerY + 1, 100);
                            score += 2;
                        } if (currentTile.getType() == TileType.COPPER) {
                            score++;
                        }
                        minedTileType = currentTile.mine(miningStrength);
                        player.changeEnergy(-5);
                        if (minedTileType == TileType.URANIUM) {
                            miningStrength += 5;
                            score += 5;
                        }
                    }
                }
                break; //makes sure the player doesn't move multiple directions so breaks it
            case 'W': //The case is W which means the player will be moving left
                //uses the setPosition() method of player with the updated X and Y values
                if (!(playerX - 1 < 0)) {
                    Tile currentTile = level[playerX - 1][playerY];
                    if (currentTile.getType() == TileType.EMPTY) {
                        player.setPosition(playerX - 1, playerY);
                    } else if (currentTile.getType() == TileType.BASE) {
                        player.refillEnergy();
                        player.setPosition(playerX - 1, playerY);
                    } else {
                        if (currentTile.getType() == TileType.SILVER) {
                            explode(playerX - 1, playerY, 100);
                            score += 2;
                        } if (currentTile.getType() == TileType.COPPER) {
                            score++;
                        }
                        minedTileType = currentTile.mine(miningStrength);
                        player.changeEnergy(-5);
                        if (minedTileType == TileType.URANIUM) {
                            miningStrength += 5;
                            score += 5;
                        }
                    }
                }
                break; //makes sure the player doesn't move multiple directions so breaks it
            case 'E': //The case is E which means the player will be moving right
                //uses the setPosition() method of player with the updated X and Y values
                if (!(playerX + 1 > levelWidth - 1)) {
                    Tile currentTile = level[playerX + 1][playerY];
                    if (currentTile.getType() == TileType.EMPTY) {
                        player.setPosition(playerX + 1, playerY);
                    } else if (currentTile.getType() == TileType.BASE) {
                        player.refillEnergy();
                        player.setPosition(playerX + 1, playerY);
                    } else {
                        if (currentTile.getType() == TileType.SILVER) {
                            explode(playerX + 1, playerY, 100);
                            score += 2;
                        } if (currentTile.getType() == TileType.COPPER) {
                            score++;
                        }
                        minedTileType = currentTile.mine(miningStrength);
                        player.changeEnergy(-5);
                        if (minedTileType == TileType.URANIUM) {
                            miningStrength += 5;
                            score += 5;
                        }
                    }
                }
        }
    }

    /**
     * Moves all moles on the current level. This method iterates over all
     * elements of the moles array (using a for loop) and checks if each one is
     * null (using an if statement inside that for loop). For every element of
     * the array that is NOT null, this method calls the moveMole method and
     * passes it the current array element (i.e. the current mole object being
     * used in the loop).
     */
    private void moveAllMoles() {
        //uses an enhanced for loop to iterate through the array
        for (Mole mole : moles) {
            if (mole != null) {
                moveMole(mole); //calls the moveMole() method for the current mole  
            }
        }
    }

    /**
     * Moves a specific mole in the game. The method updates the X and Y
     * attributes of the Mole object passed to the method to set its new
     * position.
     *
     * @param m The Mole that needs to be moved
     */
    private void moveMole(Mole m) {
        //implements a similar structure to the movePlayer method except the direction is chosen randomly
        int moleX = m.getX(); //gets the current x coord of the mole
        int moleY = m.getY(); //gets the current y coord of the mole
        int playerX = player.getX();
        int playerY = player.getY();
        int direction = rng.nextInt(1, 5); //generates a random number for the direction between 1 & 4
        boolean movementValid;
        int thisMoleX;
        int thisMoleY;
        //the switch-case statement that decides which direction the mole is moving
        switch (direction) {
            case 1: //The case is 1 which means the mole will be moving up
                movementValid = true;
                for (Mole mole : moles) {
                    if (mole != null) {
                        thisMoleY = mole.getY();
                        if (thisMoleY == moleY - 1) {
                            movementValid = false;
                        }
                    }
                }
                if (playerY == moleY - 1) {
                    movementValid = false;
                }
                //uses the setPosition() method of mole with the updated X and Y values
                if ((!(moleY - 1 < 0)) && movementValid) {
                    Tile currentTile = level[moleX][moleY - 1];
                    if (currentTile.getType() == TileType.EMPTY) {
                        m.setPosition(moleX, moleY - 1);
                    } else {
                        int durability = currentTile.getMaxDurability();
                        currentTile.mine(60);
                        m.changeFullness(durability);
                    }
                } else {
                    this.moveMole(m);
                }
                break; //makes sure the mole doesn't move multiple directions so breaks it
            case 2: //The case is 2 which means the mole will be moving down
                movementValid = true;
                for (Mole mole : moles) {
                    if (mole != null) {
                        thisMoleY = mole.getY();
                        if (thisMoleY == moleY + 1) {
                            movementValid = false;
                        }
                    }
                }
                if (playerY == moleY + 1) {
                    movementValid = false;
                }
                //uses the setPosition() method of mole with the updated X and Y values
                if ((!(moleY + 1 > levelHeight - 1)) && movementValid) {
                    Tile currentTile = level[moleX][moleY + 1];
                    if (currentTile.getType() == TileType.EMPTY) {
                        m.setPosition(moleX, moleY + 1);
                    } else {
                        int durability = currentTile.getMaxDurability();
                        currentTile.mine(60);
                        m.changeFullness(durability);
                    }
                } else {
                    this.moveMole(m);
                }
                break; //makes sure the mole doesn't move multiple directions so breaks it
            case 3: //The case is 3 which means the mole will be moving left
                movementValid = true;
                for (Mole mole : moles) {
                    if (mole != null) {
                        thisMoleX = mole.getX();
                        if (thisMoleX == moleX - 1) {
                            movementValid = false;
                        }
                    }
                }
                if (playerX == moleX - 1) {
                    movementValid = false;
                }
                //uses the setPosition() method of mole with the updated X and Y values
                if ((!(moleX - 1 < 0)) && movementValid) {
                    Tile currentTile = level[moleX - 1][moleY];
                    if (currentTile.getType() == TileType.EMPTY) {
                        m.setPosition(moleX - 1, moleY);
                    } else {
                        int durability = currentTile.getMaxDurability();
                        currentTile.mine(60);
                        m.changeFullness(durability);
                    }
                } else {
                    this.moveMole(m);
                }
                break; //makes sure the mole doesn't move multiple directions so breaks it
            case 4: //The case is E which means the mole will be moving right
                movementValid = true;
                for (Mole mole : moles) {
                    if (mole != null) {
                        thisMoleX = mole.getX();
                        if (thisMoleX == moleX + 1) {
                            movementValid = false;
                        }
                    }
                }
                if (playerX == moleX + 1) {
                    movementValid = false;
                }
                //uses the setPosition() method of player with the updated X and Y values
                if ((!(moleX + 1 > levelWidth - 1)) && movementValid) {
                    Tile currentTile = level[moleX + 1][moleY];
                    if (currentTile.getType() == TileType.EMPTY) {
                        m.setPosition(moleX + 1, moleY);
                    } else {
                        int durability = currentTile.getMaxDurability();
                        currentTile.mine(60);
                        m.changeFullness(durability);
                    }
                } else {
                    this.moveMole(m);
                }
        }
        int moleFullness = m.getFullness();
        if (moleFullness >= m.getMaxFullness()) {
            explode(m);
        }
    }

    /**
     * This method is used to make a tile "explode" when it is traversed by a
     * player (only for SILVER tiles). This method uses a nested for loop to
     * scan through the 9 tiles in a 3x3 block around the player and mine those
     * tiles making it look as if they exploded.
     *
     *
     * @param playerX the x co-ordinate of the player
     * @param playerY the y co-ordinate of the player
     * @param mineEnergy the energy that the player uses to mine the original
     * tile
     */
    private void explode(int playerX, int playerY, int mineEnergy) {
        for (int i = playerX - 1; i < playerX + 2; i++) {
            for (int j = playerY - 1; j < playerY + 2; j++) {
                if ((i > 0) && (j > 0)) {
                    if ((i < levelWidth) && (j < levelHeight)) {
                        level[i][j].mine(mineEnergy);
                    }
                }
            }
        }
    }

    /**
     * This method is used to make a mole "explode" when its fullness value
     * reaches or exceeds its maximum fullness. This method should store the
     * mole's X and Y co-ordinates and then "mine" the tiles around this
     * position out to a fixed radius.
     *
     * @param m the mole that is exploding
     */
    private void explode(Mole m) {
        int moleX = m.getX(); //gets the mole X and Y coords
        int moleY = m.getY();
        //uses a random generator to set the explosion length and width (max 4)
        int explosionLength = rng.nextInt(1, 5);
        int explosionWidth = rng.nextInt(1, 5);
        //uses a nested loop to 'mine' all of that tiles that have exploded
        for (int i = moleX - explosionWidth; i < moleX + explosionWidth; i++) {
            for (int j = moleY - explosionLength; j < moleY + explosionLength; j++) {
                if ((i > 0) && (j > 0)) {
                    if ((i < levelWidth) && (j < levelHeight)) {
                        Tile currentTile = level[i][j];
                        currentTile.mine(60);
                    }

                }

            }

        }

    }

    /**
     * This method should iterate over the moles array, checking each Mole
     * object to see if its current fullness os greater than or equal to its
     * maximum fullness (i.e. it "exploded" this turn). If it has, it should be
     * set to null in the moles array. You will need to check if the array
     * element currently being examined is null, before you attempt to call any
     * methods on the array element.
     */
    private void clearExplodedMoles() {
        for (int i = 0; i < moles.length; i++) {
            if (moles[i] != null) {
                int moleFullness = moles[i].getFullness();
                if (moleFullness >= moles[i].getMaxFullness()) {
                    moles[i] = null;
                }
            }
        }
    }

    /**
     * This method is called when the player "mines" all ore tiles (i.e. COPPER,
     * SILVER and URANIUM tiles, and returns to the BASE "completing" the level.
     *
     * This method should increase the current level number, create a new level
     * by calling the generateLevel method and setting the level attribute using
     * the returned 2D array, add new Moles, and finally place the player in the
     * new level.
     *
     */
    private void nextLevel() {
        levelNumber++;
        generateLevel();
        addMoles();
        placePlayer();
        gui.updateDisplay(level, player, moles);
    }

    /**
     * The first version of this method should place the player in the game
     * level by setting new, fixed X and Y values for the player object in this
     * class.
     *
     * The second version of this method in a later task should place the player
     * in a game level by choosing a position corresponding to a BASE tile.
     */
    private void placePlayer() {
        player.setPosition(10, 5);
    }

    /**
     * Checks if all "ore tiles" (copper, silver and uranium) have been mined in
     * the level, i.e. if no ore tiles remain in the level array in this class.
     * This method should iterate over the entire 2D level array and if an ore
     * tile is found it should return true. If all elements in the level array
     * have been searched and no ore tiles were found then it should return
     * false.
     *
     * @return true if no ore tiles exist in the level, false otherwise.
     */
    private boolean allOreMined() {
        int oreCount = 0;
        for (int i = 0; i < level.length; i++) {
            for (int j = 0; j < level[i].length; j++) {
                Tile currentTile = level[i][j];
                if (null != currentTile.getType()) {
                    switch (currentTile.getType()) {
                        case COPPER:
                            oreCount++;
                            break;
                        case SILVER:
                            oreCount++;
                            break;
                        case URANIUM:
                            oreCount++;
                    }
                }

            }

        }
        if (oreCount > 0) {
            return false;
        } else {
            return true;
        }
    }

    /**
     * Performs a single turn of the game when the user presses a key on the
     * keyboard. The method clears exploded moles, periodically moves any moles
     * in the level, and increments the turn number. Finally it requests the GUI
     * to redraw the game level by passing it the level, player and moles
     * objects for the current level.
     *
     */
    public void doTurn() {
        turnNumber++;
        if (turnNumber % 4 == 0) {
            moveAllMoles();
        }
        clearExplodedMoles();
        player.changeEnergy(+2);
        boolean minedAllOre = allOreMined();
        int playerX = player.getX();
        int playerY = player.getY();
        Tile playerTile = level[playerX][playerY];
        if ((minedAllOre) && (playerTile.getType() == TileType.BASE)) {
            nextLevel();
        }
        System.out.println("Score: "+score);
        gui.updateDisplay(level, player, moles);
    }

    /**
     * Starts a game. This method generates a level, adds moles and the player
     * and then requests the GUI to update the level on screen using the
     * information on level, player and moles.
     * 
     * @param difficulty the difficulty of the game as selected by the user 
     * on the start screen
     */
    public void startGame(String difficulty) {
        gameDifficulty = difficulty;
        generateLevel();
        addMoles();
        createPlayer();
        gui.updateDisplay(level, player, moles);
    }
}
