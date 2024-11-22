## Introduction

A Discord bot designed specifically to run the [Carleton Library Booking script](https://github.com/HenryZhangxiao/Carleton-Library-Autobooking).


<br><br>
#### Table of Contents
- [Technologies Used ](#technologies)
- [Info ](#info)


<br></br>
## Technologies Used <a name="technologies"></a>
- Python3
- discord.py
- python-dotenv


<br></br>
## Info <a name="info"></a>
- This bot is essentially a [Carleton Library Booking script](https://github.com/HenryZhangxiao/Carleton-Library-Autobooking) wrapper with 24/7 uptime.
- Users can print the usage with /help and book a library room with /book
- Bot messages are abstracted for privacy using ephemeral=True in messages sent to the user
- Using asyncio locks, only 1 user can use the bot at a time (due to limited resources)
- Bot messages are deferred until ready to prevent Discord bot command timeouts


<br></br>
![image](https://github.com/user-attachments/assets/c5a7f191-f0b9-4597-bb19-d2811eaa4c1c)
