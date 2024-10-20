
package uk.ac.bradford.diggame;

/**
 * A class to create Tile object used in the game. A Tile represents one single
 * tile in the game. Tiles has a type, defining their appearance and their
 * durability - an attribute used to track mining progress towards mining the
 * tile to destruction.
 * 
 * @author prtrundl
 */
public class Tile {
    
    /**
     * The current durability value for this Tile object. When this value reaches 
     * zero the Tile has been mined (destroyed).
     */
    private int durability;
    
    /**
     * The maximum durability value for this Tile. Can be used to determine how
     * much current durability has been reduced from the maximum, for example.
     */
    private int maxDurability;
    
    /**
     * A type for this Tile object. The type affects what is drawn to the screen
     * and maximum/starting durability values. The type must use one of the
     * values from the TileType enumeration (enum).
     */
    private TileType type;
    
    /**
     * An enumeration to restrict the type of Tile objects to one of a set
     * of fixed values. Each type has an associated graphic for drawing to the
     * screen and fixed durability values, which are set when the Tile 
     * constructor is called.
     */
    public enum TileType {
        EMPTY, DIRT, HARD_DIRT, ROCK, COPPER, SILVER, URANIUM, BASE;
    }
    
    /**
     * A constructor to create Tile objects. Sets the type for this Tile object
     * which dictates the durability for this Tile object. Note that EMPTY 
     * and BASE type Tile objects have 0 durability as they cannot be mined.
     * @param t 
     */
    public Tile(TileType t) {
        this.type = t;
        switch (t) {
            case EMPTY: this.maxDurability = 0; break;
            case DIRT: this.maxDurability = 10; break;
            case HARD_DIRT: this.maxDurability = 20; break;
            case ROCK: this.maxDurability = 40; break;
            case COPPER: this.maxDurability = 30; break;
            case SILVER: this.maxDurability = 40; break;
            case URANIUM: this.maxDurability = 60; break;
            case BASE: this.maxDurability = 0; break;
        }
        this.durability = this.maxDurability;    //always set durability to max
    }
    
    /**
     * Get the current durability of this Tile object.
     * @return the current value of the durability attribute for this Tile object
     */
    public int getDurability() {
        return this.durability;
    }

    /**
     * Get the maximum durability of this Tile object.
     * @return the value of maxDurability for this Tile object
     */
    public int getMaxDurability() {
        return this.maxDurability;
    }
    
    /**
     * Get the type for this Tile object. The value will be one of those
     * defined in the TileType enumeration in the Tile class.
     * @return 
     */
    public TileType getType() {
        return this.type;
    }
    
    /**
     * Mine a tile by calling this method on it. The method reduces the
     * durability value of the Tile object by the amount that is passed to this
     * method. If the durability value is reduced to 0 or less the Tile
     * object is changed  to an EMPTY Tile, durability and maxDurability are
     * both set to 0 and the type of Tile before it was mined is returned
     * (allowing for this information to be used in the GameEngine class). If
     * the durability was not reduced to zero or less then no further changes
     * are made and the method returns null.
     * 
     * @param strength the amount of durability to reduce for the Tile
     * 
     * @return null if this Tile was not destroyed, or the type of the Tile in
     * the form of a TileType if it was destroyed.
     */
    public TileType mine(int strength) {
        durability -= strength;
        if (durability <= 0) {
            TileType previousType = type;
            durability = 0;
            maxDurability = 0;
            this.type = TileType.EMPTY;
            return previousType;
        }
        return null;
    }
    
}
