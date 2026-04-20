# Internet Connection Check
The internet connection check is a small Python script that performs a constant ping on a specified IP address (currently 8.8.8.8).
In case a ping fails, it logs the number of successful pings in between. It also detects time gaps between two pings, such as those that occur when the computer goes to sleep.
Furthermore, it performs a speed check every 30 to 45 minutes.
