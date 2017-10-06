@ECHO OFF 
REM -----------------------------------------------------------
REM -----------------------------------------------------------
REM
REM             System: IQFeed
REM       Program Name: Level2Socket
REM        Module Name: Level2Socket.bat
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
REM Module Description: The Level1Socket example provides illustration of the 
REM various level 2 commands that are available and their returns.
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


javac -verbose -cp "." common\Java_Config.java  common\IQFeed_Socket.java Level2Socket\Level2Socket.java -d Level2Socket\classes


REM This command executes the tool.
java -cp "Level2Socket\classes" Level2Socket
pause