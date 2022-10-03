# EmployeeDoorLogs

Employee Door Logs is a script that imports our employee Door log data from CSV file into a Python Data Frame Container. 
It then manipulates the information in the Python Data Frame(CRUD modifications) and Exports the new modified Data Frame into a new CSV file. 
Moves the new CSV file to a new folder along with moving the original CSV file to a archive folder.

Missing: Need to automate script to it runs automatically, every 12 hours.


9/7/2022 Edit: Can be rigged to auto send the new CSV file as an attachment in an email. Needs password authentication every time so this is not a perfect solution.
9/15/2022 Edit: Can be rigged to auto upload the new CSV file to a google drive without password verification. This has solution was not chooses and discarded for security purposes. 
9/26/2022 Edit: Current Build. Is rigged to move the new CSV file to a new folder. We can make the output CSV folder a shared network drive so our partner company can retreive the new CSV.

