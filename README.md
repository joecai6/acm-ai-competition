# ACM AI Hide and Seek Competition

This is my bot submission that won first place in the first [ACM AI Competition Hide and Seek](https://ai.acmucsd.com/)! :trophy: :boom: 

My bot named "pizza" :pizza: has functionality for both hiding and seeking.

Here is a [blog post](https://medium.com/acmucsd/how-to-hide-from-ai-the-winner-interview-82a59aed5b0b) about my experience with the competition.
# Summary

The seeker and hider functions revolves around using A* Search Algorithm for pathfinding. There are many ideas on how to implement the seeking/hiding, but I chose the one that I am most familiar with. My code for the bot is in the bot.py file, which contains all the functions and classes used. I am currently in the process of refactoring the code so that it is more readable and organized.

# Seeker

Seeker Functionality

<img src="/demo/seeker.gif" align="left" width="300" height="384"/>

My idea for the seeker was to cover the hiding spots between walls where the seek has trouble detecting. Therefore I made the bot perform DFS on the whole map, which covers as much open edge cells as possible. The downside on this process is that the seeker might visit only one side of the map which takes a large amount of rounds away from detecting the hider. it perform this function until it can see the hider.

When it sees the hider, it performs the A* pathfinding algorithm to get the shortest path to the hider. Every time the hider moves, the seeker repeatedly uses the algorithm to find the shortest path. If the hider runs to a cell where the seeker cannot detect, the seeker moves to the last position of the hider. If it still does not see the hider, it goes back to doing DFS on the map.

<br><br>

# Hider

Hider Functionality

<img src="/demo/hider.gif" align="left" width="300" height="384"/>

I had two ideas for the hider: one was to move in the furthest direction away from the seeker and the other was to run around in circles so that the seeker has no chance of catching the hider.

If there is more than one hider, one of the hider stays until it is found and moves in the the furthest away relative to the seekers location. It continues to do that until it is caught and avoids moving to the edge of the map where it would get stuck. This method works when the hider moves to an area where it cannot me seen by the seeker. It usually gets caught after many rounds, however, it stalls for catching the other hiders.

The remaining hiders move to an island and traverse around it if found. The way I implemented this is with BFS to find the island and perform a hull algorithm used to get the path around the island. At the start of the round, the hider moves towards the island and their path is set to circle around the island. If found it moves to the opposite direction of the seeker continuously until it is caught by two seekers or the round ends.

My bot is definitely not perfect. There are many improvements to my bots such as making the DFS more efficient in rounds and finding better directions to move to for the hider.


Thanks to <br>
<img src="https://avatars3.githubusercontent.com/u/48527658?s=200&v=4s=30" align="center" width="50" height="50" />
