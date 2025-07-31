import discord
import asyncio
from datetime import datetime
from sheets import update_status, update_due_date

class ReminderView(discord.ui.View):
    """This class contains all the UI for the chatbot"""
    def __init__(self, task):
        super().__init__(timeout=None)
        self.task = task

    #The first button: task finished
    @discord.ui.button(label="Done", style=discord.ButtonStyle.success)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Thanks, task marked as done!")
        update_status(self.task["discord_id"], self.task["task"], "Done")

    #The second button: new due date
    @discord.ui.button(label="New Due Date", style=discord.ButtonStyle.secondary)
    async def reschedule(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Enter the new due date (YYYY-MM-DD HH:MM):")
        
        #Wait for the user to respond and update the sheet
        def check(m): return m.author.id == interaction.user.id
        try:
            msg = await interaction.client.wait_for("message", check=check, timeout=180)
            # Validate the format of the dates
            new_due_date = datetime.strptime(msg.content.strip(), "%Y-%m-%d %H:%M")
            # Update Google Sheet
            update_due_date(self.task["discord_id"], self.task["task"], msg.content.strip())
            #tells the user if new due date is updated succesfully
            await interaction.followup.send(f"Thanks, due date updated to {msg.content.strip()}")
        except asyncio.TimeoutError:
            await interaction.followup.send(" Sorry, you didn’t respond in time.")
        except ValueError:
            await interaction.followup.send("Sorry, invalid date format. Please follow the format YYYY-MM-DD HH:MM.")