from ccr import *
#from ccrauth import AuthFile
#from ccrauth import AuthSQLite
from ccrauth import AuthKWallet


if __name__ == "__main__":

    #auth = AuthFile()
    #auth = AuthSQLite()
    auth = AuthKWallet()
    auth.store_auth_info("an0n", "ym0us")
    session = Session(auth.username, auth.password)

    #r = session.check_vote("pyccr-testing")
    #print(r)
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