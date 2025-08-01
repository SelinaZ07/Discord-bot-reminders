import discord
from discord.ext import commands
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from sheets import load_google_sheet, parse_due_date
from button import ReminderView 


class Reminders(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.load_tasks()

    # Load all tasks from the Google Sheet and schedule reminders
    def load_tasks(self):
        df = load_google_sheet()
        for _, task in df.iterrows():
            due_date = str(task["due_date"])

            try:
                parsed_date = parse_due_date(due_date)
            except Exception as e:
                print(f"Skipping task due to invalid date: {e}")
                continue

            self.scheduler.add_job(
                self.send_reminder,
                "date",
                run_date=parsed_date,
                args=[task]
            )

    # Send reminders to users through DM
    async def send_reminder(self, task):
        try:
            user = await self.bot.fetch_user(int(task["discord_id"]))
            await user.send(
                f"Reminder: Your task **{task['task']}** is due!",
                view=ReminderView(task) 
            )
        except Exception as e:
            print(f"Failed to send reminder to {task['discord_id']}: {e}")

    # Reminder command for admins only
    @app_commands.command(name="reminders", description="List all the upcoming task deadlines for an admin.")
    async def reminders(self, interaction: discord.Interaction):
        """Admins can view their own upcoming reminders."""

        # Check if the user has admin permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Sorry, this command is restricted to administrators only.",
                ephemeral=True
            )
            return

        # Load reminders from Google Sheet for the admin who clicked on the command
        df = load_google_sheet()
        user_tasks = df[df["discord_id"] == str(interaction.user.id)]

        if user_tasks.empty:
            await interaction.response.send_message(
                "You don't have any reminders scheduled.",
                ephemeral=True
            )
            return

        # Build an embeding to send to the user
        embed = discord.Embed(
            title=f"Your Reminders",
            color=discord.Color.green()
        )
        for _, task in user_tasks.iterrows():
            embed.add_field(
                name=task["task"],
                value=f"Due: {task['due_date']} | Status: {task['status']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Reminder Cog loaded and active")


async def setup(bot: commands.Bot):
    await bot.add_cog(Reminders(bot))
