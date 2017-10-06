/**
 * An example demonstrating the level1 IQFeed communications at localhost:5009.
 *
 */

//JAVA imports needed.
import java.net.*;
import java.io.*;
import common.*;

/**
 * An example program for reading retrieving streaming level 1data.
 * 
 * Here are a few basic commands you can enter.
 * 
 * To watch a symbol type 'w' followed by the symbol and then press enter which is a <LF>.
 * This is an IQFeed level1 socket command.
 * 
 * An example:
 * 
 * wMSFT<LF>
 * wCAT<LF>
 * wIBM<LF>
 * 
 * To stop watching type 'r' followed by the symbol name and then press enter which is a <LF>.
 * 
 * An example:
 *  
 * rMSFT<LF>
 * rCAT<LF>
 * rIBM<LF>
 * 
 * To quit the application enter an 'x' followed by pressing enter which is a <LF>
 * The 'x' command described is specific to this JAVA application is not an IQFeed level1 socket command. 
 * 
 * An example:
 * 
 * x<LF>
 * 
 * See the links below to see all the level1 commands you can enter.
 *   
 * @see http://www.iqfeed.net/dev/api/docs/Level1viaTCPIP.cfm
 * @see http://www.iqfeed.net/dev/api/docs/Level1SystemMessages.cfm
 * @see http://www.iqfeed.net/dev/api/docs/DynamicFieldsets.cfm
 * @see http://www.iqfeed.net/dev/api/docs/NewsLookupviaTCPIP.cfm
 * @see http://www.iqfeed.net/dev/api/docs/RegionalMessageFormat.cfm
 * 
 * See these links and the ones above to understand the data formats used.
 * 
 * @see http://www.iqfeed.net/dev/api/docs/FundamentalMessageFormat.cfm
 * @see http://www.iqfeed.net/dev/api/docs/Level1UpdateSummaryMessage.cfm
 * @see http://www.iqfeed.net/dev/api/docs/TimeMessageFormat.cfm
 * 
 * 
 * @author Brian.Wood
 * 
*/
public class streamer
{
	BufferedReader in, sin;
	BufferedWriter sout;
	boolean exitFlag = false;

	/**
	A thread to receive and write out to the console the output from IQFeed
	*/
	class stream_thread extends Thread
	{
		public void run()
		{
			String line;
			try
			{
				while ((line = sin.readLine()) != null)
				{
					System.out.println(line);
				}
			}
			catch (IOException e) { }
		}
	}

	/**
 	 * Main run function of the application.  This applications launches the feed
	 * and then connects to IQConnect to retrieve market data.
	 * IQConnect.exe is the proxy between IQFeed clients and the IQFeed back end servers.
	 * 
	 * This application displays level1 streaming data.  The application displays the initial
	 * level1 messages and then waits for level1 socket commands.
	 *  
	*/
	void run()
	{
                Java_Config config = new Java_Config();
		// Start IQConnect & IQFeed	
		try
		{
		System.out.println("Launching IQConnect.");
                Runtime.getRuntime().exec(String.format("iqconnect.exe -product %s -version 1.0",config.product_id));
		System.out.println("Verifying if IQConnect is connected to the server");
		// verify everything is ready to send commands.
		boolean bConnected = false;
		// connect to the admin port.
		Socket sockAdmin = new Socket(InetAddress.getByName("localhost"), 9300);
		BufferedReader bufreadAdmin = new BufferedReader(new InputStreamReader(sockAdmin.getInputStream()));
		BufferedWriter bufwriteAdmin = new BufferedWriter(new OutputStreamWriter(sockAdmin.getOutputStream()));
		String strAdminLine = "";
		// loop while we are still connected to the admin port or until we are connected
		while (((strAdminLine = bufreadAdmin.readLine()) != null) && !bConnected)
		{
			System.out.println(strAdminLine);
			if (strAdminLine.indexOf(",Connected,") > -1)
			{
				System.out.println("IQConnect is connected to the server.");
				bConnected = true;
			}
			else if (strAdminLine.indexOf(",Not Connected,") > -1)
			{
				System.out.println("IQConnect is Not Connected.\r\nSending connect command.");
				bufwriteAdmin.write("S,CONNECT\r\n");
				bufwriteAdmin.flush();
			}
		}
		// cleanup admin port connection
		sockAdmin.shutdownOutput();
		sockAdmin.shutdownInput();
		sockAdmin.close();
		bufreadAdmin.close();
		bufwriteAdmin.close();

		// at this point, we are connected and the feed is ready.
		System.out.println("Connecting to Level 1 port.");

		// String to hold what the user typed in.			
		String line;

		// creates a socket connection to localhost (IP address 127.0.0.1) on port 5009.
		// This is that port that IQFeed listens on for level1 requests. 
		Socket s = new Socket(InetAddress.getByName("localhost"), 5009);

		// create a buffer to read in socket data.
		sin = new BufferedReader(new InputStreamReader(s.getInputStream()));
		// create a buffer in which to send commands to IQFeed on. 
		sout = new BufferedWriter(new OutputStreamWriter(s.getOutputStream()));

		// start a thread to receive socket data. 
		stream_thread thread = new stream_thread();
		thread.start();
		// send the command to set the IQFeed protocol
		sout.write(String.format("S,SET PROTOCOL,%s\r\n",config.most_recent_protocol));
		sout.flush();

		// create buffer to read in commands from the user.
		in = new BufferedReader(new InputStreamReader(System.in));
		boolean loop = true;
		while (loop)
		{
			// read in commands the user enters.
			line = in.readLine();
                            
			sout.write(line + "\r\n");
			sout.flush();
                            
			// if we detect the exit command abort.
			if (line.trim().equals("x"))
			{

				sout.write("S,UNWATCH ALL\r\n");
				sout.flush();
				loop = false;
				s.shutdownOutput();
				s.shutdownInput();
				s.close();
				break;
			}
		}

		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		System.out.println("Exiting application!\n");
	}

	/**
	 * JAVA application's main run method.  It creates the streamer application
	 * and then calls the run method which displays the level1 connect messages
	 * then waits for input by the user. 
	 * 
	 * @param args
	 */
	public static void main(String args[])
	{
		// creates an instant of the streamer application.		
		streamer me = new streamer();
		// executes the run function.
		me.run();
	}
}
