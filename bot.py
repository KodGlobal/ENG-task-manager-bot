import discord
from discord.ext import commands
from config import TOKEN

# Create an intents object for the bot so that the bot can receive messages
intents = discord.Intents.default()
intents.messages = True

# Create a bot object with the '!' prefix for commands
bot = commands.Bot(command_prefix='!', intents=intents)

# A dictionary for storing user tasks. Key - user ID, value - list of tasks
tasks = {}

# An event that is triggered when the bot is successfully launched
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Task management command
@bot.command()
async def task(ctx, action=None, *, content=None):
    # Fetching the ID of the user who called the command
    user_id = ctx.author.id
    # If the user does not have any tasks yet, create an empty task list for the user
    if user_id not in tasks:
        tasks[user_id] = []

    # Processing the task adding command
    if action == 'add':
        task_id = len(tasks[user_id]) + 1  # Generating task ID
        tasks[user_id].append({'id': task_id, 'content': content})  # Adding the task to the user's list
        await ctx.send(f'Task added: {content} (ID: {task_id})')  # Send confirmation

    # Processing the task removal command
    elif action == 'remove':
        if content and content.isdigit():  # Checking if a valid task ID is provided
            task_id = int(content)  # Converting task ID to a number
            task_list = tasks[user_id]  # Getting the user's task list
            # Searching for the task by ID
            task_to_remove = next((task for task in task_list if task['id'] == task_id), None)
            if task_to_remove:
                task_list.remove(task_to_remove)  # Removing the task from the list
                await ctx.send(f'Task with ID {task_id} removed.')  # Sending confirmation
            else:
                await ctx.send(f'Task with ID {task_id} not found.')  # Notifying if the task was not found
        else:
            await ctx.send('Please provide a valid task ID to remove.')  # Notifying about an error

    # Processing the command to display the task list
    elif action == 'list':
        task_list = tasks[user_id]  # Getting the user's task list
        if task_list:
            # Creating a response with the list of tasks
            response = "Your current tasks:\n"
            response += "\n".join([f"ID: {task['id']}, Description: {task['content']}" for task in task_list])
        else:
            response = "You have no current tasks."  # Notifying the user that there are no tasks
        await ctx.send(response)  # Send the task list

    # Processing an unknown command
    else:
        await ctx.send('Unknown action. Please use add, remove, or list.')

# A separate command to display help information
@bot.command()
async def info(ctx):
    response = (
        "Available commands:\n"
        "!task add [task description] - adds a new task.\n"
        "!task remove [task ID] - removes a task by the specified ID.\n"
        "!task list - displays the list of current tasks.\n"
        "!info - displays this help information."
    )
    await ctx.send(response)  # Send help information

# Run the bot with your token
bot.run(TOKEN)