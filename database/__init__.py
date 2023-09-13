import json
import pyrebase
from config import fb_db, fb_key, fb_db_url, user_db

config = {
    "apiKey": fb_key,
    "authDomain": f"{fb_db}.firebaseapp.com",
    "databaseURL": fb_db_url,
    "storageBucket": f"{fb_db}.appspot.com"
}


class DB:
    def __init__(self, childvalue) -> None:
        self.childvalue = childvalue
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.user_db = user_db

    def createUser(self, chatid, username, small_photo_id, large_photo_id):
        data = {"chatid": chatid, "username": username,
                "lg-photo-id": large_photo_id, "sm-photo-id": small_photo_id}
        if self.CheckAvailiblity(self.user_db, 'chatid', chatid) != True:
            return self.db.child(self.user_db).push(data)

    def defult_save(self, chatid, fdata):
        return self.db.child(self.childvalue).child(f"chatid_{chatid}").push(fdata)

    def folder_save(self, chatid, fdata, dg):
        return self.db.child(self.childvalue).child(f"chatid_{chatid}").child(dg).push(fdata)

    def destroy(self):
        return self.db.child(self.childvalue).remove()

    def change(self, data):
        return self.db.child(self.childvalue).update(data)

    def Read(self):
        return json.dumps(self.db.child(self.childvalue).get().val())

    def CheckAvailiblity(self, childdb, sameValue, db_value):
        read_data = json.loads(json.dumps(self.db.child(childdb).get().val()))
        sames = []
        try:
            for i in read_data:
                data = read_data[i]
                sames.append(data[sameValue])
            if db_value in sames:
                return True
            else:
                return False
        except:
            return False
