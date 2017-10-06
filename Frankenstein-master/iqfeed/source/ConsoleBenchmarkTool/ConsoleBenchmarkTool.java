//-----------------------------------------------------------
//-----------------------------------------------------------
//
//             System: IQFeed
//       Program Name: ConsoleBenchmarkTool
//        Module Name: ConsoleBenchmarkTool.java
//
//-----------------------------------------------------------
//
//            Proprietary Software Product
//
//           Data Transmission Network Inc.
//           9110 West Dodge Road Suite 200
//               Omaha, Nebraska  68114
//
//    Copyright (c) by Data Transmission Network 2010
//                 All Rights Reserved
//
//
//-----------------------------------------------------------
// Module Description: Benchmark utility to aid in determining if your bandwidth can handle the incoming load.
//         References: None
//           Compiler: Netbeans 7.4, Java 1.7045
//             Author: Tim Walter
//        Modified By: 
//
//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------
// Website for API information: http://www.iqfeed.net/dev/api/docs/
//-----------------------------------------------------------
/******************************************************************************
 * DISCLAIMER:  These apps are designed with simplicity in mind and are not 
 * designed for copy and paste development.  You will need to consider 
 * performance enhancements based upon your own needs and implement your
 * solution accordingly. They are a guide to get people started, nothing more.
 ******************************************************************************/

//JAVA imports needed.
import common.*;
import java.net.*;

public class ConsoleBenchmarkTool
{
	//Static variables to be used throughout.
	//These can be modified via registry, information is in the documentation.
	static int IQFEED_ADMIN_PORT_DEFAULT = 9300;
	static int IQFEED_LEVEL1_PORT_DEFAULT = 5009;
	
