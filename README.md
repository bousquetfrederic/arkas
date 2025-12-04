# Arkas

A browser extension which loads a blocklist to hide the comments or discussions from certain users on LET.
Also a script to convert these blocklist to a format usable by adblockers such as Adguard.

By default the extension loads my file which I publish in https://arkas.quest/post_your_invoice_number.txt
This file removes the thread posted by providers who I have seen partaking in the "post your invoice for double the spam" nonsense.
You can disable my file and/or add your own in the options of the extension.

I also publish the converted version for your adblocker in https://arkas.quest/post_your_invoice_number.blocklist.txt

# Format

- List all the users (one per line) in a filter.txt file.
- Optionally append to each name ":c" to only block comments, or ":d" to only block discussions.
- Lines starting with # are ignored.
- ???
- Profit.