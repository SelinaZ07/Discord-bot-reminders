# Discord-bot-reminders
This repository includes all the code files for the Discord Bot reminder functionality. This functionality allows the bot to send Discord user reminders to a certain task. 
The following are the things you need:
1. A google spreadsheet that contains:
   - Discord user ID
   - Name
   - Due dates
   - Status
2. Libraries required:
   discord.py, apscheduler, pandas, gspread, oauth2client

Here is what the bot can do:
1. Send user reminders through DM at the designated time from the gspreadsheet
2. Give the user two options (shown as buttons): one is "done" the other is "enter new due date"
3. Then the bot will update this status back to the google spreadsheet

Things to work on:
- Allow the bot to send a second reminder based on the updated due date.
- Have restrictions on the new due date to ensure the new due date is reasonable.
- send a message to Dr. Bar if the second due date is still not met.
