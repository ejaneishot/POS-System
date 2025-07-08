
import os
import pickle
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pos.db.database import get_session
from pos.db.models import LogSinkronisasi

DB_FILE = "data/pos.sqlite3"
BACKUP_FOLDER = "backups"

def log_sync(status, message):
    session = get_session()
    log = LogSinkronisasi(sync_time=datetime.datetime.utcnow(), status=status, message=message)
    session.add(log)
    session.commit()

def authenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def manual_backup():
    try:
        if not os.path.exists(DB_FILE):
            log_sync("gagal", "File database tidak ditemukan.")
            return False
        drive = authenticate()
        with open(DB_FILE, "rb") as f:
            file_drive = drive.CreateFile({"title": f"backup_{datetime.datetime.now().isoformat()}.sqlite3"})
            file_drive.SetContentFile(DB_FILE)
            file_drive.Upload()
        log_sync("berhasil", "Backup manual berhasil diunggah.")
        return True
    except Exception as e:
        log_sync("gagal", str(e))
        return False

def manual_restore(file_title):
    try:
        drive = authenticate()
        file_list = drive.ListFile({'q': "title = '{}'".format(file_title)}).GetList()
        if not file_list:
            log_sync("gagal", "File tidak ditemukan di Google Drive.")
            return False
        file_drive = file_list[0]
        file_drive.GetContentFile(DB_FILE)
        log_sync("berhasil", "Restore berhasil dari file " + file_title)
        return True
    except Exception as e:
        log_sync("gagal", str(e))
        return False
