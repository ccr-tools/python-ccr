from ccr import *
#from ccrauth import File
#from ccrauth import SQLite
from ccrauth import KWallet


if __name__ == "__main__":

    r = info("pyccr-testing")
    # print("Name         : %s" % r.Name)
    # print("Version      : %s" % r.Version)
    # print("URL          : %s" % r.URL)
    # print("License      : %s" % r.License)
    # print("Category     : %s" % r.Category)
    # print("Maintainer   : %s" % r.Maintainer)
    # print("Description  : %s" % r.Description)
    # print("OutOfDate    : %s" % r.OutOfDate)
    # print("Votes        : %s" % r.NumVotes)
    # print("Screenshot   : %s" % r.Screenshot)

    #auth = CCRAuthFile()
    #auth = CCRAuthSQLite()
    auth = KWallet()
    auth.store_auth_info("anon1", "ymous4")
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