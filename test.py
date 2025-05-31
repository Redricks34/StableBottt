from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, ChatWriteForbiddenError, \
    InviteHashExpiredError, ChannelPrivateError, UserAlreadyParticipantError
from telethon.errors import FloodWaitError
from telethon.errors import MultiError

from telethon.tl.types import ContactStatus, UserStatusOnline, UserStatusOffline, UserStatusRecently, \
    UserStatusLastWeek, UserStatusLastMonth, UserStatusEmpty

from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import types
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon import events
import sys
import csv
import os
import subprocess
import configparser
import traceback
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
from datetime import datetime

re = "\033[1;31m"
gr = "\033[1;32m"
cy = "\033[1;36m"


def banner():


    print(f"""
{re}╔╦╗{cy}┌─┐┬ ┌─┐{re}╔═╗ ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │ ├┤ {re}║ ╦ ╚═╗{cy}│ ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝ ╚═╝{cy}└─┘┴└─┴ ┴┴ └─┘┴└─



version : 3.1
youtube.com/channel/UCnknCgg_3pVXS27ThLpw3xQ
""")

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
api_hash = cpass['cred']['hash']
phone = cpass['cred']['phone']
client = TelegramClient(phone, api_id, api_hash)
except KeyError:
os.system('clear')
banner()
print(re + "[!] run python3 setup.py first !!\n")
sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
os.system('clear')
banner()
client.sign_in(phone, input(gr + '[+] Enter the code: ' + re))

os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

print(gr + '[+] Fetching Members from all groups...')
time.sleep(1)

for target_group in chats:
    try:
    if target_group.megagroup == True:
    groups.append(target_group)
except:
continue

with open("members.csv", "w", encoding='UTF-8', newline='') as f:
    fieldnames = ['sr. no.', 'username', 'user id', 'access hash', 'name', 'group', 'group id', 'last seen']
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()

for target_group in groups:
    try:
    print(gr + '[+] Fetching Members from Group: ' + target_group.title)
all_participants = client.get_participants(target_group, aggressive=True)

print(gr + '[+] Saving Members in file...')
time.sleep(1)
6
with open("members.csv", "a", encoding='UTF-8', newline='') as f:
    writer = csv.writer(f)
i = 0
try:
    for user in all_participants:
    accept = True

try:
    lastDate = user.status.was_online
if isinstance(lastDate, int):  # Check if 'lastDate' is an integer (Unix timestamp)
    last_date_dt = datetime.fromtimestamp(lastDate)
num_months = (datetime.now() - last_date_dt).days // 30
if num_months > 1:
    accept = False
else:
accept = False
except:
continue

if accept:
    i += 1
username = user.username if user.username else ""
first_name = user.first_name if user.first_name else ""
last_name = user.last_name if user.last_name else ""
name = (first_name + ' ' + last_name).strip()
last_seen = last_date_dt.strftime("%Y-%m-%d %H:%M:%S") if accept else "N/A"

writer.writerow([i, username, user.id, user.access_hash, name, target_group.title, target_group.id, last_seen])
time.sleep(0.1)



except KeyboardInterrupt:
print(gr + "[+] Script stopped by the user.")
break
except Exception as e:
print(re + f"[-] Error occurred while scraping group {target_group.title}: {e}")
continue

print(gr + '[+] Members from Group ' + target_group.title + ' scraped successfully.')



except Exception as e:
print(re + f"[-] Error occurred while fetching members for group {target_group.title}: {e}")
continue

print(gr + '[+] All group members scraped successfully.')
