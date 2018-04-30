/*
 * Created on Feb 6, 2005
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.wolfram.numberfeed;

import com.wolfram.deviceinterface.DeviceInterface;

/**
 * @author twj
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class NumberFeed extends DeviceInterface
{
    int counter = 0;
    boolean increment = true;
    int upperLimit = 25;
    int lowerLimit = 0;
    

/*
 * These could be synchronized in some way.
 */
    
    public void setUpper( int val)
    {
        upperLimit = val;
    }
    
    public void setLower( int val)
    {
        lowerLimit = val;
    }
    
    /*
     * This gets called on a collection thread that waits for input, 
     * when input is ready it returns the object.
     * 
     * While this method is running the system cannot be halted or 
     * terminated, so this should not wait for ever, but periodically 
     * it should return null to allow things to be shutdown.
     */
    
	public Object getResult()
    {
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            return null;
        }
        if ( counter >= upperLimit)
            increment = false;
        if ( counter <= lowerLimit)
            increment = true;
        if ( increment)
            counter++;
        else
            counter--;
        return new Integer(counter);
    }        

 }
