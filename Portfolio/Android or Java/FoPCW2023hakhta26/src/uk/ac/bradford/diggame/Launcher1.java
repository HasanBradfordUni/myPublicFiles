package uk.ac.bradford.diggame;

import java.awt.EventQueue;

/**
 * This class is the entry point for the project, containing the main method
 * that starts a game. It creates instances of the different classes of this
 * project and connects them appropriately.
 *
 * @author hakhta26 (original by prtrund1)
 */
public class Launcher1 {

    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {

            /**
             * The run method starts the game in a separate thread. It creates
             * the GUI, the engine and the input handler classes and connects
             * those that call other objects.
             */
            @Override
            public void run() {
                StartScreenGUI gui = new StartScreenGUI();            //create GUI
                gui.setVisible(true);                 //display GUI
                gui.registerMouseHandler();
            }
        });
    }

}
