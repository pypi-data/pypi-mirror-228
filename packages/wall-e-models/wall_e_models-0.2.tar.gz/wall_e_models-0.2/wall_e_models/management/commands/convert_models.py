import json

import wget
from django.core.management import BaseCommand

from wall_e_models.models import CommandStat, BanRecord, UserPoint, Level, Reminder


class Command(BaseCommand):

    def handle(self, *args, **options):
        wget.download("https://dev.sfucsss.org/wall_e/fixtures/wall_e.json")
        model_instances = json.load(open('wall_e.json'))
        for model_instance in model_instances:
            if model_instance['model'] == 'WalleModels.banrecords':
                ban_record = BanRecord(
                    username=model_instance['fields']['username'],
                    user_id=model_instance['fields']['user_id'],
                    mod=model_instance['fields']['mod'],
                    mod_id=model_instance['fields']['mod_id'],
                    ban_date=model_instance['fields']['ban_date'],
                    reason=model_instance['fields']['reason'],
                    unban_date=model_instance['fields']['unban_date']
                )
                ban_record.save()
            elif model_instance['model'] == 'WalleModels.commandstat':
                command_stat = CommandStat(
                    epoch_time=model_instance['pk'],
                    year=model_instance['fields']['year'],
                    month=model_instance['fields']['month'],
                    day=model_instance['fields']['day'],
                    hour=model_instance['fields']['hour'],
                    channel_name=model_instance['fields']['channel_name'],
                    command=model_instance['fields']['command'],
                    invoked_with=model_instance['fields']['invoked_with'],
                    invoked_subcommand=model_instance['fields']['invoked_subcommand']
                )
                command_stat.save()
            elif model_instance['model'] == 'WalleModels.userpoint':
                user = UserPoint(
                    user_id=model_instance['fields']['user_id'],
                    points=model_instance['fields']['points'],
                    level_up_specific_points=model_instance['fields']['level_up_specific_points'],
                    message_count=model_instance['fields']['message_count'],
                    latest_time_xp_was_earned_epoch=model_instance['fields']['latest_time_xp_was_earned_epoch'],
                    level_number=model_instance['fields']['level_number'],
                    hidden=model_instance['fields']['hidden']
                )
                user.save()
            elif model_instance['model'] == 'WalleModels.level':
                lvl = Level(
                    number=model_instance['fields']['number'],
                    total_points_required=model_instance['fields']['total_points_required'],
                    xp_needed_to_level_up_to_next_level=model_instance['fields']['xp_needed_to_level_up_to_next_level'],
                    role_id=model_instance['fields']['role_id'],
                    role_name=model_instance['fields']['role_name']
                )
                lvl.save()
            elif model_instance['model'] == 'WalleModels.reminder':
                rem = Reminder(
                    reminder_date_epoch=model_instance['fields']['reminder_date_epoch'],
                    message=model_instance['fields']['message'],
                    author_id=model_instance['fields']['author_id']
                )
                rem.save()