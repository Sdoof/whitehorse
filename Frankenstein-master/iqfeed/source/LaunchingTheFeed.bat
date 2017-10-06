@ECHO OFF 
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM
REM             System: IQFeed
REM       Program Name: LaunchingTheFeed
REM        Module Name: LaunchingTheFeed.bat
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
REM Module Description: Utility to show how to launch IQConnect and subsequently start the feed.
REM						Details the need to start the admin to hold the connection open until the 
REM						connection completes and then level1 data can begin.
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

REM This line compiles the IQFeed_Socket object from the common folder and the LaunchingTheFeed together and places the class files 
REM in the LaunchingTheFeed/classes folder.
javac -verbose -cp "." common/Java_Config.java  common/IQFeed_Socket.java LaunchingTheFeed/LaunchingTheFeed.java -d LaunchingTheFeed/classes


REM This command executes the tool.
java -cp "LaunchingTheFeed/classes" LaunchingTheFeed
pause