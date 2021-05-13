# discord-copbot
### A discord bot to handle cop doc entries and statistics.

The cop doc holds info on who has helped cop a pair of trainers for another in the discord server.

### Prereqs:
discord-copbot assumes PostgreSQL usage.

#### Usage:

*All commands are cleared programatically once executed*

- **`>copped "Name of shoe" @helper @helpee`**
    - Inserts a new entry to the cop doc table with the shoe name, helper discord userId, helpee discord userId and an entryId.
    - Returns a message showing the above information

- **`>delete entryId`**
    - Deletes an entry in the cop doc table for a given entryId.
    - Returns a message showing the entry has been deleted then clears the message after 3 seconds.
    
- **`>copstats @user`**
    - Returns cop doc statistics for given discord userId including amount of cops sent, amount of cops receives and a ratio of both.
    
- **`>copboard`**
    - Returns a message showing the cop doc leaderboard (per user per sent cops).