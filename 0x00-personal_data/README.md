# 0x00. Personal data

In the context of computer science, it's crucial to protect PII to maintain privacy and prevent identity theft. One way to do this is by filtering logs. Logs often contain a wealth of information about system usage, including potentially sensitive data. By setting up filters, you can exclude PII from these logs.
For example, you might set up a filter to automatically remove or obfuscate certain types of information, like email addresses or IP addresses, from your logs. This can be done using regular expressions or other pattern-matching techniques.
Remember, it's not just about removing this information from visible logs - you also need to ensure it's not being stored in any backups or archives.
It's also important to consider the principle of least privilege - only collect and store the minimum amount of personal data necessary for your application to function. This reduces the potential damage in the event of a data breach.

## Tasks/Files


|    Tasks       |     Files                     |
|----------------|-------------------------------|
|0. Regex-ing|``filtered_logger.py``|
|1. Log formatter|``filtered_logger.py``|
|2. Create logger|``filtered_logger.py``|
|3. Connect to secure database|`filtered_logger.py`|
|4. Read and filter data|`filtered_logger.py`|
|5. Encrypting passwords|``encrypt_password.py``|
|6. Check valid password|``encrypt_password.py``|
