javac -verbose -cp "../jars/postgresql-9.4-1202.jdbc42.jar:." common/Java_Config.java common/IQFeed_Socket.java DBHist/DBHist.java -d DBHist/classes
java -cp "../jars/postgresql-9.4-1202.jdbc42.jar:DBHist/classes" DBHist
