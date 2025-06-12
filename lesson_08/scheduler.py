import asyncio
from datetime import datetime, timedelta


class Scheduler:

    @staticmethod
    async def process_daily_report(hour: int, minute: int):
        while True:
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if target_time <= now:
                target_time += timedelta(days=1)

            wait_seconds = (target_time - now).total_seconds()
            await asyncio.sleep(wait_seconds)


            print("[DEBUG] Starting daily report process")
            await asyncio.create_subprocess_exec(
                'python3', '-c',
                ('from email_send import SendEmailWithDailyReport; '
                 'SendEmailWithDailyReport().send_report()'),
            )


    @staticmethod
    async def process_monthly_report(day: int, hour: int, minute: int):
        while True:

            now = datetime.now()
            try:
                target_date = now.replace(day=day, hour=hour, minute=minute, second=0, microsecond=0)
            except ValueError:
                next_month = (now.replace(day=1) + timedelta(days=31)).replace(day=1)
                target_date = next_month.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if target_date <= now:
                target_date += timedelta(days=1)

            wait_seconds = (target_date - now).total_seconds()
            await asyncio.sleep(wait_seconds)

            await asyncio.create_subprocess_exec(
                'python3', '-c',
                ('from email_send import SendEmailWithMonthlyReport; '
                 'SendEmailWithMonthlyReport().send_report()'),
            )

