import sys
import copy

from manapotion import content
from manapotion import user

User = user.User

urls = [["https://www.bluetooth.com/news/pressreleases/2016/12/07/bluetooth-5-now-available",
        "http://www.businessinsider.com/amazon-payments-way-ahead-of-apple-and-google-2016-12",
        "http://specialreports.dailydot.com/how-to-destroy-an-american-family"],
        ["http://www.governing.com/topics/public-justice-safety/courts-corrections/mississippi-correction-reform.html",
        "https://www.theguardian.com/world/2015/jan/14/-sp-roberto-saviano-my-life-under-armed-guard-gomorrah?CMP=twt_gu",
        "http://www.nybooks.com/articles/archives/2010/feb/11/the-chess-master-and-the-computer/?pagination=false"],
        ["http://www.nytimes.com/2010/06/20/magazine/20Computer-t.html?pagewanted=all",
        "http://www.guardian.co.uk/theobserver/2010/mar/21/tom-bissell-video-game-cocaine-addiction",
        "http://www.thestranger.com/seattle/Content?oid=4683741&mode=print"],
        ["http://www.ediblegeography.com/a-cocktail-party-in-the-street-an-interview-with-alan-stillman/",
        "http://www.slate.com/id/2277301/pagenum/all/#p2",
        "http://www.thenation.com/article/155400/postcard-palestine"],
        ["http://online.wsj.com/article/SB10001424052748704779704575553943328901802.html",
        "http://www.guardian.co.uk/society/2010/may/09/alcoholism-health-doctor-addiction-drug/print",
        "http://www.texasobserver.org/dateline/he-who-casts-the-first-stone"]]

rounds = 5
urls_per_round = 3


class Participant:
    def __init__(self):
        self.url_ranks = []
        self.users = []

    def __repr__(self):
        return '(' + repr(self.url_ranks) + ', ' + repr(self.users) + ')'

    def fill_users(self):
        global rounds
        global urls_per_round
        global urls
        mutable_user = [User(0)]
        for i in range(rounds):
            if i > 0:
                self.users.append(copy.deepcopy(mutable_user[0]))
            min_index = min(range(urls_per_round), key=self.url_ranks[i].__getitem__)
            mutable_user[0].update_stats(content.get_stats(urls[i][min_index]))


def get_rankings(filename):
    global rounds
    global urls_per_round
    participants = []
    mFile = open(filename)
    line = mFile.readline()
    while line:
        line = line[:-1]
        line_split = line.split(',')
        if len(line_split) < 2:
            continue
        participant = Participant()
        count = 0
        for i in range(rounds):
            participant.url_ranks.append([])
            for j in range(urls_per_round):
                participant.url_ranks[i].append(int(line_split[count]))
                count += 1
        participants.append(participant)
        line = mFile.readline()
    return participants


def get_participants(filename):
    participants = get_rankings(filename)
    for participant in participants:
        participant.fill_users()
    return participants


# for now gets the overall accuracy and the accuracy by round of the system
def evaluate_model(participants):
    global rounds
    global urls_per_round
    global urls
    round_correct = [0 for x in range(1, rounds)]
    round_total = [0 for x in range(1, rounds)]
    total = 0
    correct = 0
    for participant in participants:
        for i in range(1, rounds):
            predicted_url = content.get_top_urls(urls[i], participant.users[i - 1], 1)[0]
            predicted_index = urls[i].index(predicted_url[1])
            if participant.url_ranks[i][predicted_index] == 1:
                round_correct[i - 1] += 1
                correct += 1
            round_total[i - 1] += 1
            total += 1
    total_accuracy = float(correct) / float(total)
    round_accuracies = [float(round_correct[i]) / float(round_total[i]) for i in range(len(round_correct))]
    print(repr(total_accuracy))
    print(repr(round_accuracies))
    return total_accuracy, round_accuracies


def main():
    if len(sys.argv) != 2:
        print("incorrect usage")
        quit()

    participants = get_participants(sys.argv[1])
    evaluate_model(participants)

main()