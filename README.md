# SimplePasswordManager
I wanted a easy to use, lightweight password manager for my own use since the password manager I was using - Bitwarden, has started malfunctioning. I store the password file in an encrypted format at variious locations following the 3-2-1 redundency pattern.

# Password File Format
No \<some spaces\> NAME \<some spaces\> USERNAME \<some spaces\> PASSWORDS \<some spaces\> NOTES \<some spaces\>
  
Each password record is on a new line.
Leave enough spaces in the \<some spaces\> element to accomodate the largest length item that you think might exist in that type. 
The No column stores record numbers.

# Changes to implement
1. Add update functionality
