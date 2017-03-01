__author__ = 'zapping-seb'

import pylast
import os
import time
import re
import pandas as pd

def assertEqual(first, second, msg=None):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
    """
    return first == second

def get_secret_dict(secrets_file="../tests/test_pylast.yaml"):
    if os.path.isfile(secrets_file):
        import yaml  # pip install pyyaml
        with open(secrets_file, "r") as f:  # see example_test_pylast.yaml
            doc = yaml.load(f)
    else:
        doc = {}
        try:
            doc["username"] = os.environ['PYLAST_USERNAME'].strip()
            doc["password_hash"] = os.environ['PYLAST_PASSWORD_HASH'].strip()
            doc["api_key"] = os.environ['PYLAST_API_KEY'].strip()
            doc["api_secret"] = os.environ['PYLAST_API_SECRET'].strip()
        except KeyError:
            return {}
    return doc

def deparse_txt(filename="./test_list.txt", exceptions=None):
    if not exceptions:
        exceptions = ["Remix", "Reprise", "Edit"]

    flatten = lambda l: [item for sublist in l for item in sublist]

    if not os.path.isfile(filename):
        raise LookupError("File {:s} could not be found".format(filename))
    else:
        with open(filename) as file_input:
            list_of_artist_track = file_input.read().split("\n")

            for splitter in ["-","–"]:

                list_of_artist_track = flatten([file_line.split(splitter) for file_line in list_of_artist_track])


            for entry in exceptions:
                pattern = "".join(["(?:", entry, ")(\))"])
                out_pat = "".join([entry,"|)"])
                list_of_artist_track = [re.sub(pattern, out_pat, entry) for entry in list_of_artist_track]

            print(list_of_artist_track)
            print("-----")

            list_of_artist_track = flatten([re.split("(?<!\|)(\))", entry) for entry in list_of_artist_track])


            list_of_artist_track = [element for element in list_of_artist_track if element != ")"]


            list_of_artist_track = [
                [list_of_artist_track[i].strip().strip("|"),
                 "".join(list_of_artist_track[i+1].strip().split("(")[
                     0:list_of_artist_track[i+1].count("(")
                 ]).strip().replace("|","").strip(")")]
                   for i in range(0, len(list_of_artist_track)-1, 2)]

            list_of_artist_track = [var for var in list_of_artist_track if len(var)>0]
            return(pd.DataFrame(list_of_artist_track))


if __name__ == "__main__":
    doc = get_secret_dict()

    # network = pylast.LastFMNetwork(api_key=doc["api_key"],
    #                                api_secret=doc["api_secret"],
    #                                username=doc["username"],
    #                                password_hash=doc["password_hash"])
    #
    # timestamp = time.time()
    # #network.scrobble("Fettes Brot","Jein",timestamp)
    #
    # lastfm_user = network.get_user(doc["username"])
    # last_scrobble = lastfm_user.get_recent_tracks(limit=2)[0]
    #
    # print(assertEqual(str(last_scrobble.track.artist), str("Fettes Brot")))
    # print(assertEqual(str(last_scrobble.track.title), str("Jein")))
    # print(assertEqual(str(last_scrobble.timestamp), str(timestamp)))

    print(deparse_txt())