## Edits Log

- [x] Adam Shabbir at 01/10/2024 from ~16:00 to 16:28 - Making a class for accounts, which will contain account data. Just a general one for now, nothing unique yet.
- [x] Adam Shabbir at 01/10/2024 from 20:26 to 21:13 - Login function works, but a while loop or for loop needs to be implemented to allow for the user to try again.
- [x] Hasan Akhtar at 02/10/2024 from 07:06 to 07:13 - changed account reference to self to make specific to that object, added unit test for account in seperate cell, account still works and unit test good.
- [x] Adam Shabbir at 04/10/2024 from ~18:00 to 19:15 - Trying to make a test to allow for a limited number of logging in attempts. Also made some notes for myself on what I think should be developed.
- [x] Hasan Akhtar at 05/10/2024 from 16:36 to 18:15 - Making a class for storage and manipulation of all accounts (kinda like a mini database), updating Account class to include more essential methods, also adding Menu class to include interface methods of program. Added a unit test for each of these new additions. Features all fully working, just need minor improvements.
- [x] Adam Shabbir at 06/10/2024 from 15:20 to 16:40 - Added finance accounts class to track finances.
- [x] Hasan Akhtar at 06/10/2024 from 15:30 to 16:50 - Added admin account type and related methods, also added menu option 12 which allows and admin to add admin accounts, next need to add checks for admin permissions and new unit test, but this part now done.
- [x] Adam Shabbir at 09/10/2024 from 08:00 to 09:30 - Worked on the FinanceOptions class. The finance Options class is not completed.
- [x] Adam Shabbir at 11/10/2024 from 15:40 to 16:08 - Made minor fixes - Allowed the user to see their finance history, which shows their income and expenses. Finance options is still not completed, but significant progress made. Also wrote unit test for this, unit test shows that it is fully working at the moment.
- [x] Hasan Akhtar + Adam Shabbir at 12/10/2024 from 15:45 to 16:16 - Hasan added the options dictionary in the constructor method attributes. Also adjusted the SeeFinanceHistory method to make it more user-friendly. Adam added in the displayMenu and getChoice methods thereafter. Hasan also filled in financeOptions method of Menu class to reflect the changes to the FinanceOptions class.
- [x] Hasan Akhtar at 10/11/2024 from 09:30 to 10:30 - Added the Category class with its various methods. Also updated the Budgeting class to incorporate this new class.
- [x] Adam Shabbir at 10/11/2024 from 09:30 to 10:30 - Started work on the Reporting Class by adding in parameters and allowing dates to be converted into objects
- [x] Rayhaan Hussain at 10/11/2024 from 09:00 to 11:00 (noice) - Started work on the Transaction Notes class by allowing notes to be viewed, made and deleted
- [x] Hasan Akhtar at 01/12/2024 from 12:15 to 13:25 - Updated the Budgeting class to incorporate new Category class, final adjustments and added a progressCategory method to supplement this, also tested and all working as intended.
- [x] Adam Shabbir at 01/12/2024 from 12:15 to 13:15 - Made corrections to reporting class (forgot self 💀) and started to add a 2d array grid function that will add income and expenses of each day
- [x] Rayhaan Hussain at 01/12/2024 from 12:15 to 13:15 - Added a 2nd array "transactions" and can now process transactions (viewing, adding, deleting).
- [x] Hasan Akhtar at 21/12/2024 from 20:35 to 22:15 - Adjusted Finance Options to account for Reporting and generating the report
- [x] Adam Shabbir at 24/12/2024 for 30 minutes and at 25/12/2024 from 17:30 to 19:35 - Completed setDate method for Reporting class, which generates IDs and pairs a newly generated ID with a transaction date passed into the method.
- [x] Hasan Akhtar at 29/12/2024 from 16:15 to 17:30 - Adjusted Transaction Notes to integrate with the rest of the code and reflect the recent changes in Finance Options, also updated Finance Options to complete the integration and ran unit tests
- [x] Adam Shabbir at 29/12/2024 from 16:30 to 17:30 - Literally tried to figure out how to generate what to generate. Didn't do anything substantial except for 5 lines.
- [x] Hasan Akhtar at 26/01/2025 from 17:15 to 18:00 - Adjusted integration of whole program, added to Transaction Notes class and that's all
- [x] Adam Shabbir at 26/01/2025 from around 17:00 to 18:00: Refamilarised himself with his code (literally forgot what  was doing 💀💀💀) , almost took the start & end date parameters and made them into actual dates.
- [x] Rayhaan Hussain at 26/01/2025 from around 17:00 to 18:00: Researched graph generation libraries and techniques for data visualisation but couldn't implement it then, we decided not to try the implementation then
- [x] Hasan Akhtar at 02/02/2025 from around 15:00 to 16:30: Pulling everyting together, making the Python Flask version 
- [x] Adam Shabbir at 02/02/2025 from around 15:00 to 16:30: Finally finished the reporting class, integrating everything and running final tests
- [x] Rayhaan Hussain at 02/02/2025 from around 15:00 to 15:30: Got chatGPT to generate front-end webpages for login and registering to be used in Flask version
