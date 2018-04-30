/*
 * Created on Feb 6, 2005
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.wolfram.deviceinterface;

import com.wolfram.jlink.KernelLink;
import com.wolfram.jlink.KernelLinkImpl;
import com.wolfram.jlink.MathLink;
import com.wolfram.jlink.MathLinkException;
import com.wolfram.jlink.StdLink;

/**
 * @author twj
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public abstract class DeviceInterface
{
	ReportThread reportThread;
    DeviceInterfaceThread interfaceThread;
    boolean initialized = false;
   

    protected DeviceInterface()
	{
        reportThread = new ReportThread( this);
        interfaceThread = new DeviceInterfaceThread( this);

    }

   public void initializeDevice()
   {
       KernelLink mainLink = StdLink.getLink();
       KernelLink uiLink = StdLink.getUILink();
       
		((KernelLinkImpl) uiLink)
		.setObjectHandler(((KernelLinkImpl) mainLink)
				.getObjectHandler());
		reportThread.start();
		interfaceThread.start();
		initialized = true;
   }
   
   public void startDevice()
   {
       if ( !initialized)
           initializeDevice();
       interfaceThread.setRunning( true);
   }
   
   public void stopDevice()
   {
       interfaceThread.setRunning( false);
   }

   public void terminateDevice()
   {
       synchronized( reportThread) {
           reportThread.setTerminated( true);
           reportThread.notify();
       }    
       interfaceThread.setTerminated( true);
   }
      
   
   public void addListener( String fun)
   {
       reportThread.addListener( fun);
   }
   
   
   public void removeListener( String fun)
   {
       reportThread.removeListener( fun);
   }
   
   public String[] getListeners(  )
   {
       return reportThread.getListeners( );
   }
   
   void writeObjectToFunction( String func, Object[] objs)
   {
       KernelLink link = StdLink.getLink();
       synchronized ( link) {
        try {
           for ( int i = 0; i < objs.length; i++) {
               
               link.putFunction("EvaluatePacket", 1);
               link.putNext( MathLink.MLTKFUNC);
               link.putArgCount(1);  
               link.putNext( MathLink.MLTKFUNC);
               link.putArgCount(1);  
               link.putSymbol("ToExpression");
               link.put(func);
               link.putReference(objs[i]);
               link.endPacket();
               link.discardAnswer();
           }
       } catch (MathLinkException e) {
           e.printStackTrace();
       }
       }
   }
   
   void processEvent( String[] listeners)
   {
       Object[] objs = reportThread.getResults();
       for ( int i = 0; i < listeners.length; i++) {
           writeObjectToFunction( listeners[i], objs);
       }
   }
   
   void addResult( Object result)
   {
       reportThread.addResult( result);
   }
   
   
   public abstract Object getResult( );
   
}
