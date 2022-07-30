# External imports
from distutils.log import error
import os
import discord
import datetime
from dotenv import load_dotenv
from pathlib import Path


# Internal imports
from constants import *
from sign_ups import parse_sign_up
from tourney_recs import parse_discord_message, parse_game_files, parse_zipped_game_files
from db import *
from discord_commands import parse_command

# Load data env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DB_USER_NAME = os.getenv('DB_USER_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Start Discord client
client = discord.Client()

# Confirm connection to server
@client.event
async def on_ready():
    print('Bot is connected to the following guilds:')
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

# Parse all messages
@client.event
async def on_message(message: discord.Message):
    await process_message(message)

@client.event
async def on_raw_message_edit(payload):
    try:
        channel = client.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
            await process_message(message)
        except discord.NotFound:
            return
    except discord.NotFound:
        return


@client.event
async def on_message_delete(message: discord.Message):
    # TODO: Need to handle message deletion to remove participant or set from DB
    return

@client.event
async def on_guild_join(guild: discord.Guild):
    # Create object
    # TODO: What if tourney name is not guild name?
    tourney_info = Tournament(guild.name, guild.name)

    # Add to DB
    success = post_tourney(DB_USER_NAME, DB_PASSWORD, tourney_info)

    # TODO: Handle failed addition?

@client.event
async def on_guild_leave(guild: discord.Guild):
    delete_guild_tourneys(DB_USER_NAME, DB_PASSWORD, guild.name)
    return

async def send_error_message(message: discord.Message, error_message: str):
    # Send error messages in DM to avoid cluterring channels
    await message.author.create_dm()
    await message.author.dm_channel.send(error_message)
    return

async def process_message(message: discord.Message):
    # We dont want bot to reply to itself
    if message.author == client.user:
        return

    # Create tourney object
    tourney_name = '' # TODO: How should I get this value? Base this off of the channel?
    tourney_info = Tournament(tourney_name, message.guild.name)

    # Get monitored channels
    monitored_channels = get_tourney_channels(DB_USER_NAME, DB_PASSWORD, tourney_info)

    # Check if message should be processed
    if message.channel.name in monitored_channels.keys():
        # Get channel type
        channel_type = monitored_channels[message.channel.name]

        # Check for discord command
        if parse_command(DB_USER_NAME, DB_PASSWORD, message):
            return

        # Check for sign up or game rec submissions
        if channel_type == 'sign_up':
            registration, error_message = parse_sign_up(message.content)
            
            if error_message:
                # Send error message
                return send_error_message(message, error_message)
            elif registration:
                # Add to DB
                success = post_participant(DB_USER_NAME, DB_PASSWORD, registration)

                if success:
                    # If successfully processed thumbs up post
                    await message.add_reaction('\U0001F44D')
                    return
                else:
                    # TODO: Handle failed addition?
                    return
        elif channel_type == 'game_rec':
            # Get valid maps from tourney info
            tourney_map_pool = get_tourney_map_pool(DB_USER_NAME, DB_PASSWORD, tourney_info)
            games_per_round = get_tourney_games_per_stage(DB_USER_NAME, DB_PASSWORD, tourney_info)

            game_set, available_maps, error_message, success = parse_discord_message(message.content, tourney_map_pool, games_per_round)

            if not success:
                # If message is likely not a rec submission
                return
            elif error_message:
                # Send error message
                return send_error_message(message, error_message)
            elif game_set:
                print('Trying: {} vs {}'.format(game_set.p1_name, game_set.p2_name))

                # Match round to number of games
                num_games = games_per_round[game_set.stage]

                # Download games files
                attachment_filenames = [attachment.filename for attachment in message.attachments]

                # Get files as a byte IO stream, better than downloading everything
                attachment_files = [await f.to_file() for f in message.attachments]

                # Determine if games were directly attached or zipped
                attachment_file_extensions = [Path(f).suffix for f in attachment_filenames]
                
                if len(attachment_file_extensions) == 1 and all([f == '.zip' for f in attachment_file_extensions]):
                    # Check if directory exists
                    if not os.path.exists(TEMP_DIR):
                        os.makedirs(TEMP_DIR)

                    # Download file
                    # TODO: Is there a way to do this without saving the file?
                    saved_filepath = '{}\\{}'.format(TEMP_DIR, attachment_filenames[0])
                    await message.attachments[0].save(saved_filepath)

                    # Sent to parse
                    game_set, error_message = parse_zipped_game_files(saved_filepath, game_set, available_maps, num_games)
                elif all([f == '.aoe2record' for f in attachment_file_extensions]):
                    # Parse games to confirm maps, civs and outcome
                    game_set, error_message = parse_game_files(attachment_filenames, attachment_files, game_set, available_maps, num_games)
                else:
                    error_message = 'The recently submitted set does not have the correct number of recorded games (attachements). We are expecting 1 zipped file (.zip) or a set of {} recs (.aoe2record). Discord does not allow editing of attachments so please delete post and resubmit. Thank you'.format(num_games)

                # Send error message
                if error_message is not None:
                    return send_error_message(message, error_message)

                # Add to DB
                success = post_set(DB_USER_NAME, DB_PASSWORD, game_set)

                if success:
                    # If successfully processed thumbs up post
                    await message.add_reaction('\U0001F44D')

                    # Write to summary output channel
                    summary_channel_name = get_tourney_summary_channel(DB_USER_NAME, DB_PASSWORD, tourney_info)
                    await update_summary_message(game_set, tourney_info, summary_channel_name, message.channel.name)

                    print('Logged: {} vs {}'.format(game_set.p1_name, game_set.p2_name))
                else:
                    # TODO: Handle failed addition?
                    return

    return
 
