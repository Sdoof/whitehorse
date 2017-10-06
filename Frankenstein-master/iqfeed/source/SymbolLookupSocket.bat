@ECHO OFF 
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM
REM             System: IQFeed
REM       Program Name: SymbolLookupSocket
REM        Module Name: SymbolLookupSocket.bat
REM
REM -----------------------------------------------------------
REM
REM            Proprietary Software Product
REM
REM           Data Transmission Network Inc.
REM           9110 West Dodge Road Suite 200
REM               Omaha, Nebraska  68114
REM
REM    Copyright (c) by Data Transmission Network 2010
REM                 All Rights Reserved
REM
REM
REM -----------------------------------------------------------
REM Module Description: The SymbolLookupSocket example provides illustration of the 
REM commands to search for a symbol(s) from the symbol lookup socket.
REM         References: None
REM           Compiler: Netbeans 7.4, Java 1.7045
REM             Author: Tim Walter
REM        Modified By: 
REM
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM Website for API information: http://www.iqfeed.net/dev/
REM -----------------------------------------------------------


REM This utility shows both a compilation example and how to execute the compiled code.

javac -verbose -cp "." common\Java_Config.java  common\IQFeed_Socket.java SymbolLookupSocket\SymbolLookupSocket.java -d SymbolLookupSocket\classes


REM This command executes the tool.
java -cp "SymbolLookupSocket\classes" SymbolLookupSocket
pause