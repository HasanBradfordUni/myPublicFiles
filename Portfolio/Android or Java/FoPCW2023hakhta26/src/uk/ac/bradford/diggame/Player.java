package uk.ac.bradford.diggame;

/**
 * The Player class is a subclass of Entity and adds specific state and
 * behaviour for the player in the game including energy, the ability to reset
 * this energy value back to full and to retrieve the current energy value.
 *
 * @author prtrundl
 */
public class Player extends Entity {

    /**
     * maxStamina stores the maximum possible energy for this player
     */
    private final int maxEnergy;

    /**
     * stamina stores the current energy for this player
     */
    private int energy;

    

    /**
     * This constructor is used to create a Player object to use in the game
     *
     * @param maxEnergy the maximum energy of this Player, also used to set
     * its starting energy value
     * @param x the starting X position of this Player in the game
     * @param y the starting Y position of this Player in the game
     */
    public Player(int maxEnergy, int x, int y) {
        this.maxEnergy = maxEnergy;
        this.energy = maxEnergy;
        setPosition(x, y);
    }

    /**
     * Changes the current energy value for this Player, setting it to the
     * value of maxEnergy.
     */
    public void refillEnergy() {
        energy = maxEnergy;
    }
    
    /**
     * Changes the energy value for the player. Negative values passed to this
     * method will reduce the player energy and positive values will increase
     * it. If the new value for player energy is larger than the maximum
     * then the value is set to the maximum.
     * @param amount the change in energy required
     */
    public void changeEnergy(int amount) {
        energy += amount;
        if (energy > maxEnergy) {
            energy = maxEnergy;
        }
        if (energy < 0) {
            energy = 0;
        }
    }

    /**
     * Returns the current energy value for the player
     *
     * @return the value of the energy attribute for the player
     */
    public int getEnergy() {
        return energy;
    }

    /**
     * Returns the maxEnergy value for the player
     *
     * @return the value of the maxEnergy attribute for this Player
     */
    public int getMaxEnergy() {
        return maxEnergy;
    }
}
