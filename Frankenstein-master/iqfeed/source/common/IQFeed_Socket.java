//-----------------------------------------------------------
//-----------------------------------------------------------
//
//             System: IQFeed
//       Program Name: Generic Socket Class
//        Module Name: IQFeed_Socket.java
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
// Module Description: Generic Socket Class w/Buffered Reader and Writer
//         References: None
//           Compiler: Netbeans 7.4, Java 1.7045
//             Author: Tim Walter
//        Modified By: 
//
//-----------------------------------------------------------
//-----------------------------------------------------------
//-----------------------------------------------------------
// Website for Level1 information: http://www.iqfeed.net/dev/api/docs/Level1viaTCPIP.cfm
//-----------------------------------------------------------
/******************************************************************************
 * DISCLAIMER:  These apps are designed with simplicity in mind and are not 
 * designed for copy and paste development.  You will need to consider 
 * performance enhancements based upon your own needs and implement your
 * solution accordingly. They are a guide to get people started, nothing more.
 ******************************************************************************/

import java.io.*;
import java.net.*;


public class IQFeed_Socket extends Socket
{
	BufferedReader brBufferedReader;
	BufferedWriter brBufferedWriter;
	//-----------------------------------------------------------
	// public IQFeed_Socket() 
	/**
	*/
	//  Notes:  Default Constructor using parent Socket class
	//
	//-----------------------------------------------------------	
	public IQFeed_Socket() 
	{
		super();
	}
	//-----------------------------------------------------------
	// protected void ConnectSocket(int iPort)
	/**
	*/
	// @params iPort - integer representing a socket port to connect to.
	// @return If connect goes through without error, return true, false if there is any other issue.
	//  Notes:  Connects a socket to the localhost on the port sent
	//	Dafault values are located in the registry settings documentation on the API site.
	//
	//-----------------------------------------------------------
	protected boolean ConnectSocket(int iPort)
	{
		try
		{
			this.connect(new InetSocketAddress("localhost", iPort));
		}
		catch(IOException eError)
		{
			System.out.printf("Unable to connect to socket on port, %d.\n",iPort);
			//eError.printStackTrace();
		}
		finally
		{
			return this.isConnected();
		}
	}
	//-----------------------------------------------------------
	// protected void Disconnect()
	/**
	*/
	//  Notes:  Disconnect the socket and close both buffer streams
	//
	//-----------------------------------------------------------	
	protected void Disconnect()
	{
		try
		{
			this.CloseBuffers();
			this.close();
		}
		catch(IOException eError)
		{
			System.out.printf("Unable to disconnect the socket.");
			eError.printStackTrace();
			System.exit(1);
		}
	}
	//-----------------------------------------------------------
	// protected void CreateBuffers()
	/**
	*/
	//  Notes:  Using a class references socket, implement both a buffered reader
	//	and a buffered writer to pass data back and forth between the app and IQConnect.
	//
	//-----------------------------------------------------------	
	protected void CreateBuffers()
	{
		try
		{
			// create a buffer to read in socket data.
			brBufferedReader = new BufferedReader(new InputStreamReader(this.getInputStream()));
			// create a buffer in which to send commands to IQFeed on. 
			brBufferedWriter = new BufferedWriter(new OutputStreamWriter(this.getOutputStream()));	
		}
		catch(IOException eError)
		{
			System.out.printf("Unable to create readers.");
			eError.printStackTrace();
			System.exit(1);
		}
	}
	//-----------------------------------------------------------
	// protected void CloseBuffers()
	/**
	*/
	//  Notes:  Close both the read and write buffer.
	//
	//-----------------------------------------------------------	
	protected void CloseBuffers()
	{
		try
		{		
			brBufferedReader.close();
			brBufferedWriter.close();
		}
		catch(IOException eError)
		{
			System.out.printf("Unable to close readers.");
			eError.printStackTrace();
			System.exit(1);
		}
	}
}
