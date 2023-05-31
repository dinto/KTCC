# Generated by Django 3.2.19 on 2023-05-31 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AUCTIONRULE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rules', models.CharField(max_length=700)),
            ],
            options={
                'verbose_name_plural': 'AUCTION RULES',
            },
        ),
        migrations.CreateModel(
            name='ImportantDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EVENT', models.CharField(max_length=700)),
                ('Start_Date', models.DateField()),
                ('Start_Time', models.CharField(blank=True, max_length=100, null=True)),
                ('End_Date', models.DateField()),
                ('End_Time', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Season_Name', models.CharField(max_length=100)),
                ('Maximum_Bid_Point', models.IntegerField()),
                ('Base_Point_For_Player', models.IntegerField()),
                ('ICON_Player_Point', models.IntegerField()),
                ('Maximum_Players_Per_Team', models.IntegerField()),
                ('Minimum_Players_Per_Team', models.IntegerField()),
                ('youtube_Link', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook_Link', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_Link', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.IntegerField()),
                ('mail_id', models.EmailField(max_length=100)),
                ('Winning_point', models.IntegerField()),
                ('NR_point', models.IntegerField()),
                ('Total_over_Per_Innings', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Season',
            },
        ),
        migrations.CreateModel(
            name='VideoLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Youtube_Link', models.CharField(max_length=700)),
                ('Title_Name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TeamInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team_Name', models.CharField(max_length=100)),
                ('Short_Name', models.CharField(max_length=100)),
                ('Manager_Name', models.CharField(max_length=100)),
                ('Manager_Phone_Number', models.IntegerField()),
                ('Owner_Name', models.CharField(max_length=100)),
                ('Owner_Phone_Number', models.IntegerField()),
                ('Team_Logo', models.ImageField(blank=True, null=True, upload_to='Team_Logo/')),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
                ('Users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Team List',
                'unique_together': {('Users', 'Season')},
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Match_Number', models.IntegerField()),
                ('Date', models.DateField(blank=True, null=True)),
                ('Time', models.CharField(blank=True, max_length=200, null=True)),
                ('Venue', models.CharField(blank=True, max_length=200, null=True)),
                ('Result', models.CharField(blank=True, max_length=200, null=True)),
                ('Team1_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Team1_Name', to='KTCC.teaminfo')),
                ('Team2_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Team2_Name', to='KTCC.teaminfo')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Match_Number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.schedule')),
                ('Winning_Team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.teaminfo')),
            ],
        ),
        migrations.CreateModel(
            name='Pool_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pool_Name', models.CharField(max_length=100)),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
                ('Team_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.teaminfo')),
            ],
            options={
                'unique_together': {('Team_Name', 'Season')},
            },
        ),
        migrations.CreateModel(
            name='PlayerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('age', models.IntegerField()),
                ('place', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('mail_id', models.EmailField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('Role', models.CharField(choices=[('Batsman', 'Batsman'), ('Bowling Allrounder', 'Bowling Allrounder'), ('Batting Allrounder', 'Batting Allrounder'), ('Wicket-Keeper', 'Wicket-Keeper'), ('Bowler', 'Bowler')], max_length=22)),
                ('Batting_style', models.CharField(choices=[('Right Handed Bat', 'Right Handed Bat'), ('Left Handed Bat', 'Left Handed Bat')], max_length=22)),
                ('Bowling_style', models.CharField(choices=[('Right-arm Fast Medium', 'Right-arm Fast Medium'), ('Left-arm Fast Medium', 'Left-arm Fast Medium'), ('Right-arm  Medium', 'Right-arm  Medium'), ('Left-arm  Medium', 'Left-arm  Medium'), ('right-arm legbreak', 'right-arm legbreak'), ('right-arm offbreak', 'right-arm offbreak'), ('Left-arm orthodox', 'Left-arm orthodox'), ('Left-arm chinaman', 'Left-arm chinaman')], max_length=22)),
                ('aadharcard_no', models.CharField(max_length=100)),
                ('aadharcard', models.FileField(upload_to='aadharcard/')),
                ('Profile_Pic', models.ImageField(blank=True, null=True, upload_to='Profile_Pic/')),
                ('is_home_ground_player', models.BooleanField(default=False)),
                ('is_icon_player', models.BooleanField(default=False)),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
            ],
            options={
                'verbose_name_plural': 'Player List',
                'unique_together': {('mail_id', 'Season')},
            },
        ),
        migrations.CreateModel(
            name='Bid_Bucket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=100)),
                ('Current_player', models.BooleanField(default=False)),
                ('Player_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.playerinfo')),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
            ],
            options={
                'verbose_name_plural': 'Bid Bucket',
            },
        ),
        migrations.CreateModel(
            name='Unsold_player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=100)),
                ('Player_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.playerinfo')),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
            ],
            options={
                'unique_together': {('Player_name', 'Season')},
            },
        ),
        migrations.CreateModel(
            name='PointTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Match', models.IntegerField()),
                ('Win_count', models.IntegerField()),
                ('Lose_count', models.IntegerField()),
                ('NR_count', models.IntegerField()),
                ('Points', models.IntegerField()),
                ('NRR', models.CharField(blank=True, max_length=200, null=True)),
                ('Pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.pool_master')),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
                ('Team_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.teaminfo')),
            ],
            options={
                'verbose_name_plural': 'Point Table',
                'unique_together': {('Team_Name', 'Season', 'Pool')},
            },
        ),
        migrations.CreateModel(
            name='CurrentBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Current_Bid_Point', models.IntegerField()),
                ('Player_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.playerinfo')),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
                ('Team_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.teaminfo')),
            ],
            options={
                'unique_together': {('Player_name', 'Season')},
            },
        ),
        migrations.CreateModel(
            name='Bid_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=100)),
                ('Sold_Point', models.IntegerField(blank=True, null=True)),
                ('Player_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.playerinfo')),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
                ('Team_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.teaminfo')),
            ],
            options={
                'verbose_name_plural': 'Bid Details',
                'unique_together': {('Player_name', 'Season')},
            },
        ),
        migrations.CreateModel(
            name='Available_Point_Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Available_Point', models.IntegerField()),
                ('Season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.season')),
                ('Team_Name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTCC.teaminfo')),
            ],
            options={
                'unique_together': {('Team_Name', 'Season')},
            },
        ),
    ]
