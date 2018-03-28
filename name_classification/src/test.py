from gender_predictor import GenderNames, GenderPredictor, get_predictor_from_file, get_predictor_from_pickle

if __name__ == '__main__':

    # Example 1 how use it
    print("Example 1 Sami:")
    gn = GenderNames()
    gn = gn.load_from_files(path_female='data/female.txt', path_male='data/male.txt')
    gp = GenderPredictor(gn, female_label='Female', male_label='Male')
    print(gp.get_gender('Sami'))
    print()

    print("Example 2 Pekka:")
    gn = GenderNames()
    gn = gn.load_from_files(path_female='data/female.txt', path_male='data/male.txt')
    gp = GenderPredictor(gn, female_label='Female', male_label='Male')
    print(gp.get_gender('Pekka'))
    print()

