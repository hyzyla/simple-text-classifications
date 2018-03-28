import pickle
try:
    import numpy as np
except ImportError:
    print("Please install numpy using following command: \n"
          "pip install numpy\n"
          "(Best practice is to do this in virtual environment)\n")
    exit(1)


class GenderNames:
    def __init__(self):
        self.female_names = None
        self.male_names = None

    @staticmethod
    def _read_from_file(path):
        """
        Function for reading names from txt file

        :param path: str
        :return: set of str
        """
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
        return set(lines)

    @staticmethod
    def _preprocess_names(names):
        # Delete any spaces between words, delete commas, semicolons and other chars from string
        # and split words with - as two different names.
        names = [line.strip().replace(',', '').replace(';', '').strip().split('-') for line in names]

        # Flatting list, because split method makes list of list
        # [[name1, name2], [name3], [name4] ... ] --> [name1, name2, name3, name4 ... ]
        names = [list(line if not isinstance(line, list) else i for i in line) for line in names]
        names = [item for sublist in names for item in sublist]

        # Use 'set' for delete duplicate
        return set(names)

    def _check_names(self):
        if self.female_names is None or self.male_names is None:
            raise AttributeError("female_names and male_names is None. "
                                 "Use load_from_files or load_from_pickle before using this method")

    def load_from_files(self, path_female='female.txt', path_male='male.txt'):
        female_names = self._read_from_file(path_female)
        male_names = self._read_from_file(path_male)

        female_names = self._preprocess_names(female_names)
        male_names = self._preprocess_names(male_names)

        # Delete common (set operations: &(intersection) and  -(difference))
        # In the feature version common set can be useful for detection unisex names
        common_set = female_names & male_names
        female_names -= common_set
        male_names -= common_set

        self.female_names = female_names
        self.male_names = male_names
        return self

    def save_to_pickle(self, path='data.pickle'):
        # If some of names is not initialised this method raise Exception
        self._check_names()

        # Save to pickle file
        with open(path, 'wb') as f:
            pickle.dump((self.female_names, self.male_names), f, protocol=pickle.HIGHEST_PROTOCOL)

        return self

    def load_from_pickle(self, path='data.pickle'):
        # Loading pickled object of female and male names
        with open(path, 'rb') as f:
            self.female_names, self.male_names = pickle.load(f)

        return self

    def get_ndarray(self):
        self._check_names()

        data = list(zip(self.female_names, 'F' * len(self.female_names)))
        data += list(list(zip(self.male_names, 'M' * len(self.male_names))))
        data = np.array(data).astype(str)
        return data

    def is_female(self, name):
        self._check_names()
        return name in self.female_names

    def is_male(self, name):
        self._check_names()
        return name in self.male_names


class GenderPredictor:
    def __init__(self, gender_names, female_label='F', male_label='M'):
        if not isinstance(gender_names, GenderNames):
            raise AttributeError("Please use instance of class GenderNames")
        self.gender_names = gender_names
        self.data = self.gender_names.get_ndarray()

        self.female_label = female_label
        self.male_label = male_label

    @staticmethod
    def _prepare_name(name):
        # Stripping word
        name = name.strip()

        # Delete any spaces
        name = ''.join(name.split())

        # Delete ending
        if name.endswith(' b') or name.endswith(' m') or name.endswith(' f'):
            name = name[:-2]

        # Split names by hyphen ex: Name-Name
        return name.split('-')

    def _get_gender_by_label(self, label):
        if label == 'M':
            return self.male_label
        if label == 'F':
            return self.female_label

    def predict_gender(self, name):
        names = self.data[:, 0]
        genders = self.data[:, 1]

        # Iterate over name length
        result_probability = np.ones([2])
        gender_unique = np.unique(genders)
        for idx, _ in enumerate(name[: -1], start=2):

            # Name ending with idx length
            name_ending = name[-idx:]

            # Function for check all names with same ending as in given name
            have_same_ending = np.vectorize(lambda s: s[-idx:] == name_ending)

            # Genders for names with the same ending as in given name
            genders_by_ending = genders[have_same_ending(names) == True]
            g, counts = np.unique(genders_by_ending, return_counts=True)

            if sum(counts) == 0:
                break

            if counts.shape == (1,):
                return g[0]

            result_probability *= counts / sum(counts)

        max_prob_idx = np.argmax(result_probability)
        return gender_unique[max_prob_idx]

    def get_gender(self, name, use_predictor=True):

        # Preparing list of name: [name1] or [name1, name2]
        names = self._prepare_name(name)

        # Iterate over each names
        for name in names:
            name = name.capitalize()
            if self.gender_names.is_female(name):
                return self._get_gender_by_label('F')
            if self.gender_names.is_male(name):
                return self._get_gender_by_label('M')

        if use_predictor:
            # when any part of names is not in name list
            predicted_label = self.predict_gender(name)
            return self._get_gender_by_label(predicted_label)


def get_predictor_from_file(path_female='female.txt', path_male='male.txt', female_label='Female', male_label='Male'):
    gn = GenderNames()
    gn = gn.load_from_files(path_female=path_female, path_male=path_male)
    return GenderPredictor(gn, female_label=female_label, male_label=male_label)


def get_predictor_from_pickle(path ='data.pickle', female_label='Female', male_label='Male'):
    gn = GenderNames()
    gn = gn.load_from_pickle(path=path)
    return GenderPredictor(gn, female_label=female_label, male_label=male_label)
