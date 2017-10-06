/**
 * An example demonstrating the lookup communications at localhost:9100.
 *
 */

// JAVA imports needed.
import java.net.*;
import java.io.*;

/**
 * Class which demonstrates IQFeed Lookup Requests.
 * 
 * For more information on the lookup commands, see the links below.
 * 
 * @see http://www.iqfeed.net/dev/api/docs/HistoricalviaTCPIP.cfm
 * @see http://www.iqfeed.net/dev/api/docs/OptionChainsviaTCPIP.cfm
 * @see http://www.iqfeed.net/dev/api/docs/SymbolLookupviaTCPIP.cfm
 * @see http://www.iqfeed.net/dev/api/docs/NewsLookupviaTCPIP.cfm
 * 
 * 
 * @author Brian.Wood
 * 
 */

public class LookupClient
{
	///////////////
	// Variables //
	///////////////
	
	/**
	 *	BufferedReaders for reading data from System.in and from the socket
	*/
	BufferedReader	in, sin;
	/**
	 * 	BufferedWriter for writing to the socket
	*/
	BufferedWriter	sout;

	///////////////
	// Functions //
	///////////////
	
	/**
	 * 	Retrieves the news configuration data.
	 * 
	 * @throws Exception
	*/
	void GetNewsConfig() throws Exception
	{
		// get input from user for parameters
		String sTextXML, sRequestID;
		System.out.print("Return data in XML or text ('x'=XML 't'=text default='x'): ");
		sTextXML = in.readLine();
		System.out.print("RequestID: ");
		sRequestID = in.readLine();
		// send request to the feed
		sout.write("NCG," + sTextXML + "," + sRequestID + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{		
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves number of news stories for a group of symbols.
	 * 
	 * @throws Exception
	*/
	void GetNewsStoryCounts() throws Exception
	{
		// get input from user for parameters
		String sSymbols, sSources, sDateRange, sTextXML, sRequestID;
		System.out.print("Symbols (SYMBOL1:SYMBOL2: ... :SYMBOLN): ");
		sSymbols = in.readLine();
		System.out.print("News Sources(s) (SOURCE1:SOURCE2: ... :SOURCEN): ");
		sSources = in.readLine();
		System.out.print("Date/Date Range (CCYYMMDD or CCYYMMDD-CCYYMMDD): ");
		sDateRange = in.readLine();
		System.out.print("Return data in XML or text ('x'=XML 't'=text default='x'): ");
		sTextXML = in.readLine();
		System.out.print("RequestID: ");
		sRequestID = in.readLine();
		sout.write("NSC," + sSymbols + "," + sTextXML + "," + sSources + "," + sDateRange + "," + sRequestID + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{		
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves news for a headline
	 * 
	 * @throws Exception
	*/
	void GetNewsHeadlinesBySource() throws Exception
	{
		// get input from user for parameters
		String sSources, sLimit, sDate, sTextXML, sRequestID;
		System.out.print("News Sources(s) (SOURCE1:SOURCE2: ... :SOURCEN): ");
		sSources = in.readLine();
		System.out.print("Max Headlines: ");
		sLimit = in.readLine();
		// Note: the date parameter is only valid for the Platts Data news sources.
		System.out.print("From Date (YYYYMMDD): ");
		sDate = in.readLine();
		System.out.print("Return data in XML or text ('x'=XML 't'=text default='x'): ");
		sTextXML = in.readLine();
		System.out.print("RequestID: ");
		sRequestID = in.readLine();
		sout.write("NHL," + sSources + ",," + sTextXML + "," + sLimit + "," + sDate + "," + sRequestID + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves news headlines by symbol(s).
	 * 
	 * @throws Exception
	 */
	void GetNewsHeadlinesBySymbol() throws Exception
	{
		// get input from user for parameters
		String sSources, sLimit, sSymbols, sTextXML, sRequestID;
		System.out.print("Symbols (SYMBOL1:SYMBOL2: ... :SYMBOLN): ");
		sSymbols = in.readLine();
		System.out.print("News Sources(s) (SOURCE1:SOURCE2: ... :SOURCEN): ");
		sSources = in.readLine();
		System.out.print("Max Headlines: ");
		sLimit = in.readLine();
		System.out.print("Return data in XML or text ('x'=XML 't'=text default='x'): ");
		sTextXML = in.readLine();
		System.out.print("RequestID: ");
		sRequestID = in.readLine();
		sout.write("NHL," + sSources + "," + sSymbols + "," + sTextXML + "," + sLimit + "," + sRequestID + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves a story.
	 * 
	 * @throws Exception
	*/
	void GetNewsStory() throws Exception
	{
		// get input from user for parameters
		String	sStoryID, sTextXMLEmail, sDeliverTo = "", sRequestID = "";
		System.out.print("Story ID: ");	
		sStoryID = in.readLine();
		System.out.print("Return data in XML, text, or email ('x'=XML 't'=text 'e'=email default='x'): ");
		sTextXMLEmail = in.readLine();
		if (sTextXMLEmail.equals("e"))
		{
			// if they want it emailed, we need the address
			System.out.print("Email Address: ");
			sDeliverTo = in.readLine();
		}
		else
		{
			// requestID only valid for non-emailed stories.
			System.out.print("RequestID: ");
			sRequestID = in.readLine();
		}
		sout.write("NSY," + sStoryID + "," + sTextXMLEmail + "," + sDeliverTo + "," + sRequestID + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	
	/**
	 * Retrieves symbol list by filter.
	 * 
	 * @throws Exception
	 */
	void GetSymbolsByFilter() throws Exception
	{
		// get input from user for parameters
		String sSearchField, sSearchString, sFilterType, sFilterValue;
		System.out.print("Field ('s'=Symbol 'd'=Description): ");
		sSearchField = in.readLine();
		System.out.print("Search String: ");
		sSearchString = in.readLine();
		System.out.print("Filter Type ('e'=Listed Markets 't'=SecurityType default=none): ");
		sFilterType = in.readLine();
		System.out.print("Filter Value: ");
		sFilterValue = in.readLine();
		
		sout.write("SBF," + sSearchField + "," + sSearchString + "," + sFilterType + "," + sFilterValue + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 		
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	/**
	 * Retrieves symbol list by SIC code
	 * 
	 * @throws Exception
	 */
	void GetSymbolsBySIC() throws Exception
	{
		// get input from user for parameters
		String sSICCodes;
		System.out.print("SIC Codes: ");
		sSICCodes = in.readLine();
		
		sout.write("SBS," + sSICCodes + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 		
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	/**
	 * Retrieves symbol list by NAICS code
	 * 
	 * @throws Exception
	 */
	void GetSymbolsByNAICS() throws Exception
	{
		// get input from user for parameters
		String sNAICSCodes;
		System.out.print("NAICS Codes: ");
		sNAICSCodes = in.readLine();
		
		sout.write("SBN," + sNAICSCodes + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 		
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves a list of futures.
	 * 
	 * @throws Exception
	 */
	void GetFuturesChain() throws Exception
	{
		// get input from user for parameters
		String sSymbol, sMonthCodes, sYears, sNearMonths;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Month Codes: ");
		sMonthCodes = in.readLine();
		System.out.print("Years: ");
		sYears = in.readLine();
		System.out.print("Near Months: ");
		sNearMonths = in.readLine();
		
		sout.write("CFU," + sSymbol + "," + sMonthCodes + "," + sYears + "," + sNearMonths + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 		
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	/**
	 * Retrieves a list of future spreads.
	 * 
	 * @throws Exception
	 */
	void GetFutureSpreadChain() throws Exception
	{
		// get input from user for parameters
		String sSymbol, sMonthCodes, sYears, sNearMonths;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Month Codes: ");
		sMonthCodes = in.readLine();
		System.out.print("Years: ");
		sYears = in.readLine();
		System.out.print("Near Months: ");
		sNearMonths = in.readLine();
		
		sout.write("CFS," + sSymbol + "," + sMonthCodes + "," + sYears + "," + sNearMonths + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 		
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	/**
	 * Retrieves a list of futures options.
	 * 
	 * @throws Exception
	 */
	void GetFutureOptionChain() throws Exception
	{
		// get input from user for parameters
		String sSymbol, sPutsCalls, sMonthCodes, sYears, sNearMonths;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Type ('p'=Puts 'c'=Calls 'pc'=Puts & Calls): ");
		sPutsCalls = in.readLine();
		System.out.print("Months: ");
		sMonthCodes = in.readLine();
		System.out.print("Years: ");
		sYears = in.readLine();
		System.out.print("Near Months: ");
		sNearMonths = in.readLine();
		
		sout.write("CFO," + sSymbol + "," + sPutsCalls + "," + sMonthCodes + "," + sYears + "," + sNearMonths + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 		
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	/**
	 * Retrieves a list of index and equity options.
	 * 
	 * @throws Exception
	 */
	void GetEquityOrIndexOptionChain() throws Exception
	{
		// get input from user for parameters
		String sSymbol, sPutsCalls, sMonthCodes, sNearMonths, sBinaryOptions, sFilterType, sFilterValueOne, sFilterValueTwo;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Type ('p'=Puts 'c'=Calls 'pc'=Puts & Calls): ");
		sPutsCalls = in.readLine();
		System.out.print("Months: ");
		sMonthCodes = in.readLine();
		System.out.print("Near Months: ");
		sNearMonths = in.readLine();
		System.out.print("Exclude Binary Options ('0'=Include '1'=Exclude default='0'): ");
		sBinaryOptions = in.readLine();
		System.out.print("Filter Type: ");
		sFilterType = in.readLine();
		System.out.print("Filter One: ");
		sFilterValueOne = in.readLine();
		System.out.print("Filter Two: ");
		sFilterValueTwo = in.readLine();
		
		sout.write("CEO," + sSymbol + "," + sPutsCalls + "," + sMonthCodes + "," + sNearMonths + "," + sBinaryOptions + "," + sFilterType + "," + sFilterValueOne + "," + sFilterValueTwo + "\r\n");
		sout.flush();
		String sLine = sin.readLine(); 
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1) 
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves history tick data based on the number of data points requested.
	 *   
	 * @throws Exception
	 */
	void GetHistoryTickDatapoints() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sMaxDatapoints, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HTX," + sSymbol + "," + sMaxDatapoints + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves history tick data based on the number of days requested.
	 * 
	 * @throws Exception
	 */
	void GetHistoryTickDays() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sDays, sMaxDatapoints, sBeginFilterTime, sEndFilterTime, sDataDirection, sDatapointsPerSend, sRequestID;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Days: ");
		sDays = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Begin Filter Time: ");
		sBeginFilterTime = in.readLine();
		System.out.print("End Filter Time: ");
		sEndFilterTime = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HTD," + sSymbol + "," + sDays + "," + sMaxDatapoints + "," + sBeginFilterTime + "," + sEndFilterTime + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves history tick data based on the timeframe requested.
	 * 
	 * @throws Exception
	 */
	void GetHistoryTickTimeframe() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sBeginDateTime, sEndDateTime, sMaxDatapoints, sBeginFilterTime, sEndFilterTime, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Begin Date Time (CCYYMMDD HHmmSS): ");
		sBeginDateTime = in.readLine();
		System.out.print("End Date Time (CCYYMMDD HHmmSS): ");
		sEndDateTime = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Begin Filter Time (HHmmSS): ");
		sBeginFilterTime = in.readLine();
		System.out.print("End Filter Time (HHmmSS): ");
		sEndFilterTime = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HTT," + sSymbol + "," + sBeginDateTime + "," + sEndDateTime + "," + sMaxDatapoints + "," + sBeginFilterTime + "," + sEndFilterTime + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves history interval data based on the number of data points requested.
	 * 
	 * @throws Exception
	 */
	void GetHistoryIntervalDatapoints() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sInterval, sMaxDatapoints, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Interval (seconds): ");
		sInterval = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HIX," + sSymbol + "," + sInterval + "," + sMaxDatapoints + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves history interval data based on the number of days requested.
	 * 
	 * @throws Exception
	*/
	void GetHistoryIntervalDays() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sInterval, sDays, sMaxDatapoints, sBeginFilterTime, sEndFilterTime, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Interval (seconds): ");
		sInterval = in.readLine();
		System.out.print("Days: ");
		sDays = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Begin Filter Time (HHmmSS): ");
		sBeginFilterTime = in.readLine();
		System.out.print("End Filter Time (HHmmSS): ");
		sEndFilterTime = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HID," + sSymbol + "," + sInterval + "," + sDays + "," + sMaxDatapoints + "," + sBeginFilterTime + "," + sEndFilterTime + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * Retrieves history interval data based on the timeframe requested.
	 * 
	 * @throws Exception
	 */
	void GetHistoryIntervalTimeframe() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sInterval, sBeginDateTime, sEndDateTime, sBeginFilterTime, sEndFilterTime, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Interval (seconds): ");
		sInterval = in.readLine();
		System.out.print("Begin Date Time (CCYYMMDD HHmmSS): ");
		sBeginDateTime = in.readLine();
		System.out.print("End Date Time (CCYYMMDD HHmmSS): ");
		sEndDateTime = in.readLine();
		System.out.print("Begin Filter Time (HHmmSS): ");
		sBeginFilterTime = in.readLine();
		System.out.print("End Filter Time (HHmmSS): ");
		sEndFilterTime = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HIT," + sSymbol + "," + sInterval + "," + sBeginDateTime + "," + sEndDateTime + ",," + sBeginFilterTime + "," + sEndFilterTime + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves history daily data based on the number of data points requested.
	 * 
	 * @throws Exception
	*/
	void GetHistoryDailyDatapoints() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sMaxDatapoints, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HDX," + sSymbol + "," + sMaxDatapoints + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves history daily data based on the timeframe requested.
	 * 
	 * @throws Exception
	*/
	void GetHistoryDailyTimeframe() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sBeginDate, sEndDate, sMaxDatapoints, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Begin Date Time (CCYYMMDD): ");
		sBeginDate = in.readLine();
		System.out.print("End Date Time (CCYYMMDD): ");
		sEndDate = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HDT," + sSymbol + "," + sBeginDate + "," + sEndDate + "," + sMaxDatapoints + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves history weekly data based on the number of data points requested.
	 * 
	 * @throws Exception
	*/
	void GetHistoryWeeklyDatapoints() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sMaxDatapoints, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HWX," + sSymbol + "," + sMaxDatapoints + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)  
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}

	/**
	 * 	Retrieves history monthly data based on the number of data points requested.
	 * 
	 * @throws Exception
	*/
	void GetHistoryMonthlyDatapoints() throws Exception
	{
		// Documentation for this function can be found in Documentation page titled Historical via TCPIP

		// get input from user for parameters
		String sSymbol, sMaxDatapoints, sDataDirection, sRequestID, sDatapointsPerSend;
		System.out.print("Symbol: ");
		sSymbol = in.readLine();
		System.out.print("Max datapoints: ");
		sMaxDatapoints = in.readLine();
		System.out.print("Data direction ('0'=Newest To Oldest '1'=Oldest To Newest default='0'): ");
		sDataDirection = in.readLine();
		System.out.print("Request ID: ");
		sRequestID = in.readLine();
		System.out.print("Data Points Per Send: ");
		sDatapointsPerSend = in.readLine();
		sout.write("HMX," + sSymbol + "," + sMaxDatapoints + "," + sDataDirection + "," + sRequestID + "," + sDatapointsPerSend + "\r\n");
		sout.flush();
		String sLine = sin.readLine();
		while (sLine != null && sLine.indexOf("!ENDMSG!", 0) == -1)
		{
			System.out.println(sLine);
			if (sLine.equals("E,!SYNTAX_ERROR!,"))
			{
				sLine = null;
			}
			else
			{
				sLine = sin.readLine();
			}
		}
	}
	
	/**
 	 * Main run function of the application.  
	 * This application displays a menu of IQFeed lookup requests that can be demonstrated.
	 * Enter the number listed to run the described demonstration.
	 * 
	 * After each menu selection it should loop back to the menu again.   Enter a Q
	 * to exit the application.
	 * 
	*/
	void run() {
		Java_Config config = new Java_Config();
		try {

			// Launch IQFeed and Register the app with IQFeed.
			System.out.println("Launching IQConnect.");
			Runtime.getRuntime().exec(String.format("iqconnect.exe -product %s -version 1.0",config.product_id));
			System.out.println("Verifying if IQConnect is connected to the server");
			// verify everything is ready to send commands.
			boolean bConnected = false;
			// connect to the admin port.
			Socket sockAdmin = new Socket(InetAddress.getByName("localhost"), 9300);
			BufferedReader bufreadAdmin = new BufferedReader(new InputStreamReader(sockAdmin.getInputStream()));
			BufferedWriter bufwriteAdmin = new BufferedWriter(new OutputStreamWriter(sockAdmin.getOutputStream()));
			String sAdminLine = "";
			// loop while we are still connected to the admin port or until we are connected
			while (((sAdminLine = bufreadAdmin.readLine()) != null) && !bConnected)
			{
				System.out.println(sAdminLine);
				if (sAdminLine.indexOf(",Connected,") > -1)
				{
					System.out.println("IQConnect is connected to the server.");
					bConnected = true;
				}
				else if (sAdminLine.indexOf(",Not Connected,") > -1)
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
			
			// String to hold what the user typed in.
			String	sLine;
				
			// creates a socket connection to localhost (IP address 127.0.0.1) on port 9100.
			// This is that port that IQFeed listens on for lookup requests. 
			Socket s = new Socket(InetAddress.getByName("localhost"), 9100);
	
			// buffer to incomming data.
			sin = new BufferedReader(new InputStreamReader(s.getInputStream()));
			// buffer for out going commands.
			sout = new BufferedWriter(new OutputStreamWriter(s.getOutputStream()));
			// buffer for incomming menu commands, that the user of the application enters.
			in = new BufferedReader(new InputStreamReader(System.in));

                        // Set the lookup port protocol  
                        sout.write(String.format("S,SET PROTOCOL,%s\r\n", config.most_recent_protocol ));
                        sout.flush();	

			while (true) {
				System.out.print("\n 1) News Configuration\n" +
								" 2) News headlines by source\n" +
								" 3) News headlines by symbol\n" +
								" 4) News story\n" +
								" 5) News story count for symbol\n" +
								"\n" +
								" 6) Symbol Search by Filter\n" +
								" 7) Symbol by SIC\n" +
								" 8) Symbol by NAICS\n" +
								"\n" +
								" 9) Chain lookup for Futures\n" +
								"10) Chain lookup for Future Spreads\n" +
								"11) Chain lookup for Future Options\n" +
								"12) Chain lookup for Index or Equity Options\n" +
								"\n" +
								"13) Get tick history by number of datapoints\n" +
								"14) Get tick history by number of days\n" +
								"15) Get tick history by timeframe\n" +
								"16) Get interval history by number of datapoints\n" +
								"17) Get interval history by number of days\n" +
								"18) Get interval history by timeframe\n" +
								"19) Get daily history by number of datapoints\n" +
								"20) Get daily history by timeframe\n" +
								"21) Get weekly history by number of datapoints\n" +
								"22) Get monthly history by number of datapoints\n" +
								"\n" +
								"Q to quit\n" +
								"==>");
	
				sLine = in.readLine();
				if (sLine.equalsIgnoreCase("q"))
				{
					break;
				}
				else if (sLine.equals("1"))
				{
					GetNewsConfig();
				}
				else if (sLine.equals("2"))
				{
					GetNewsHeadlinesBySource();
				}
				else if (sLine.equals("3"))
				{
					GetNewsHeadlinesBySymbol();
				}
				else if (sLine.equals("4"))
				{
					GetNewsStory();
				}
				else if (sLine.equals("5"))
				{
					GetNewsStoryCounts();
				}
				else if (sLine.equals("6"))
				{
					GetSymbolsByFilter();
				}
				else if (sLine.equals("7"))
				{
					GetSymbolsBySIC();
				}
				else if (sLine.equals("8"))
				{
					GetSymbolsByNAICS();
				}
				else if (sLine.equals("9"))
				{
					GetFuturesChain();
				}
				else if (sLine.equals("10"))
				{
					GetFutureSpreadChain();
				}
				else if (sLine.equals("11"))
				{
					GetFutureOptionChain();
				}
				else if (sLine.equals("12"))
				{
					GetEquityOrIndexOptionChain();
				}
				else if (sLine.equals("13"))
				{
					GetHistoryTickDatapoints();
				}
				else if (sLine.equals("14"))
				{
					GetHistoryTickDays();
				}
				else if (sLine.equals("15"))
				{
					GetHistoryTickTimeframe();
				}
				else if (sLine.equals("16"))
				{
					GetHistoryIntervalDatapoints();
				}
				else if (sLine.equals("17"))
				{
					GetHistoryIntervalDays();
				}
				else if (sLine.equals("18"))
				{
					GetHistoryIntervalTimeframe();
				}
				else if (sLine.equals("19"))
				{
					GetHistoryDailyDatapoints();
				}
				else if (sLine.equals("20"))
				{
					GetHistoryDailyTimeframe();
				}
				else if (sLine.equals("21"))
				{
					GetHistoryWeeklyDatapoints();
				}
				else if (sLine.equals("22"))
				{
					GetHistoryMonthlyDatapoints();
				}
			}
		} catch (Exception e)
		{
			e.printStackTrace();
		}
		System.out.println("Exiting...\n");
	}

	/**
	 * JAVA application's main run method.  It creates the lookup client
	 * and then calls the run method which displays the menu and
	 * then waits for input by the user. 
	 * 
	 * @param args
	 */
	public static void main(String args[]) {
		// creates an instant of the lookup client application.
		LookupClient me = new LookupClient();
		// executes the run function.
		me.run();
	}
}
