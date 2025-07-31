from sheets import load_google_sheet
from button import ReminderView 

class Reminders(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.load_tasks()

#Read the tasks from the sheet and schedule reminders
    def load_tasks(self):
        df = load_google_sheet()
        for _, task in df.iterrows():
            due_date = task["due_date"]

            try:
                due_date = parse_due_date(str(task["due_date"]))
            except Exception as e:
                print(f"Skipping task due to invalid date: {e}")
                continue

            self.scheduler.add_job(
                self.send_reminder, 
                "date",
                run_date=due_date,
                args=[task]
            )
#send reminders to user through DM
    async def send_reminder(self, task):
        try:
            user = await self.bot.fetch_user(int(task["discord_id"]))
            await user.send(
                f"Reminder: Your task **{task['task']}** is due!",
                view=ReminderView(task)
            )
        except Exception as e:
            print(f"Failed to send reminder to {task['discord_id']}: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Reminder Cog loaded and active")

async def setup(bot: commands.Bot):
    await bot.add_cog(Reminders(bot))
