//-----------------------------------------------------------
//-----------------------------------------------------------
//
//             System: IQFeed
//       Filename: DBFeed.java
//
//-----------------------------------------------------------
//
//            Proprietary Software Product
//
//           Data Transmission Network Inc.
//           9110 West Dodge Road Suite 200
//               Omaha, Nebraska  68114
//
//    Copyright (c) by Data Transmission Network 2008
//                 All Rights Reserved
//
//
//-----------------------------------------------------------
// Module Description: Standard application source file
//         References: None
//           IDE: Netbeans 7.4
//             Author: Tim Walter
//        Modified By: 
//
//-----------------------------------------------------------
// Website for API information: http://www.iqfeed.net/dev/
//-----------------------------------------------------------
/******************************************************************************
 * DISCLAIMER:  These apps are designed with simplicity in mind and are not 
 * designed for copy and paste development.  You will need to consider 
 * performance enhancements based upon your own needs and implement your
 * solution accordingly. They are a guide to get people started, nothing more.
 ******************************************************************************/

import java.io.*;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;

import javax.swing.*;
import java.awt.event.*;
//import common.*;

public class DBFeed extends javax.swing.JFrame implements ActionListener, WindowListener
{
    //Define variables for use throughout the code
    private int IQFEED_LEVEL1_PORT_DEFAULT = 5009;      //Defaults to 5009, adjustable in the registy.
	//IQFeed_Socket is defined in the common folder, effectively it is a socket with a buffered reader and writer added.
    IQFeed_Socket C_Level1IQFeed_Socket;

    /**
     * Creates new form Level1_Example_Frame
     */
   

