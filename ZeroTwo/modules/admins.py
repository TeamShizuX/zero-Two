from asyncio.queues import QueueEmpty
from ZeroTwo.config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from ZeroTwo.function.admins import set
from ZeroTwo.helpers.channelmusic import get_chat_id
from ZeroTwo.helpers.decorators import authorized_users_only, errors
from ZeroTwo.helpers.filters import command, other_filters
from ZeroTwo.services.callsmusic import callsmusic
from ZeroTwo.services.callsmusic import queues


@Client.on_message(filters.command(["reload@StreamMusic_Bot"]))
async def update_admin(client, message: Message):
    chat_id = get_chat_id(message.chat)
    set(
        chat_id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ __**Sucessfully Updated Admins List!**__")


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ __**Nothing Is Playing To Paused!**__")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("⏸ __**Paused! Use `/resume` To Resume.**__")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ __**Nothing Is Paused To Resume!**__")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("▶️ __**Resumed! Use `/pause` To Pause.**__")


@Client.on_message(command("stop") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ __**Nothing Is Streaming To Stop!**__")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹ __**Stopped & Left From Voice Chat!**__")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ __**Queue Is Empty, Just Like Your Life!**__")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"⏭ __**Skipped:**__ `{skip[0]}`\n- Now Playing: `{qeue[0][0]}`")


@Client.on_message(filters.command("admincache"))
@errors
async def admincache(client, message: Message):
    set(
        message.chat.id,
        [
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("❇️ `Admin Cache Refreshed!`")