async def update_summary_message(new_rec: GameSet, tourney_info: Tournament, summary_channel_name: str, group_name: str):
    # Find last message sent by bot
    guild = discord.utils.find(lambda g: g.name == tourney_info.guild_name, client.guilds)
    channel = discord.utils.find(lambda g: g.name == summary_channel_name, guild.channels)
    messages = await channel.history(limit=500).flatten()
    last_message = None
    for m in messages:
        if m.author.name == client.user.name:
            last_message = m
            break
    
    # Check date
    created_date = None
    if last_message is not None:
        created_date = str(last_message.created_at.date())
    todays_date = str(datetime.date.today())

    # Identify whether new message needs to be created
    create_new_message = True
    if created_date is not None and created_date == todays_date:
        create_new_message =  False

    # Create new or update message
    spacer = '{}'.format(''.ljust(SUMMARY_WIDTH,'-'))
    if create_new_message:
        # Create summary message
        summary_message = 'Daily Rec Summary for {}\n'.format(todays_date)
        summary_message += '{}\n'.format(spacer)
        summary_message += '{}\n'.format(group_name)
        summary_message += '{}\n'.format(spacer)
        summary_message += '{}\n'.format(new_rec.to_string())
        summary_message += '{}\n'.format(spacer)

        # Send message
        await channel.send(summary_message)
    else:
        # Update summary message
        new_summary_content = last_message.content
        summary_lines = last_message.content.split('\n')
        new_rec_summary = new_rec.to_string()

        # Do not want to repeat entries
        if new_rec_summary in new_summary_content:
            return

        # Check if group already exists
        if group_name in new_summary_content:
            group_line_index = summary_lines.index(group_name)
            summary_lines.insert(group_line_index+2, new_rec_summary)
        else:
            summary_lines.append(group_name)
            summary_lines.append(spacer)
            summary_lines.append(new_rec_summary)
            summary_lines.append(spacer)
        new_summary_content = '\n'.join(summary_lines)

        # Accomodate max
        if len(new_summary_content) > 2000:
            # Create summary message
            summary_message = 'Addl Daily Rec Summary for {}\n'.format(todays_date)
            summary_message += '{}\n'.format(spacer)
            summary_message += '{}\n'.format(group_name)
            summary_message += '{}\n'.format(spacer)
            summary_message += '{}\n'.format(new_rec.to_string())
            summary_message += '{}\n'.format(spacer)

            # Send message
            await channel.send(summary_message)
        else:
            # Edit message
            await last_message.edit(content=new_summary_content)

client.run(TOKEN)