from parse_files import adjust_date_time
from graph_edge_rank import login, load_graph, load_data, update_graph

def print_menu():
    print("\033c")
    print("-"*35)
    print("1. Log in")
    print("2. Update graph with test data")
    print("3. Exit")
    print("-"*35)

menu1 = {
    "1": login,
    "2": update_graph,
    "3": exit
}

if __name__ == '__main__':
    load_data()
    load_graph()
    print_menu()
    while True:
        option = input(">> ").lower().strip()
        while option not in menu1:
            option = input(">> ").lower().strip()
        menu1[option]()