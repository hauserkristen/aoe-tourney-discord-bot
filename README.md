Goals of the Bot:
- Verifies games and outcomes
- Writes a summary of new verified games in one channel every day
- Keeps an updated summary of stats by bracket/map/civ in another channel

Open items to work on, generally listed in order of importance:
- Migrate to DB storage for configuration and stats
    - Moving to MongoDB hosted on Google
    - Need to figure out how to configure tourney settings
        - map pool
        - define games per stage (Bo3, Bo5, etc)
        - specify channels for:
            - rec channels
            - sign up channel
            - maintenance output channel
            -  (Potential) stats channel
- How to accomodate TG format for sets/participant
- How to accomodate multiple tourneys in a single discord
- Improved logging of errors and when they occur
- How to allow admin win reporting?
- Accomodate CM for map drafting
- Accomodate non-CM for civ drafting (what if hidden civ no repeat, or just global bans)
- Switched to "stage" notation since it could have a group stage before main event?

Notes for Users:
- Use in game name for the score.
- The spoiler tag character '|' is a heavily used parsing symbol, if their IGN uses '|' please have them omit it. Our name matching should still match them correctly to the name in the rec. 
- General format:  
    paradox303 || 3 : 0 || Stealth_R_Us  
    Stage: Round of 32  
    Civ Draft: https://aoe2cm.net/draft/sRnmN  
    paradox HM: Golden Hill, Houseboat  
    Stealth_R_Us HM: Mired, Compass  
- Attached games must be labeled, must have '{p1}_vs_{p2}_g1.aoe2record' or '{p1}_vs_{p2}_G1.aoe2record' and so on for the various games in the title. 
- Games that needed to be restored, please label as '{p1}_vs_{p2}_G1a.aoe2record' and '{p1}_vs_{p2}_G1b.aoe2record' and so on.
- Reporting must be completed in 1 message and the recs must be attached to that single message. If recs are too large, attach a zip files with the recs properly named
- If errors are made, they can just edit that original message and the bot will try to revalidate it. 
