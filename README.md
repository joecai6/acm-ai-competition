# acm-ai-competition

This is my bot submission that won first place in the first ACM AI Competition Hide and Seek. :trophy: :boom: :blush:

[Link ](https://ai.acmucsd.com/)

My bot named "pizza" has functionality for both hiding and seeking.

Summary

The seeker and hider functions revolves around using A* Search Algorithm for pathfinding. There are many ideas on how to implement the seeking/hiding, but I chose the one that I am most familiar with. My code for the bot is in the bot.py file, which contains all the functions and classes used. I am currently in the process of refactoring the code so that it is more readable and organized.

# Seeker

Seeker Functionality

[Video of a Seeker Game Here]

My idea for the seeker was to cover the hiding spots which are the edges of the map and between walls where the seek has trouble detecting. Therefore I made the bot perform DFS on the whole map, which covers as much open edge cells as possible. The downside on this process is that the seeker might visit only one side of the map which takes a large amount of rounds away from detecting the hider. it perform this function until it can see the hider.

When it sees the hider, it performs the A* pathfinding algorithm to get the shortest path to the hider. Every time the hider moves, the seeker repeatedly uses the algorithm to find the shortest path. If the hider runs to a cell where the seeker cannot detect, the seeker moves to the last position of the hider. If it still does not see the hider, it goes back to doing DFS on the map.

# Hider

Hider Functionality

[Video of Hider]

I had two ideas for the hider: one was to move in the furthest direction away from the seeker and the other was to run around in circles so that the seeker has no chance of catching the hider.


My bot is definitely not perfect. There are many improvements to my bots such as making the DFS more efficient in rounds and finding better directions to move to for the hider.

:kissing_cat:
:flushed: :flushed: :flushed::flushed::flushed::flushed::flushed:

