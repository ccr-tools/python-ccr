from ccr import *
from ccrauth import AuthFile
from ccrauth import AuthDB
from ccrauth import AuthKWallet
import os


if __name__ == "__main__":

    #auth = AuthFile()
    auth = AuthDB()
    auth.CCR_DB = os.path.expanduser('~') + "/.config/ccr-tools/ccr.db"
    #auth = AuthKWallet()
    #auth.store_auth_info("an0n", "ym0us")
    auth.delete_auth_info()
    #session = Session(auth.username, auth.password)

    #print(session.check_vote("pyccr-testing"))
    #session.adopt("pyccr-testing")
    #session.disown("pyccr-testing")
    #session.flag("pyccr-testing")
    #session.unflag("pyccr-testing")
    #session.notify("pyccr-testing")
    #session.unnotify("pyccr-testing")
    #session.vote("pyccr-testing")
    #session.unvote("pyccr-testing")
    #session.submit("pyccr-testing-0.0.1-3.src.tar.gz", "devel")
    #session.setcategory("pyccr-testing", "devel")
    #session.delete("pyccr-testing")