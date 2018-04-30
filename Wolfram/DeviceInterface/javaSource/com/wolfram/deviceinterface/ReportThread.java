/*
 * Created on Feb 6, 2005
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.wolfram.deviceinterface;

import java.util.Vector;

/**
 * @author twj
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
class ReportThread extends Thread
{
    DeviceInterface controller;
    Vector listeners;
    boolean resultReady = false;
    boolean terminated = false;
    Vector result;
    
    
    ReportThread( DeviceInterface controller_)
    {
        controller = controller_;
        listeners = new Vector();
        result = new Vector();
    }

    synchronized void addResult( Object result_)
    {
        result.add( result_);
        resultReady = true;
    }
    
    synchronized Object[] getResults()
    {
        Object[] resultArray = result.toArray();
        result = new Vector();
        resultReady = false;
        return resultArray;
    }
    
 
    synchronized void addListener( String name)
    {
        if ( listeners.contains( name))
            return;
        listeners.add( name);
    }
    
    synchronized void removeListener( String name)
    {
        listeners.remove( name);
    }
    
    synchronized String[] getListeners( )
    {
        return (String[])listeners.toArray( new String[] {});
    }
    
    
    synchronized void setTerminated( boolean terminated_)
    {
        terminated = terminated_;
    }
    
    synchronized boolean getTerminated()
    {
        return terminated;
    }
    
    synchronized void setResultReady( boolean resultReady_)
    {
        resultReady = resultReady_;
    }
    
    void waitForResult()
    	throws DeviceInterfaceException
    {
        try {
            synchronized( this) {
                while( true) {
                    if ( resultReady)
                        return;
                    if ( terminated)
                        throw new DeviceInterfaceException();
                    this.wait(100);
                }
            }
        } catch (InterruptedException e) {
            throw new DeviceInterfaceException();
        }
    }
       
     
	public void run()
	{
	    try {
            while( true) {
                waitForResult();
                controller.processEvent( getListeners());
            }
        } catch (DeviceInterfaceException e) {
            return;
        }
	    
	}
    

}
