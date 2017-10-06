@ECHO OFF 
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM
REM             System: IQFeed
REM       Program Name: ConsoleBenchmarkTool
REM        Module Name: ConsoleBenchmarkTool.bat
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
REM Module Description: Benchmark utility to aid in determining if your bandwidth can handle the incoming load.
REM         References: None
REM           Compiler: Netbeans 7.4, Java 1.7045
REM             Author: Tim Walter
REM        Modified By: 
REM
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM Website for API information: http://www.iqfeed.net/dev/api/docs/
REM -----------------------------------------------------------


REM This utility shows both a compilation example and how to execute the compiled code.

REM This line compiles the IQFeed_Socket object from the common folder and the ConsoleBenchmarkTool together and places the class files 
REM in the ConsoleBenchmarkTool\classes folder.
javac -verbose -cp "."  common\Java_Config.java common\IQFeed_Socket.java ConsoleBenchmarkTool\ConsoleBenchmarkTool.java -d ConsoleBenchmarkTool\classes


REM This command executes the tool.
java -cp "ConsoleBenchmarkTool\classes" ConsoleBenchmarkTool
pause
