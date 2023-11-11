
from utils import *


class Labels_Matcher:
    def __init__(self, labels: dict[str, dict[str, list[str]]]):
        """
        Initiaize matcher ready to recognize labels

        :param labels: dictionary of labels with their branches
        """
        self.words_forest = self.prepare_labels(labels, True)

    def prepare_labels(self, labels_dict: dict[str, dict[str, list[str]]], clean_old: bool = False
                       ) -> dict[str, dict]:
        words_forest = {} if clean_old else self.words_forest
        for branch, labels in labels_dict.items():
            words_tree: dict[str, any] = {}
            for label, label_instances in labels.items():
                for label_instance in label_instances:
                    words = lemmatize(label_instance.lower())
                    current_words_tree_node = words_tree
                    for word in words:
                        current_words_tree_node = current_words_tree_node.setdefault(word, {})
                    current_words_tree_node['_label_id'] = label
            words_forest[branch] = words_tree
        return words_forest

    def match(self, text: str, branches: list[str], return_word_position: bool = False
              ) -> dict[str, list[str | tuple[str, int, int]]]:
        words = lemmatize(text.lower())
        all_labels = {}
        for branch in branches:
            words_tree = self.words_forest[branch]
            labels = []
            i = -1
            while (i := i + 1) < len(words):
                current_node = words_tree
                depth = -1
                candidate = None
                for next_word in words[i:]:
                    if next_word in current_node:
                        current_node = current_node[next_word]
                        depth += 1
                    elif candidate is not None:
                        if return_word_position:
                            labels.append((candidate[0], i, i + depth + 1))
                        else:
                            labels.append(candidate[0])
                        i += depth
                        candidate = None
                        break
                    else:
                        break
                    if '_label_id' in current_node:
                        candidate = (current_node['_label_id'], depth)
                if candidate is not None:
                    if return_word_position:
                        labels.append((candidate[0], i, i + depth + 1))
                    else:
                        labels.append(candidate[0])
                    i += depth
            all_labels[branch] = labels
        return all_labels
