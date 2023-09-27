from .achivements import Achivement, AchivementManager

achivements = {
    "testing": AchivementManager.new(
        "exact", phrase="devtest", description='Say "devtest"'
    ),
    "testing episode 2": AchivementManager.new(
        "includes", phrase="cat", description='Have a "cat" in your message.'
    ),
    "testing episode 3": AchivementManager.new(
        "exact", phrase="this is a very hidden message", hidden=True
    ),
}
