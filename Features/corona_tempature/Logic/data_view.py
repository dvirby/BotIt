from BotFramework.Activity.FormActivity.Field import PictureField, TextField, ChoiceField


class CoronaForm:
    def __init__(self):
        self.temperature = TextField(name="טמפרטורה", msg="מה הטמפרטורה שמדדת?")
        self.symptoms = TextField(name="תסמינים?", msg="האם יש לך תסמינים, אם כן אילו? (אם אין רשום אין)", value="אין")
        self.family = ChoiceField(name="בני משפחה בבידוד?", msg="האם אחד מבני המשפחה בבידוד?", options={True: 'כן', False: "לא"}, value=False)
