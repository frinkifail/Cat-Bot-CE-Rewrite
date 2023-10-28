from .achivements import AchivementManager

achivements = {
    "i like pies": AchivementManager.new(
        "pi catch", "external", description="catch a cat in 3.14 seconds"
    ),
    "skull emoji": AchivementManager.new(
        "skull", "exact", phrase="💀", description="SKULL EMOJIII"
    ),
}
