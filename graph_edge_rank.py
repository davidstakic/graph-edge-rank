from parse_files_2 import load_comments, load_statuses, load_shares, load_reactions, load_friends
from networkx import DiGraph
from search import Search
from datetime import datetime
from print_function import print_status
from serialization import load_graph
import math

comments = {}

test_comments = {}

statuses = {}

test_statuses = {}

shares = []

test_shares = []

reactions = []

test_reactions = []

friends = {}

statuses_rates = {}

graph = DiGraph()

search = Search()

def load_data():
    global comments
    global statuses
    global shares
    global reactions
    global friends
    comments = load_comments("dataset/original_comments.csv")
    statuses = load_statuses("dataset/original_statuses.csv")
    shares = load_shares("dataset/original_shares.csv")
    reactions = load_reactions("dataset/original_reactions.csv")
    friends = load_friends("dataset/friends.csv")

def form_graph():
    global graph
    global comments
    global statuses
    global shares
    global reactions
    global friends

    decay_factor = 0.5

    for person in friends:
        graph.add_node(person)

    for comment_id in comments:
        status_id = comments[comment_id]["status_id"]
        comment_author = comments[comment_id]["comment_author"]
        status_author = statuses[status_id]["author"]
        weight = 0.0
        if graph.has_edge(comment_author, status_author):
            edge_data = graph.get_edge_data(comment_author, status_author)
            weight = edge_data["weight"]
        elif status_author in friends[comment_author]["friends"]:
            weight = 2.0
            if graph.has_edge(status_author, comment_author) == False:
                graph.add_edge(status_author, comment_author, weight=2.0)
        # else:
        #     for friend in friends[comment_author]["friends"]:
        #         if status_author in friend["friends"]:
        #             weight = 0.5
        time_diff = (datetime.now() - datetime.strptime(comments[comment_id]["comment_published"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        weight += 1.0 * math.exp(-decay_factor * time_diff / 216000)
        graph.add_edge(comment_author, status_author, weight=weight)

    for share in shares:
        status_id = share["status_id"]
        sharer = share["sharer"]
        status_author = statuses[status_id]["author"]
        weight = 0.0
        if graph.has_edge(sharer, status_author):
            edge_data = graph.get_edge_data(sharer, status_author)
            weight = edge_data["weight"]
        elif status_author in friends[sharer]["friends"]:
            weight = 2.0
            if graph.has_edge(status_author, sharer) == False:
                graph.add_edge(status_author, sharer, weight=2.0)
        # else:
        #     for friend in friends[sharer]["friends"]:
        #         if status_author in friend["friends"]:
        #             weight = 0.5
        time_diff = (datetime.now() - datetime.strptime(share["status_shared"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        weight += 1.4 * math.exp(-decay_factor * time_diff / 216000)
        graph.add_edge(sharer, status_author, weight=weight)

    for reaction in reactions:
        status_id = reaction["status_id"]
        reactor = reaction["reactor"]
        status_author = statuses[status_id]["author"]
        weight = 0.0
        if graph.has_edge(reactor, status_author):
            edge_data = graph.get_edge_data(reactor, status_author)
            weight = edge_data["weight"]
        elif status_author in friends[reactor]["friends"]:
            weight = 2.0
            if graph.has_edge(status_author, reactor) == False:
                graph.add_edge(status_author, reactor, weight=2.0)
        # else:
        #     for friend in friends[reactor]["friends"]:
        #         if status_author in friend["friends"]:
        #             weight = 0.5
        time_diff = (datetime.now() - datetime.strptime(reaction["reacted"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        if reaction["type_of_reaction"] == "likes":
            weight += 1 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "loves":
            weight += 1.3 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "wows":
            weight += 0.8 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "sads":
            weight += 1.2 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "angrys":
            weight += 1.1 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "special":
            weight += 1.2 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "hahas":
            weight += 0.9 * math.exp(-decay_factor * time_diff / 216000)
        graph.add_edge(reactor, status_author, weight=weight)
    
    for edge in graph.edges():
        weight = graph.get_edge_data(edge[0], edge[1])["weight"]
        for friend in friends[edge[0]]["friends"]:
            if graph.has_edge(friend, edge[1]):
                friend_weight = graph.get_edge_data(friend, edge[1])["weight"]
                weight += friend_weight * 0.1
            # for friend_friend in friend[friends]:
            #     if graph.has_edge(friend_friend, edge[1]):
            #         friend_friend_weight = graph.get_edge_data(friend_friend, edge[1])["weight"]
            #         weight += friend_friend_weight * 0.1
        graph.add_edge(edge[0], edge[1], weight=weight)

    return graph

def load_test_data():
    global comments
    global test_comments
    global statuses
    global test_statuses
    global shares
    global test_shares
    global reactions
    global test_reactions
    test_comments = load_comments("dataset/test_comments.csv")
    test_statuses = load_statuses("dataset/test_statuses.csv")
    test_shares = load_shares("dataset/test_shares.csv")
    test_reactions = load_reactions("dataset/test_reactions.csv")
    comments.update(test_comments)
    statuses.update(test_statuses)
    shares.extend(test_shares)
    reactions.extend(test_reactions)

def update_graph():
    global graph
    global test_comments
    global test_statuses
    global test_shares
    global test_reactions
    global friends
    
    load_test_data()
    decay_factor = 0.5

    for comment_id in test_comments:
        status_id = test_comments[comment_id]["status_id"]
        comment_author = test_comments[comment_id]["comment_author"]
        status_author = statuses[status_id]["author"]
        weight = 0.0
        if graph.has_edge(comment_author, status_author):
            edge_data = graph.get_edge_data(comment_author, status_author)
            weight = edge_data["weight"]
        elif status_author in friends[comment_author]["friends"]:
            weight = 2.0
            if graph.has_edge(status_author, comment_author) == False:
                graph.add_edge(status_author, comment_author, weight=2.0)
        # else:
        #     for friend in friends[comment_author]["friends"]:
        #         if status_author in friend["friends"]:
        #             weight = 0.5
        time_diff = (datetime.now() - datetime.strptime(test_comments[comment_id]["comment_published"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        weight += 1.0 * math.exp(-decay_factor * time_diff / 216000)
        graph.add_edge(comment_author, status_author, weight=weight)

    for share in test_shares:
        status_id = share["status_id"]
        sharer = share["sharer"]
        status_author = statuses[status_id]["author"]
        weight = 0.0
        if graph.has_edge(sharer, status_author):
            edge_data = graph.get_edge_data(sharer, status_author)
            weight = edge_data["weight"]
        elif status_author in friends[sharer]["friends"]:
            weight = 2.0
            if graph.has_edge(status_author, sharer) == False:
                graph.add_edge(status_author, sharer, weight=2.0)
        # else:
        #     for friend in friends[sharer]["friends"]:
        #         if status_author in friend["friends"]:
        #             weight = 0.5
        time_diff = (datetime.now() - datetime.strptime(share["status_shared"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        weight += 1.4 * math.exp(-decay_factor * time_diff / 216000)
        graph.add_edge(sharer, status_author, weight=weight)

    for reaction in test_reactions:
        status_id = reaction["status_id"]
        reactor = reaction["reactor"]
        status_author = statuses[status_id]["author"]
        weight = 0.0
        if graph.has_edge(reactor, status_author):
            edge_data = graph.get_edge_data(reactor, status_author)
            weight = edge_data["weight"]
        elif status_author in friends[reactor]["friends"]:
            weight = 2.0
            if graph.has_edge(status_author, reactor) == False:
                graph.add_edge(status_author, reactor, weight=2.0)
        # else:
        #     for friend in friends[reactor]["friends"]:
        #         if status_author in friend["friends"]:
        #             weight = 0.5
        time_diff = (datetime.now() - datetime.strptime(reaction["reacted"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        if reaction["type_of_reaction"] == "likes":
            weight += 1 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "loves":
            weight += 1.3 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "wows":
            weight += 0.8 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "sads":
            weight += 1.2 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "angrys":
            weight += 1.1 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "special":
            weight += 1.2 * math.exp(-decay_factor * time_diff / 216000)
        elif reaction["type_of_reaction"] == "hahas":
            weight += 0.9 * math.exp(-decay_factor * time_diff / 216000)
        graph.add_edge(reactor, status_author, weight=weight)
    
    for edge in graph.edges():
        weight = graph.get_edge_data(edge[0], edge[1])["weight"]
        for friend in friends[edge[0]]["friends"]:
            if graph.has_edge(friend, edge[1]):
                friend_weight = graph.get_edge_data(friend, edge[1])["weight"]
                weight += friend_weight * 0.1
            # for friend_friend in friend[friends]:
            #     if graph.has_edge(friend_friend, edge[1]):
            #         friend_friend_weight = graph.get_edge_data(friend_friend, edge[1])["weight"]
            #         weight += friend_friend_weight * 0.1
        graph.add_edge(edge[0], edge[1], weight=weight)
    print("Graph has been updated.")
    return graph

def edge_rank(user):
    global statuses_rates
    global graph
    global statuses
    statuses_rates = {}
    for status_id in statuses:
        weight = 1
        if graph.has_edge(user, statuses[status_id]["author"]):
            weight = graph.get_edge_data(user, statuses[status_id]["author"])["weight"]
        time_diff = (datetime.now() - datetime.strptime(statuses[status_id]["status_published"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        status_rate = int(statuses[status_id]["num_comments"]) + int(statuses[status_id]["num_shares"]) * 1.5 + int(statuses[status_id]["num_likes"]) 
        + int(statuses[status_id]["num_loves"]) * 1.5 + int(statuses[status_id]["num_wows"]) * 0.8 + int(statuses[status_id]["num_hahas"]) * 0.9 
        + int(statuses[status_id]["num_sads"]) * 1.2 + int(statuses[status_id]["num_angrys"]) * 1.1
        total_rate = weight * status_rate * math.exp(-0.5 * time_diff / 216000)
        statuses_rates[status_id] = total_rate
    return statuses_rates

def login():
    print("\033c")
    user = input("Enter user name: ").strip()
    main_page(user)

def main_page(user):
    print("\033c")
    print("Welcome, " + user + "!\n")
    print("1. View posts")
    print("2. Search")
    print("-"*35)
    option = input(">> ").lower().strip()
    if option != "2" and option != "1":
        option = input(">> ").lower().strip()
    if option == "1":
        show_posts(user)
    elif option == "2":
        search(user)

def show_posts(user):
    global statuses_rates
    global statuses
    print("\033c")
    statuses_rates = edge_rank(user)
    statuses_rates_sorted = dict(sorted(statuses_rates.items(), key=lambda item: item[1], reverse=True))
    counter = 0
    for status_id in statuses_rates_sorted:
        if (counter == 10):
            break
        print("STATUS " + str(counter + 1))
        print_status(statuses[status_id])
        counter += 1
    print("Press any key to exit")
    print("-"*35)
    exit = input(">> ")
    main_page(user)

def search(user):
    global statuses
    statuses_rates = edge_rank(user)
    search = Search()
    search.form_trie(statuses)
    print("\033c")
    print('If you want to search for a phrase, write it inside quotation marks "".')
    print("If you want to use autocomplete, end the word with *.\n")
    search_input = input("Search: ").lower().strip()
    if search_input.startswith('"') and search_input.endswith('"'):
        status_ids_weight_sorted = search.search_phrase(search_input[1:-1], statuses_rates, statuses)
    else:
        search_input_splitted = search_input.split(" ")
        if len(search_input_splitted) == 1:
            if search_input.endswith("*"):
                status_ids_weight_sorted = search.autocomplete(search_input[:-1], statuses_rates, statuses)
            else:
                status_ids_weight_sorted = search.search_one_word(search_input_splitted[0], statuses_rates, statuses)
        else:
            status_ids_weight_sorted = search.search_multiple_words(search_input_splitted, statuses_rates, statuses)
    counter = 0
    print("\033c")
    print("Search results")
    print("-"*35)
    print("\n")
    if status_ids_weight_sorted != None:
        for status_id in status_ids_weight_sorted:
            if (counter == 10):
                break
            print("STATUS " + str(counter + 1))
            print_status(statuses[status_id])
            counter += 1
    else:
        print("There are no results.\n")
    print("Press any key to exit")
    exit = input(">> ")
    main_page(user)