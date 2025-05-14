from trie import Trie

class Search():

    def __init__(self):
        self.trie = Trie()

    def form_trie(self, statuses):
        for status_id in statuses:
            status_message = statuses[status_id]["status_message"]
            status_message_words = status_message.split(" ")
            for word in status_message_words:
                self.trie.insert(word.lower(), status_id)

    def search_one_word(self, word, statuses_rates, statuses):
        status_ids_weight = {}
        query_results = self.trie.query(word)
        if len(query_results) == 0:
            return None
        else:
            for result in query_results:
                query_word = result[0]
                if query_word == word:
                    status_ids = result[2]
                    for status_id in status_ids:
                        word_occurrence_number = statuses[status_id]["status_message"].count(word)
                        weight = word_occurrence_number + statuses_rates[status_id] * 0.3
                        status_ids_weight[status_id] = weight
                    break
            else:
                return None
            status_ids_weight_sorted = dict(sorted(status_ids_weight.items(), key=lambda item: item[1], reverse=True))
            return status_ids_weight_sorted
        
    def search_multiple_words(self, words, statuses_rate, statuses):
        status_ids_weight = {}
        common_status_ids = None
        
        for word in words:
            query_results = self.trie.query(word)
            word_status_ids = set()
            for result in query_results:
                if result[0] == word:
                    word_status_ids.update(result[2])

            if common_status_ids is None:
                common_status_ids = word_status_ids
            else:
                common_status_ids.intersection_update(word_status_ids)
                
        if common_status_ids is None or len(common_status_ids) == 0:
            return None
        
        common_status_ids_filtered = set()
        for status_id in common_status_ids:
            found_all_words = True
            for word in words:
                query_results = self.trie.query(word)
                found_word = False
                for result in query_results:
                    if result[0] == word and status_id in result[2]:
                        found_word = True
                        break
                if not found_word:
                    found_all_words = False
                    break
            if found_all_words:
                common_status_ids_filtered.add(status_id)
                
        if len(common_status_ids_filtered) == 0:
            return None

        for status_id in common_status_ids_filtered:
            weight = 0
            for word in words:
                query_results = self.trie.query(word)
                for result in query_results:
                    if result[0] == word and status_id in result[2]:
                        weight += statuses[status_id]["status_message"].count(word)
            weight += statuses_rate[status_id] * 0.3
            status_ids_weight[status_id] = weight

        status_ids_weight_sorted = dict(sorted(status_ids_weight.items(), key=lambda item: item[1], reverse=True))
        return status_ids_weight_sorted
    
    def autocomplete(self, word, statuses_rates, statuses):
        query_results = self.trie.query(word)
        if len(query_results) == 0:
            return None
        menu = {}
        counter = 1
        for result in query_results:
            menu[str(counter)] = result[0]
            counter += 1
        for key in menu:
            print(key + ". " + menu[key])
        while True:
            option = input("Choose option: ").strip().lower()
            if option in menu:
                break
        word_to_search = menu[option]
        status_ids_weight_sorted = self.search_one_word(word_to_search, statuses_rates, statuses)
        return status_ids_weight_sorted

    def search_phrase(self, phrase, statuses_rates, statuses):
        status_ids_weight = {}
        for status_id in statuses_rates:
            if phrase in statuses[status_id]["status_message"].lower():
                status_ids_weight[status_id] = statuses_rates[status_id]
        
        status_ids_weight_sorted = dict(sorted(status_ids_weight.items(), key=lambda item: item[1], reverse=True))
        return status_ids_weight_sorted

