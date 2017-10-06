#!\bin\sh
#@ECHO OFF 
# -----------------------------------------------------------
# -----------------------------------------------------------
#
#             System: IQFeed
#       Program Name: Level1Socket
#        Module Name: Level1Socket.bat
#
# -----------------------------------------------------------
#
#            Proprietary Software Product
#
#           Data Transmission Network Inc.
#           9110 West Dodge Road Suite 200
#               Omaha, Nebraska  68114
#
#    Copyright (c) by Data Transmission Network 2010
#                 All Rights Reserved
#
#
# -----------------------------------------------------------
# Module Description: The Level1Socket example provides illustration of the 
# various level 1 commands that are available and their returns.
#         References: None
#           Compiler: Netbeans 7.4, Java 1.7045
#             Author: Tim Walter
#        Modified By: 
#
# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------
# Website for API information: http:\\www.iqfeed.net\dev\api\docs\
# -----------------------------------------------------------
javac -verbose -cp "..\jars\postgresql-42.0.0.jar;." common\FeedDB.java  common\Java_Config.java  common\IQFeed_Socket.java Level1Socket\Level1Socket.java -d Level1Socket\classes
# This command executes the tool.
java -cp "..\jars\postgresql-42.0.0.jar;Level1Socket\classes" Level1Socket
#pause