    public void getFeeds() {
  	  Connection c=FeedDB.getConnection();
  	  Statement statement = null;

  		String selectTableSQL = "SELECT mi.sym, mi.exch FROM main_instrument mi WHERE mi.sec_type='STK' AND subscribe=True";
  		
  		try {
  			statement = c.createStatement();

  			System.out.println(selectTableSQL);

  			// execute select SQL stetement
  			ResultSet rs = statement.executeQuery(selectTableSQL);
  			
  			while (rs.next()) {

  				String sym = rs.getString("sym");
  				String exch = rs.getString("exch");

  				System.out.println("sym : " + sym + " | " + exch);

  				String sCommand = "w" + sym +"\r\n";
  		        sendMessage(sCommand);
  		        updateCommandLabelResult(sCommand);
  			}
  			// Turn on News
  	        String sCommand = "S,NEWSON\r\n";
  	        sendMessage(sCommand);
  	        updateCommandLabelResult(sCommand);         

  	        
  	        sCommand = "S,REQUEST ALL UPDATE FIELDNAMES\r\n";
  	        sendMessage(sCommand);
  	        updateCommandLabelResult(sCommand);         

  	        sCommand = "S,SELECT UPDATE FIELDS,Symbol,Ask,Ask Size,Bid,Bid Size,Total Volume,VWAP,Open,High,Low,Close,Most Recent Trade,Most Recent Trade Size,Most Recent Trade Time,Most Recent Trade Market Center,Message Contents,Most Recent Trade Conditions\r\n";
	        sendMessage(sCommand);
	        updateCommandLabelResult(sCommand);         

  	        //sCommand = "S,REQUEST CURRENT UPDATE FIELDNAMES\r\n";
  	        //sendMessage(sCommand);
  	        //updateCommandLabelResult(sCommand);         


  		} catch (SQLException e) {

  			System.out.println(e.getMessage());

  		} finally {

  			if (statement != null) {
  				//statement.close();
  			}

  			if (c != null) {
  				//c.close();
  			}

  		}
    }
    public DBFeed() 
    {
		super("Level 1 Socket");
        //Draw the window
        initComponents();        
		boolean Connected = false;
		C_Level1IQFeed_Socket = new IQFeed_Socket();
        //Attempt to connect our socket

			System.out.println("Connecting to Level 1 port.");
			// requests a socket connection to localhost on port IQFEED_LEVEL1_PORT_DEFAULT, default = localhost and port 5009
			// Port 5009 is configurable in the registry.  See registry settings in the documentation.
			// If False is returned we are not able to connect display an error and exit. 
			if (!C_Level1IQFeed_Socket.ConnectSocket(IQFEED_LEVEL1_PORT_DEFAULT))
			{
				JOptionPane.showMessageDialog(null, "Did you forget to login first?\nTake a look at the LaunchingTheFeed example app.");
				System.exit(1);				
			}
			
			System.out.println("Connected to Level 1 port.");
			C_Level1IQFeed_Socket.CreateBuffers();

            //Initialize the protocol, this prepares us for commands to come and verifies that our socket is working as intended.
            try
            {
                Java_Config config = new Java_Config();
                C_Level1IQFeed_Socket.brBufferedWriter.write(String.format("S,SET PROTOCOL,%s\r\n",config.most_recent_protocol));
                C_Level1IQFeed_Socket.brBufferedWriter.flush();
                System.out.println("Message Posted, Protocol set.");
            }
            catch (Exception eError) 
            {
                updateCommandLabelError("Error writing to socket.\n%s", eError.toString());
            }
            
            Level1_Listener thread = new Level1_Listener();
            thread.start();
        }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents()
    {

        btnRemoveAllWatches = new javax.swing.JButton();
        btnSetFieldset = new javax.swing.JButton();
        btnGetAllUpdateSummaryFields = new javax.swing.JButton();
        btnGetCurrentFieldset = new javax.swing.JButton();
        btnDisconnect = new javax.swing.JButton();
        btnGetAllFundamentalFields = new javax.swing.JButton();
        btnForce = new javax.swing.JButton();
        btnNewsOff = new javax.swing.JButton();
        lblSymbol = new javax.swing.JLabel();
        btnWatch = new javax.swing.JButton();
        btnRemoveRegionals = new javax.swing.JButton();
        btnConnect = new javax.swing.JButton();
        btnTimestamp = new javax.swing.JButton();
        btnWatchRegionals = new javax.swing.JButton();
        btnTradesOnlyWatch = new javax.swing.JButton();
        btnRemove = new javax.swing.JButton();
        btnGetCurrentWatches = new javax.swing.JButton();
        lblDataSentToServer = new javax.swing.JLabel();
        btnNewsOn = new javax.swing.JButton();
        btnRequestStats = new javax.swing.JButton();
        jScrollPane2 = new javax.swing.JScrollPane();
        txtDisplay = new javax.swing.JTextArea();
        txtSymbol = new javax.swing.JTextField();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        btnRemoveAllWatches.setText("Remove All Watches");
        btnRemoveAllWatches.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnRemoveAllWatchesActionPerformed(evt);
            }
        });

        btnSetFieldset.setText("Set Fieldset");
        btnSetFieldset.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnSetFieldsetActionPerformed(evt);
            }
        });

        btnGetAllUpdateSummaryFields.setText("Get All Update/Summary Fields");
        btnGetAllUpdateSummaryFields.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnGetAllUpdateSummaryFieldsActionPerformed(evt);
            }
        });

        btnGetCurrentFieldset.setText("Get Current Fieldset");
        btnGetCurrentFieldset.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnGetCurrentFieldsetActionPerformed(evt);
            }
        });

        btnDisconnect.setText("Disconnect");
        btnDisconnect.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnDisconnectActionPerformed(evt);
            }
        });

        btnGetAllFundamentalFields.setText("Get All Fundamental Fields");
        btnGetAllFundamentalFields.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnGetAllFundamentalFieldsActionPerformed(evt);
            }
        });

        btnForce.setText("Force");
        btnForce.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnForceActionPerformed(evt);
            }
        });

        btnNewsOff.setText("News Off");
        btnNewsOff.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnNewsOffActionPerformed(evt);
            }
        });

        lblSymbol.setText("Symbol / Request Data");

        btnWatch.setText("Watch");
        btnWatch.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnWatchActionPerformed(evt);
            }
        });

        btnRemoveRegionals.setText("Remove Regionals");
        btnRemoveRegionals.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnRemoveRegionalsActionPerformed(evt);
            }
        });

        btnConnect.setText("Connect");
        btnConnect.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnConnectActionPerformed(evt);
            }
        });

        btnTimestamp.setText("Timestamp");
        btnTimestamp.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnTimestampActionPerformed(evt);
            }
        });

        btnWatchRegionals.setText("Watch Regionals");
        btnWatchRegionals.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnWatchRegionalsActionPerformed(evt);
            }
        });

        btnTradesOnlyWatch.setText("Trades Only Watch");
        btnTradesOnlyWatch.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnTradesOnlyWatchActionPerformed(evt);
            }
        });

        btnRemove.setText("Remove");
        btnRemove.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnRemoveActionPerformed(evt);
            }
        });

        btnGetCurrentWatches.setText("Get Current Watches");
        btnGetCurrentWatches.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnGetCurrentWatchesActionPerformed(evt);
            }
        });

        lblDataSentToServer.setText("Message Sent: ");
        lblDataSentToServer.setToolTipText("");
        lblDataSentToServer.setVerticalAlignment(javax.swing.SwingConstants.TOP);
        lblDataSentToServer.setVerticalTextPosition(javax.swing.SwingConstants.TOP);

        btnNewsOn.setText("News On");
        btnNewsOn.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnNewsOnActionPerformed(evt);
            }
        });

        btnRequestStats.setText("Request Stats");
        btnRequestStats.addActionListener(new java.awt.event.ActionListener()
        {
            public void actionPerformed(java.awt.event.ActionEvent evt)
            {
                btnRequestStatsActionPerformed(evt);
            }
        });

        txtDisplay.setColumns(20);
        txtDisplay.setRows(5);
        jScrollPane2.setViewportView(txtDisplay);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 723, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addGroup(layout.createSequentialGroup()
                                .addComponent(btnRemove, javax.swing.GroupLayout.PREFERRED_SIZE, 154, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(btnRemoveRegionals)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(btnForce)
                                .addGap(18, 18, 18)
                                .addComponent(btnNewsOff, javax.swing.GroupLayout.PREFERRED_SIZE, 97, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(btnDisconnect)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(btnRemoveAllWatches, javax.swing.GroupLayout.PREFERRED_SIZE, 139, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                                .addComponent(lblDataSentToServer, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addGroup(layout.createSequentialGroup()
                                    .addGap(0, 12, Short.MAX_VALUE)
                                    .addComponent(btnGetAllFundamentalFields)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(btnGetAllUpdateSummaryFields)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(btnGetCurrentFieldset, javax.swing.GroupLayout.PREFERRED_SIZE, 129, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(btnSetFieldset)
                                    .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                    .addComponent(btnRequestStats, javax.swing.GroupLayout.PREFERRED_SIZE, 131, javax.swing.GroupLayout.PREFERRED_SIZE)))
                            .addGroup(layout.createSequentialGroup()
                                .addGap(14, 14, 14)
                                .addComponent(lblSymbol)
                                .addGap(18, 18, 18)
                                .addComponent(txtSymbol))
                            .addGroup(layout.createSequentialGroup()
                                .addGap(10, 10, 10)
                                .addComponent(btnWatch)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(btnTradesOnlyWatch, javax.swing.GroupLayout.PREFERRED_SIZE, 125, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(2, 2, 2)
                                .addComponent(btnWatchRegionals, javax.swing.GroupLayout.PREFERRED_SIZE, 112, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(btnTimestamp)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(btnNewsOn, javax.swing.GroupLayout.PREFERRED_SIZE, 75, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(14, 14, 14)
                                .addComponent(btnConnect, javax.swing.GroupLayout.PREFERRED_SIZE, 79, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(btnGetCurrentWatches)))
                        .addContainerGap(20, Short.MAX_VALUE))))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGap(7, 7, 7)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblSymbol, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(txtSymbol, javax.swing.GroupLayout.PREFERRED_SIZE, 34, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.CENTER)
                    .addComponent(btnWatch)
                    .addComponent(btnConnect)
                    .addComponent(btnTradesOnlyWatch)
                    .addComponent(btnGetCurrentWatches)
                    .addComponent(btnWatchRegionals)
                    .addComponent(btnTimestamp)
                    .addComponent(btnNewsOn))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnRemove)
                    .addComponent(btnRemoveRegionals)
                    .addComponent(btnForce)
                    .addComponent(btnNewsOff)
                    .addComponent(btnDisconnect)
                    .addComponent(btnRemoveAllWatches))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(btnGetAllFundamentalFields)
                    .addComponent(btnSetFieldset)
                    .addComponent(btnGetAllUpdateSummaryFields)
                    .addComponent(btnGetCurrentFieldset)
                    .addComponent(btnRequestStats))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(lblDataSentToServer, javax.swing.GroupLayout.PREFERRED_SIZE, 51, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 290, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents
//-----------------------------------------------------------
// void btnGetCurrentFieldsetActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "REQUEST CURRENT UPDATE FIELDNAMES" command.
*/
//-----------------------------------------------------------
    private void btnGetCurrentFieldsetActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnGetCurrentFieldsetActionPerformed
        //Message format: S,REQUEST CURRENT UPDATE FIELDNAMES<CR><LF> 
        String sCommand = "S,REQUEST CURRENT UPDATE FIELDNAMES\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnGetCurrentFieldsetActionPerformed
//-----------------------------------------------------------
// void btnWatchActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Watch" command.
*/
//-----------------------------------------------------------
    private void btnWatchActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnWatchActionPerformed
    {//GEN-HEADEREND:event_btnWatchActionPerformed
        //Message format: w[SYMBOL]<CR><LF> 
        String sCommand = "w" + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);
    }//GEN-LAST:event_btnWatchActionPerformed
//-----------------------------------------------------------
// void btnTradesOnlyWatchActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Trades Only Watch" command.
*/
//-----------------------------------------------------------
    private void btnTradesOnlyWatchActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnTradesOnlyWatchActionPerformed
    {//GEN-HEADEREND:event_btnTradesOnlyWatchActionPerformed
        //Message format: t[SYMBOL]<CR><LF> 
        String sCommand = "t" + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);
    }//GEN-LAST:event_btnTradesOnlyWatchActionPerformed
