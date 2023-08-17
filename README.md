# emojibotdiscord
Creates a Discord bot that allows a user to create a poll for a new custom emoji on their server and vote to add or refuse it.

Ignore main.py, I don't know why I uploaded it. Ignore WAIT_TIMES_BETWEEN_CHECKS and POLL_UPDATE_POST_TIMES in url.py as well.

To create a bot go here:
https://discord.com/developers/applications

Click on "New Application" and give your bot a name. Under OAuth2 general section, give your bot both the bot and applications.commands scopes, and set 
the appropriate permissions for your bot for it to be able to create custom emojis (I believe it is manage and/or create expressions). You can make your
bot an admin which will give it all permissions, but be careful doing this in a public server with many members. Click on Bot and turn on all intents,
make sure you copy the token since you'll need it to turn on the bot (make sure you don't share the token with anyone!). Go to OAuth2, under URL 
information click on all of the permissions you gave it before (make sure to remember them), copy the URL below and then enter it in the search bar,
then authorize your bot to join your server.
