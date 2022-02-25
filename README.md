Goals of the bot after discussion with Paradox:
- Verifies games and outcomes
- Writes a summary of new verified games in one channel every day
- Keeps an updated summary of stats by division in another channel

Open items to work on, generally listed in order of importance:
- Migrate to DB storage for configuration and stats
    - Moving to MongoDB hosted on Google
- How to accomodate TG format for sets/participant
- How to accomodate multiple tourneys in a single discord
- Generate stats data for public channel instead of through my DMs
- Improved logging of errors and when they occur
- How to store token so its safe from git? Just ignore .env file and share as needed. main.py:15
- Move most of constants and .env file to configurable parameters for use by admins of a guild only. This would allow multiple tourneys to use the bot at the same time
- How to allow admin win reporting?

Notes for Paradox:
- Please have them use in game name for the score.
- The spoiler tag character '|' is a heavily used parsing symbol, if their IGN uses '|' please have them omit it. Our name matching should still match them correctly to the name in the rec. 
- General format:  
    paradox303 || 3 : 0 || Stealth_R_Us  
    Round: Round of 32  
    Civ Draft: https://aoe2cm.net/draft/sRnmN  
    paradox HM: Golden Hill, Houseboat  
    Stealth_R_Us HM: Mired, Compass  
- Attached games must be labeled, must have '{p1}_vs_{p2}_g1.aoe2record' or '{p1}_vs_{p2}_G1.aoe2record' and so on for the various games in the title. 
- Reporting must be completed in 1 message and the recs must be attached to that single message. If errors are made, they can just edit that original message and the bot will try to revalidate it. 
