<h1>Welcome To The Distant Realms Framework/Engine-thingy</h1>
<p>In order to handle game events, each event can be thought of as a new state in a tree of states. A child state. Think of Choose Your Own Adventure novels. Each choice influences the path you take. That's down to the application level, and frankly, I think, central to a decent RPG engine.</p>

<p>I've improved a lot of the handling of the framework with this update. Put centralized input handling onto game event handler. Redid all the state handling, and centralized all states to the core/state directory and each layer is separated. Each subdirectory contains every state manager at that layer (i.e. core/state/ApplicationLayer contains both state managers for the APPSTATE and APPMODE) of parallel state machines.</p>


<p>Streamlined the debugger's rendering loop a bit more along with showing the current track.</p>

<p>more restructuring. made a base statemanager for every other state system below the top level (appstate,appmode) to be reusable with resuable functionality. redid the logging system and modularized the fontengine</p>

<p>test for kotorized branch</p>

<p>Added ray caster game with functionality as a test. It works you can just put your Pygame games directly into the game directory, tie it into the Game class, and then put all your main loop code in the Game.draw() method under where APPSTATE is IN_GAME and voila. It should work as long as you pass the in built render calls to it.</p>

<p>This will be an excellent starting point for the KOTOR clone or rather just some RPG I'll try to hack together.</p>

<p>UPDATE</p>

<p>Went ahead and fully integrated the player and map classes from the raycaster directly into the framework
and isolated the raycaster. All input management for the player's movement and actions are handled by the player's update method. A bit messy in my opinion, but it does keep the player input isolated from the application input.</p>
<p>Added state machines for player logic</p>

<p>Added a config file just for the window title, but i'm sure it'll get more uses</p>

<p>Added the player movestate and turnstate into the debug overlay.</p>

<p>Going to begin working on the map editor soon and the map class to better integrate custom maps. This will be simple at first, allowing you to create a map of a pre-determined size. I'll need to re-work the raycaster to account for it as well, but it's turning into an actual engine now.</p>

<p><b>Major Updates:</b></p>
<p>changed the way maps are handled. they now use wall types and floor types designated by the letters F or W alongside a number</p>
<p>each map tile can have an action if you choose, also a color. textures are a future idea</p>
<p>updated the collision handling on the player object</p>
<p>The tile system is now ready for the map creator/editor. I'll be working in some entities now</p>
<p>after i've worked in some items and some enemies and npcs, i'll start focusing on simple combat mechanics</p>
<p>Once it's flexible enough, I'll start reworking the raycaster system to handle a camera and dynamic map sizes</p>
<p>Only following that will I impliment the map creator. This will allow the player to create a lot of types of games just with the base mechanics
of the raycaster engine, and entity system</p>

<p>In other words, it's finally starting to shape into an enigne from just a robust framework</p>

<p>added sprinting, experimenting with gun sprites. The sprite that's there is a dummy for now and doesn't look right yet. I just don't
want to work on it more for this commit. regardless, eventually i'm going to need to figure out how to add enemies, and make the gun shoot.
The latter, I can probably do easily, but the former? oof not there yet, but soon</p>


<p>Made the raycaster library isolated in its own directory with its own game class so you can just edit it from that location.</p>
<p>Any changes there will not have any effect on the greater shell of the application. I will modularize it to let you create the game.</p>
<p>I want to make it so when you start the program, it prompts you to create a game with a type upon first start up. Then once you have at least a single saved project, it will ask you if you want to start a new one or load a saved project.</p>
<p>Eventually this entire thing will be an actual game engine where eventually you'll be able to export an executable. I'll have to work out how that works, but I think pyinstaller would be a good method unless I can make a custom packaging system. That way we can get the most efficient and quickest binaries.</p>
<p>At this point, I think i'm safe to integrate this into the engine base branch. The kotor thing was a dumb idea, but i've just built the engine up more. I have made several improvements on the SnowBlitzBeta branch of <b>rugerclaus/DistantRealmsPython</b> and will be integrating the core engine improvements into the main branch.</p>
<p>Those changes will not be able to be directly merged, and frankly I should start a whole new repo for Snow Blitz Beta. But the changes I made were very important.</p>