	//This path was for my Netbeans installation, yours may be different.
	String FILENAME = "commands.txt";
	// variables for stats tracking
	int iFMessages = 0;
	int iPMessages = 0;
	int iQMessages = 0;
	int iTMessages = 0;
	int iSMessages = 0;
	int iNMessages = 0;
	int iRMessages = 0;
	int iMsgsLastSecond = 0;
	long l64TotalMsgs = 0;
	long lMsgsLastSecond = 0;
	long lTimeInMilliseconds = 0;
	long l64SecondsStart = 0;
	long l64TotalMsgsPerSecond = 0;
	long l64SecondsNow = 0;
	long lElapsedTime = 0;
    //-----------------------------------------------------------
    // private void ParseLevel1Messages(IQFeed_Socket C_AdminIQFeed_Socket)
    /**
    */
	// @params = A IQFeed_Socket that has a current connection to Level1.
    //  Notes:  Function recieves a Level1 IQFeed_Socket and parses the buffer
	//	for display to the command line, printing message counts and timestamps 
	//	for evaluation.
    //
    //-----------------------------------------------------------	
	private void ParseLevel1Messages(IQFeed_Socket C_AdminIQFeed_Socket)
	{
		l64SecondsStart = System.currentTimeMillis();//Initialize time
		//String to hold the current data from the stream.
		String line;
		try
		{
			while ((line = C_AdminIQFeed_Socket.brBufferedReader.readLine()) != null)
			{
				//Increment counters
				l64TotalMsgs++;
				iMsgsLastSecond++;
				//Based upon the first letter of the line, increment the appropriate update type
				//or if it is T, display the current counters and resets the messages per second values.
				switch (line.charAt(0))
				{

					case 'Q': // Q
						// Update Message
						iQMessages++;
						break;
					case 'T': // T
						// Timestamp Message
						iTMessages++;
						// we trigger our output to the screen when we receive a timestamp message.
						l64SecondsNow = System.currentTimeMillis();
						lElapsedTime = (l64SecondsNow - l64SecondsStart) / 1000;
						if (lElapsedTime > 0)
						{
							// skip the first writeout if a complete second hasn't elapsed to prevent division by zero
							l64TotalMsgsPerSecond = l64TotalMsgs / lElapsedTime;
							System.out.printf("F:%d\tP:%d\tQ:%d\tT:%d\tS:%d\tN:%d\tR:%d\tLM:%d\tTMS:%d\tTIME:%d\n",
									iFMessages, iPMessages, iQMessages, iTMessages, iSMessages, iNMessages, iRMessages, iMsgsLastSecond, l64TotalMsgsPerSecond, l64SecondsNow);
							// reset our "Messages in the last second" counter
							iMsgsLastSecond = 0;
						}
						break;
					case 'F': // F
						// Fundamental Message
						iFMessages++;
						break;
					case 'P': // P
						// Summary Message
						iPMessages++;
						break;
					case 'R': // R
						// Regional Message
						iRMessages++;
						break;
				}
			}
		} 
		catch (Exception eError)
		{
			C_AdminIQFeed_Socket.Disconnect();
			eError.printStackTrace();
		}
	}
    //-----------------------------------------------------------
    // private void m_VerifyTheDataFeedIsConnected(IQFeed_Socket C_AdminIQFeed_Socket)
    /**
    */
	// @params = A IQFeed_Socket that has a current connection to Admin.
    //  Notes:  Function recieves an Admin IQFeed_Socket,then verifies the 
	//	admin has connected prior to returning the execution back to main.
    //
    //-----------------------------------------------------------
	private void m_VerifyTheDataFeedIsConnected(IQFeed_Socket C_AdminIQFeed_Socket)
	{
		boolean bConnected = false;
		String strAdminLine = "";
		//Connect to socket
		C_AdminIQFeed_Socket.ConnectSocket(IQFEED_ADMIN_PORT_DEFAULT);
		//Initialize the buffers
		C_AdminIQFeed_Socket.CreateBuffers();
		System.out.printf("Feed is Connected? %b\n", C_AdminIQFeed_Socket.isConnected());
		//Loop till connected.
		try
		{
			while ((strAdminLine = C_AdminIQFeed_Socket.brBufferedReader.readLine()) != null && !bConnected)
			{
				System.out.println(strAdminLine);
				if (strAdminLine.indexOf(",Connected,") > -1)
				{
					System.out.println("IQConnect is connected to the server.");
					bConnected = true;
				} else if (strAdminLine.indexOf(",Not Connected,") > -1)
				{
					System.out.println("IQConnect is Not Connected.\r\nSending connect command.");
					C_AdminIQFeed_Socket.brBufferedWriter.write("S,CONNECT\r\n");
					C_AdminIQFeed_Socket.brBufferedWriter.flush();
				}
			}
		} 
		catch (IOException eError)
		{
			System.out.printf("Error working with admin socket.");
			eError.printStackTrace();
		}
		//Feed is available, we are done with the admin socket at this point.
		//Disconnecting the admin socket.
		C_AdminIQFeed_Socket.Disconnect();
	}
    //-----------------------------------------------------------
    // private void m_ParseCommandsToLevel1Socket(IQFeed_Socket C_AdminIQFeed_Socket)
    /**
    */
	// @params = A IQFeed_Socket that has a current connection to Level 1.
    //  Notes:  Function recieves a Level1 IQFeed_Socket, it then opens commands.txt
	//	and reads in the contents of that file.  These contents are the commands that you 
	//	want to send to the parser.
    //
    //-----------------------------------------------------------
	private void m_ParseCommandsToLevel1Socket(IQFeed_Socket C_Level1IQFeed_Socket)
	{

			Java_Config config = new Java_Config();
			//This is the folder where the class file is located.
			final File file_path = new File(ConsoleBenchmarkTool.class.getProtectionDomain().getCodeSource().getLocation().getPath());
			FileReader commandsFile;
			String line;
			boolean gotFile = false;
			String PathWithFilename = file_path.toString() + "\\commands.txt";
			//Open the file, FILENAME is defined above.
			//If the file is not found, we ask for it and loop till we get a good path or till the Exit command is entered.
			do  
			{
				try
				{
					if(PathWithFilename.contains("Exit"))
					{
						System.exit(0);
					}
					System.out.println("Opening file: ");
					System.out.println(PathWithFilename);
					commandsFile = new FileReader(PathWithFilename);
					BufferedReader reader = new BufferedReader(commandsFile);
					gotFile = true;
                                        line = "";
                                        C_Level1IQFeed_Socket.brBufferedWriter.write("S,SET PROTOCOL,"+ config.most_recent_protocol + "\r\n");
                                        C_Level1IQFeed_Socket.brBufferedWriter.flush();
					//Now that we have a good filr, read in each line and flushing each so all commands get processed before moving on.
					while ((line = reader.readLine()) != null)
					{
						System.out.printf(line + "\n");
						C_Level1IQFeed_Socket.brBufferedWriter.write(line.trim() + "\r\n");
						C_Level1IQFeed_Socket.brBufferedWriter.flush();
					}
				}
				catch (IOException eError)
				{
					//This handles if the default file cannot be found by asking for and receiving the user input.
					System.out.printf("Open failed: Enter the full path to the file %s\n", FILENAME);
					System.out.printf("Example : C:\\Temp\\commands.txt or Exit to leave the application.\n");
					
					InputStreamReader converter = new InputStreamReader(System.in);
					BufferedReader in = new BufferedReader(converter);
					try
					{
						PathWithFilename = in.readLine();
					}
					catch (IOException eError2)
					{
						eError2.printStackTrace();
						System.exit(1);
					}
				}
			} while (gotFile == false);
	}
    //-----------------------------------------------------------
    // public static void main(String args[])
    /**
    */
	// @params = No arguments are expected from the command line.
    //  Notes:  Main app, get the sockets, create the readers, handle the data.
    //
    //-----------------------------------------------------------	
	public static void main(String args[])
	{
            
                Java_Config config = new Java_Config();
		ConsoleBenchmarkTool CConsoleBenchmarkTool = new ConsoleBenchmarkTool();
		IQFeed_Socket C_AdminIQFeed_Socket = new IQFeed_Socket();
		IQFeed_Socket C_Level1IQFeed_Socket = new IQFeed_Socket();
                
		//Launch the datafeed
		System.out.printf("Launching IQConnect.\n");
		
		try
		{
			Runtime.getRuntime().exec(String.format("iqconnect.exe -product %s -version 1.0.\n",config.product_id));
		} 
		catch (IOException eError)
		{
			eError.printStackTrace();
		}

		System.out.printf("Verifying IQConnect is connected to the server.\n");

		CConsoleBenchmarkTool.m_VerifyTheDataFeedIsConnected(C_AdminIQFeed_Socket);

		//Now that the admin is done, begin the level1 processing.
		C_Level1IQFeed_Socket.ConnectSocket(IQFEED_LEVEL1_PORT_DEFAULT);
		//Create the read and write socket buffers.
		C_Level1IQFeed_Socket.CreateBuffers();
		//Send the contents of the commands file to the client.
		CConsoleBenchmarkTool.m_ParseCommandsToLevel1Socket(C_Level1IQFeed_Socket);
		//Parse the returning messages.
		CConsoleBenchmarkTool.ParseLevel1Messages(C_Level1IQFeed_Socket);
	}

}
