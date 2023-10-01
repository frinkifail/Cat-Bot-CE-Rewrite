from discord import Color, Embed, Interaction
from .utility.util import db
from .achivements import Achivement, AchivementManager
from .current_achs import achivements


async def achivement_cb(interaction: Interaction):
    msg = await interaction.send("ok workin on it", ephemeral=True)
    db.reload("achs")

    def check_lock(ach: Achivement):
        if ach["unlocked"] == True:
            if not v["hidden"]:
                unlock_str = f"Unlocked: {v['description']}"
            else:
                unlock_str = "Unlocked."
        else:
            if v["hidden"]:
                unlock_str = "Locked."
            else:
                unlock_str = f"Locked: {v['description']}"
        return unlock_str

    user = interaction.user
    if user is None:
        await interaction.send("User not found.")
        return
    embed = Embed(color=Color.brand_green(), title="Achivements")
    adb: dict[str, Achivement] = db.uget(user.id, "achs")
    for k, v in achivements.items():
        ach = adb.get(k)
        if ach is not None:
            unlock_str = check_lock(ach)
        else:
            adb[k] = AchivementManager.new(
                v["unlocked_using"],
                v["unlocked"],
                v["unlocked_by"],
                v["phrase"],
                v["description"],
                v["hidden"],
            )
            unlock_str = check_lock(adb[k])

        embed.add_field(name=k.capitalize(), value=unlock_str)
    await msg.edit("", embed=embed)
