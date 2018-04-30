/*
 * Created on Feb 7, 2005
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.wolfram.deviceinterface;


/**
 * @author twj
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
class DeviceInterfaceThread extends Thread
{
    int pause;
    boolean running = false;
    boolean terminated = false;
    DeviceInterface controller;
    
    int counter;
    
    DeviceInterfaceThread( DeviceInterface controller_)
    {
        controller = controller_;
        counter = 0;
    }
 
    synchronized void setTerminated( boolean terminated_)
    {
        terminated = terminated_;
    }

    synchronized void setRunning( boolean running_)
    {
        running = running_;
    }

    void checkRunning() throws DeviceInterfaceException
    {
        try {
            synchronized (this) {
                while( true) {
                    if ( running)
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
                checkRunning();
                Object result = controller.getResult();
                if ( result != null) {
                    checkRunning();
                    controller.addResult( result);
                }
            }
        } catch (DeviceInterfaceException e) {
            return;
        }
	}
    
    
}
