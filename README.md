## Inspiration

The inspiration for our game comes mainly from The Binding Of Isaac and Hollow Knight, both classic action-adventure and RPG games, where exploration, combat, and character progression are at the heart of the experience. 

## What it does

Shadows of Lumina is a dungeon-crawler where players explore a labyrinch, facing enemies known as Umbrals, and a powerful boss called the Shadow Lord. Players can collect powerups to increase their health and lumina energy, which is essential for attacking. 

## How we built it

We built The Cursed Kingdom: Shadows of Lumina using Python and PyGame. The game features a room-based system where each room contains enemies, powerups, and doors leading to other areas. Sprite sheets are used for detailed character animations, and each enemy, including the boss, has custom behaviors such as wandering, chasing, and attacking. The powerup system is modular, allowing us to easily expand the player’s abilities as they progress. We also implemented background music, dynamic health and lumina systems which act as mana.

## Challenges we ran into

One of the main challenges that we ran into was sprites. When we first started trying to put together the game yesterday, we really struggled trying to figure out a way to make our game look decent. Since we only have 36 hours to code the game and integrate assets, we didn't have time to make custom sprites and backdrops for the game. After searching for a solution, we found a sprite generator which generated sprite sheets which saved us a lot of time.

## Accomplishments that we’re proud of

We are proud of how well the boss mechanics came together. The bosses ability to shoot circle projectiles, spells, and continuously chase the player adds a real sense of danger to the boss room. Since we've played games such as The Binding of Isaac, Hollow Knight, and even Touhou, we were very open to adding many projectiles in the boss room and making it a bit of a challenge. We were also proud that we figured out how to use such a large file structure in order to keep our programming organized. Usually, we have one or two files and almost all of our code jammed into a main function. But here, we separated classes into their own files and grouped each type into their own python packages for better organization.

## What we learned

Throughout the development of Shadows of Lumina, we learned a great deal about handling game state transitions, sprite-based animations, and collision detection within a 2D space. We also gained a deeper understanding of pathfinding and player feedback mechanisms. Balancing difficulty while maintaining an engaging player experience taught us the importance of iteration and playtesting. Moreover, we improved our skills in managing project files, optimizing asset loading, and creating reusable game components.

## What’s next for Shadows of Lumina

We were really ambitious at the start, wanting to add a unique light mechanic to the game which would reveal hidden paths and even use the different angling and swinging of a lantern in order to fight mobs and bosses. However, quickly we released that we had no where near enough time to even start implementing this. In the future, we hope to be able to change the combat system to reflect this and even add puzzles to the rooms. We also hope to have more than one boss in the future.


Credits: 
Spritesheets:
Authors: drjamgo@hotmail.com, bluecarrot16, Evert, TheraHedwig, MuffinElZangano, Durrani, Sander Frenken (castelonia), Benjamin K. Smith (BenCreating), Eliza Wyatt (ElizaWy), dalonedrau, Stephen Challener (Redshrike), ElizaWy, JaidynReiman, Nila122, Matthew Krohn (makrohn), Fabzy, LordNeo, Michael Whitlock (bigbeargames)

- shadow/adult/shadow.png: by drjamgo@hotmail.com. License(s): CC0. 
    - https://opengameart.org/content/shadow-for-lpc-sprite

- body/bodies/muscular/fur_black.png: by bluecarrot16, Evert, TheraHedwig, MuffinElZangano, Durrani, Sander Frenken (castelonia), Benjamin K. Smith (BenCreating), Eliza Wyatt (ElizaWy), dalonedrau, Stephen Challener (Redshrike). License(s): . see details at https://opengameart.org/content/lpc-character-bases
    - https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles
    - https://opengameart.org/content/lpc-barbarian-sprite-base
    - https://opengameart.org/content/lpc-muscular-swing-animation
    - https://opengameart.org/content/lpc-muscular-hurt-animation
    - https://opengameart.org/content/lpc-jump-expanded

- body/wings/bat/adult/fg/black.png: by ElizaWy, JaidynReiman. License(s): OGA-BY 3.0. 
    - https://opengameart.org/content/lpc-revised-ulpc-wings

- body/wings/bat/adult/bg/black.png: by ElizaWy, JaidynReiman. License(s): OGA-BY 3.0. 
    - https://opengameart.org/content/lpc-revised-ulpc-wings

OSTS:
Kingdoms Edge, Sealed Vessel, Hollow Knight Main Theme - Christopher Larkin
From Hollow Knight by Team Cherry.