//-----------------------------------------------------------
// void btnWatchRegionalsActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Watch Regional Quotes" command.
*/
//-----------------------------------------------------------
    private void btnWatchRegionalsActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnWatchRegionalsActionPerformed
    {//GEN-HEADEREND:event_btnWatchRegionalsActionPerformed
        //Message format: r[SYMBOL]<CR><LF> 
        String sCommand = "S,REGON," + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnWatchRegionalsActionPerformed
//-----------------------------------------------------------
// void btnForceActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Force Refresh" command.
*/
//-----------------------------------------------------------
    private void btnForceActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnForceActionPerformed
    {//GEN-HEADEREND:event_btnForceActionPerformed
        //Message format: f[SYMBOL]<CR><LF> 
        String sCommand = "f" + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnForceActionPerformed
//-----------------------------------------------------------
// void btnTimestampActionPerformed(java.awt.event.ActionEvent evt)  
/**
 * Button click event to send the "Timestamp" command.
*/
//-----------------------------------------------------------
    private void btnTimestampActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnTimestampActionPerformed
    {//GEN-HEADEREND:event_btnTimestampActionPerformed
        //Message format: T<CR><LF> 
        String sCommand = "T" +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnTimestampActionPerformed
//-----------------------------------------------------------
// void btnRemoveRegionalsActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Remove Regional Watches" command.
*/
//-----------------------------------------------------------
    private void btnRemoveRegionalsActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnRemoveRegionalsActionPerformed
    {//GEN-HEADEREND:event_btnRemoveRegionalsActionPerformed
        //Message format: S,REGOFF,[SYMBOL]<CR><LF> 
        String sCommand = "S,REGOFF," + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnRemoveRegionalsActionPerformed
//-----------------------------------------------------------
// void btnNewsOnActionPerformed(java.awt.event.ActionEvent evt)   
/**
 * Button click event to send the "News On" command.
*/
//-----------------------------------------------------------
    private void btnNewsOnActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnNewsOnActionPerformed
    {//GEN-HEADEREND:event_btnNewsOnActionPerformed
        //Message format: S,NEWSON<CR><LF> 
        String sCommand = "S,NEWSON\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnNewsOnActionPerformed
//-----------------------------------------------------------
// void btnNewsOffActionPerformed(java.awt.event.ActionEvent evt)  
/**
 * Button click event to send the "News Off" command.
*/
//-----------------------------------------------------------
    private void btnNewsOffActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnNewsOffActionPerformed
    {//GEN-HEADEREND:event_btnNewsOffActionPerformed
        //Message format: S,NEWSOFF\r\n
        String sCommand = "S,NEWSOFF\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnNewsOffActionPerformed
//-----------------------------------------------------------
// void btnRemoveActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Remove Watch" command.
*/
//-----------------------------------------------------------
    private void btnRemoveActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnRemoveActionPerformed
    {//GEN-HEADEREND:event_btnRemoveActionPerformed
        //Message format: r[SYMBOL]<CR><LF> 
        String sCommand = "r" + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnRemoveActionPerformed
//-----------------------------------------------------------
// void btnRequestStatsActionPerformed(java.awt.event.ActionEvent evt)
/**
 * Button click event to send the "Request Stats" command.
*/
//-----------------------------------------------------------
    private void btnRequestStatsActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnRequestStatsActionPerformed
    {//GEN-HEADEREND:event_btnRequestStatsActionPerformed
        //Message format: S,REQUEST STATS<CR><LF> 
        String sCommand = "S,REQUEST STATS\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnRequestStatsActionPerformed
//-----------------------------------------------------------
// void btnGetAllFundamentalFieldsActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Get All Fundamental Fields" command.
*/
//-----------------------------------------------------------
    private void btnGetAllFundamentalFieldsActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnGetAllFundamentalFieldsActionPerformed
    {//GEN-HEADEREND:event_btnGetAllFundamentalFieldsActionPerformed
        //Message format: S,REQUEST FUNDAMENTAL FIELDNAMES<CR><LF> 
        String sCommand = "S,REQUEST FUNDAMENTAL FIELDNAMES\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnGetAllFundamentalFieldsActionPerformed
//-----------------------------------------------------------
// void btnGetAllUpdateSummaryFieldsActionPerformed(java.awt.event.ActionEvent evt)    
/**
 * Button click event to send the "Request All Update Fields" command.
*/
//-----------------------------------------------------------
    private void btnGetAllUpdateSummaryFieldsActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnGetAllUpdateSummaryFieldsActionPerformed
    {//GEN-HEADEREND:event_btnGetAllUpdateSummaryFieldsActionPerformed
        //Message format: S,REQUEST ALL UPDATE FIELDNAMES<CR><LF> 
        String sCommand = "S,REQUEST ALL UPDATE FIELDNAMES\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnGetAllUpdateSummaryFieldsActionPerformed
//-----------------------------------------------------------
// void btnSetFieldsetActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Set Field Sets" command.
*/
//-----------------------------------------------------------
    private void btnSetFieldsetActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnSetFieldsetActionPerformed
    {//GEN-HEADEREND:event_btnSetFieldsetActionPerformed
        //Message format: S,SELECT UPDATE FIELDS,[FIELD 1 NAME],[FIELD 2 NAME],...,[FIELD N NAME]<CR><LF> 
        String sCommand = "S,SELECT UPDATE FIELDS," + txtSymbol.getText() +"\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnSetFieldsetActionPerformed
//-----------------------------------------------------------
// void btnGetCurrentWatchesActionPerformed(java.awt.event.ActionEvent evt)   
/**
 * Button click event to send the "Request Watches" command.
*/
//-----------------------------------------------------------
    private void btnGetCurrentWatchesActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnGetCurrentWatchesActionPerformed
    {//GEN-HEADEREND:event_btnGetCurrentWatchesActionPerformed
        //Message format: S,REQUEST WATCHES<CR><LF> 
        String sCommand = "S,REQUEST WATCHES\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnGetCurrentWatchesActionPerformed
//-----------------------------------------------------------
// void btnConnectActionPerformed(java.awt.event.ActionEvent evt)   
/**
 * Button click event to send the "Connect" command.
*/
//-----------------------------------------------------------
    private void btnConnectActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnConnectActionPerformed
    {//GEN-HEADEREND:event_btnConnectActionPerformed
        //Message format: S,CONNECT<CR><LF> 
        String sCommand = "S,CONNECT\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);             
    }//GEN-LAST:event_btnConnectActionPerformed
//-----------------------------------------------------------
// void btnDisconnectActionPerformed(java.awt.event.ActionEvent evt) 
/**
 * Button click event to send the "Disconnect" command.
*/
//-----------------------------------------------------------
    private void btnDisconnectActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnDisconnectActionPerformed
    {//GEN-HEADEREND:event_btnDisconnectActionPerformed
        //Message format: S,DISCONNECT<CR><LF> 
        String sCommand = "S,DISCONNECT\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnDisconnectActionPerformed
//-----------------------------------------------------------
// void btnRemoveAllWatchesActionPerformed(java.awt.event.ActionEvent evt)  
/**
 * Button click event to send the "Remove All Watches" command.
*/
//-----------------------------------------------------------
    private void btnRemoveAllWatchesActionPerformed(java.awt.event.ActionEvent evt)//GEN-FIRST:event_btnRemoveAllWatchesActionPerformed
    {//GEN-HEADEREND:event_btnRemoveAllWatchesActionPerformed
        //Message format: S,UNWATCH ALL<CR><LF> 
        String sCommand = "S,UNWATCH ALL\r\n";
        sendMessage(sCommand);
        updateCommandLabelResult(sCommand);         
    }//GEN-LAST:event_btnRemoveAllWatchesActionPerformed
//-----------------------------------------------------------
// void sendMessage(String sCommand) 
/**
 * Sends a command to the output stream for processing by the Level1_Listener class\thread.
 * 
 *   @param sCommand, a String with a full message ready to be sent to the server
 *                    including carriage return and line feed. Example: "S,UNWATCH ALL\r\n"
*/
//-----------------------------------------------------------    
    void sendMessage(String sCommand) 
    {
        try 
        {
            //Send the message and flush to be sure it is handled right away.
            C_Level1IQFeed_Socket.brBufferedWriter.write(sCommand);
            C_Level1IQFeed_Socket.brBufferedWriter.flush();
            //Label will show the actual string sent to the server.
            updateCommandLabelResult(sCommand + " sent.");
        }
        catch(IOException eError) 
        {
            updateCommandLabelError("Error:" + sCommand, eError.toString());
        }
    }
//-----------------------------------------------------------
// void updateCommandLabelResult(String sCommand) 
/**
 * Displays a message to a user that identifies the full message being sent.
 * 
 *   @param sCommand, a String with a full message ready to be sent to the server
 *                    including carriage return and line feed. Example: "S,UNWATCH ALL\r\n"
*/
//-----------------------------------------------------------  
    void updateCommandLabelResult(String sCommand) 
    {
        lblDataSentToServer.setText("Message Sent: " + sCommand); 
    }
//-----------------------------------------------------------
// void updateCommandLabelError(String sCommand, String sError) 
/**
 * Displays a message to a user that identifies the error that may have occured.
 * 
 *   @param sCommand, a String with a full message ready to be sent to the server
 *                    including carriage return and line feed. Example: "S,UNWATCH ALL\r\n"
 *   @param sError, a String passed from the exception object.
*/
//-----------------------------------------------------------   
    void updateCommandLabelError(String sCommand, String sError) 
    {
        String sErrorMessage = String.format("%s \n Error Message: %s",sCommand, sError);
        lblDataSentToServer.setText(sErrorMessage); 
    }    
    /**
     * @param args the command line arguments
     */
//-----------------------------------------------------------
// public static void main(String args[]) 
// 
/**
 * Main, instantiates the window and sets it to being visible.
*/
//-----------------------------------------------------------    
    public static void main(String args[]) 
    {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(DBFeed.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(DBFeed.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(DBFeed.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(DBFeed.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        
        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() 
        {
            public void run() 
            {
                new DBFeed().setVisible(true);
                
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnConnect;
    private javax.swing.JButton btnDisconnect;
    private javax.swing.JButton btnForce;
    private javax.swing.JButton btnGetAllFundamentalFields;
    private javax.swing.JButton btnGetAllUpdateSummaryFields;
    private javax.swing.JButton btnGetCurrentFieldset;
    private javax.swing.JButton btnGetCurrentWatches;
    private javax.swing.JButton btnNewsOff;
    private javax.swing.JButton btnNewsOn;
    private javax.swing.JButton btnRemove;
    private javax.swing.JButton btnRemoveAllWatches;
    private javax.swing.JButton btnRemoveRegionals;
    private javax.swing.JButton btnRequestStats;
    private javax.swing.JButton btnSetFieldset;
    private javax.swing.JButton btnTimestamp;
    private javax.swing.JButton btnTradesOnlyWatch;
    private javax.swing.JButton btnWatch;
    private javax.swing.JButton btnWatchRegionals;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JLabel lblDataSentToServer;
    private javax.swing.JLabel lblSymbol;
    private javax.swing.JTextArea txtDisplay;
    private javax.swing.JTextField txtSymbol;
    // End of variables declaration//GEN-END:variables

 /******************************************************************
 ******************************************************************
 ******************************************************************/
//-----------------------------------------------------------
// void actionPerformed(ActionEvent e)
// void windowOpened(WindowEvent e)
// void windowClosing(WindowEvent e)
// void windowIconified(WindowEvent e)
// void windowDeiconified(WindowEvent e)
// void windowClosed(WindowEvent e)
// void windowActivated(WindowEvent e)
// void windowActivated(WindowEvent e)        
/**
 * These 8 Window's event functions are left effectively blank due to simplicity, but are required for compilation.
*/
//-----------------------------------------------------------
// Start of Window's events.
    @Override
    public void actionPerformed(ActionEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void windowOpened(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void windowClosing(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void windowClosed(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void windowIconified(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public void windowDeiconified(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
    @Override
    public void windowActivated(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
    @Override
    public void windowDeactivated(WindowEvent e)
    {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }
    //End of window's events
    /******************************************************************
    ******************************************************************
    ******************************************************************/
    
    
    //Class to execute and listen to replies from the server.
    //I am displaying the data returned in this function for simplicity to the text Window.
    //Considerations for performance will be needed as this will not work for most normal usage.
    class Level1_Listener extends Thread
    {
    //-----------------------------------------------------------
    // void run()
    /**
    */
    //  Notes:  Check for data on the socket, process it if it exists by displaying
    //          to the text window.
    //
    //-----------------------------------------------------------
    		String dateStr="";
    		Date timestamp=new Date();
    		
            public void run()
            {
                    String line;
                    try
                    {
                    		getFeeds();

                            while ((line = C_Level1IQFeed_Socket.brBufferedReader.readLine()) != null)
                            {
                                    System.out.println(line);
                                    txtDisplay.append(line + "\n");
                                    try {
                                		String[] items=line.split(",");
                                		if (items.length > 0) {
	                                		char msg=items[0].charAt(0);
	                                		switch (msg) {
	                            	            case 'Q': procQuoteMsg(line);
	                            	                     break;
	                            	            case 'S': procFieldMsg(line);
	                            	                     break;
	                            	            case 'T': procTimeMsg(line);
	                            	            		 break;
	                                		 }
                                		}
                                    } catch (Exception e) {
                                    	System.out.println(e.toString());
                                    }
                            }
                    }
                    catch (Exception eError) 
                    { 
                        updateCommandLabelError("Unable to read from socket.\n" , eError.toString());
                    }
            }
            
            void procFieldMsg(String msg) {
            	String[] fields=msg.split(",");
            	if (fields.length > 2) {
            		if (fields[1].equals("UPDATE FIELDNAMES")) {
            			/*
            			 * S,UPDATE FIELDNAMES,Symbol,Exchange ID,Last,Change,Percent Change,
            			 * Total Volume,High,Low,Bid,Ask,Bid Size,Ask Size,Tick,Range,Open Interest,
            			 * Open,Close,Spread,Settle,Delay,Restricted Code,Net Asset Value,Average Maturity,
            			 * 7 Day Yield,Extended Trading Change,Extended Trading Difference,Price-Earnings Ratio,
            			 * Percent Off Average Volume,Bid Change,Ask Change,Change From Open,Market Open,
            			 * Volatility,Market Capitalization,Fraction Display Code,Decimal Precision,
            			 * Days to Expiration,Previous Day Volume,Open Range 1,Close Range 1,
            			 * Open Range 2,Close Range 2,Number of Trades Today,VWAP,TickID,Financial Status Indicator,
            			 * Settlement Date,Bid Market Center,Ask Market Center,Available Regions,Last Size,Last Time,
            			 * Last Market Center,Most Recent Trade,Most Recent Trade Size,Most Recent Trade Time,
            			 * Most Recent Trade Conditions,Most Recent Trade Market Center,Extended Trade,
            			 * Extended Trade Size,Extended Trade Time,Extended Trade Market Center,Message Contents,
            			 * Ask Time,Bid Time,Last Date,Extended Trade Date,Most Recent Trade Date

            			 */
            		} else if (fields[1].equals("CURRENT UPDATE FIELDNAMES")) {
            			/*
            			 * S,CURRENT UPDATE FIELDNAMES,Symbol,Ask,Ask Size,Bid,Bid Size,Total Volume,VWAP,
            			 * Open,High,Low,Close,
            			 * Most Recent Trade,Most Recent Trade Size,Most Recent Trade Time,
            			 * Most Recent Trade Market Center,Message Contents,Most Recent Trade Conditions

            			 */
            			
            		}
            	}
            }
            void procQuoteMsg(String msg) {
            	/*
            	 * Q,ATVI,48.5100,135,11:13:25.175857,18,1394955,48.5000,6400,48.5100,900,48.1200,48.6450,48.0000,48.0600,ba,01,
				   Q,ATVI,48.5100,135,11:13:25.175857,18,1394955,48.5000,6400,48.5100,800,48.1200,48.6450,48.0000,48.0600,ba,01,
            	 */
            	String[] fields=msg.split(",");
            }
            
            void procTimeMsg(String msg) {
            	/*
            	 * T,20170308 11:13:30
				*/
            	String[] fields=msg.split(",");
            	if (fields.length == 2) {
            		try {
		            	SimpleDateFormat format1 = new SimpleDateFormat("yyyyMMdd hh:mm:ss");
		            	String date=fields[1];
		            	Date d1 = format1.parse( date );
		            	this.timestamp=d1;
		            	this.dateStr=date;
            		} catch (Exception e) {
            			System.out.println(e.toString());
            		}
            	}
            }
    }
}
