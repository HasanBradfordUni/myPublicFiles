package uk.ac.bradford.diggame;

/** The Mole class is a subclass of Entity and adds specific state and
 * behaviour for the moles in the game, including fullness and the ability
 * to change fullness values.
 *
 * @author prtrundl
 */
public class Mole extends Entity {
    
    /**
     * maxFullness stores the maximum possible fullness for this Mole
     */
    private final int maxFullness;
    
    /**
     * fullness stores the current fullness for this Mole. When this value
     * exceeds maxFullness the mole should explode.
     */
    private int fullness;
    
    /**
     * This constructor is used to create a Mole object to use in the game,
     * and sets the maximum fullness value for this mole.
     * @param maxFullness the maximum fullness of this Mole, also used to set its starting
     * fullness value
     * @param x the starting X position of this Mole in the level
     * @param y the starting Y position of this Mole in the level
     */
    public Mole(int maxFullness, int x, int y) {
        this.maxFullness = maxFullness;
        this.fullness = 0;
        setPosition(x, y);
    }
    
    /**
     * Changes the fullness value for this mole. Positive values passed to this
     * method will increase the fullness, and negative values will decrease it.
     * @param amount the change required for the fullness value
     */
    public void changeFullness(int amount) {
        fullness += amount;
    }
        
    /**
     * Returns the current fullness value for this Mole
     * @return the value of the fullness attribute for this Mole
     */
    public int getFullness() {
        return fullness;
    }
    
    /**
     * Returns the maxFullness value for this Mole
     * @return the value of the maxFullness attribute for this Mole
     */
    public int getMaxFullness() {
        return maxFullness;
    }
}
