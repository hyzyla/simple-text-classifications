from gender_predictor import get_predictor_from_file
import csv


def predict_from_csv():

    # In this section you can change for your case
    ############################
    gp = get_predictor_from_file('female.txt', 'male.txt')
    path = 'test_joni.csv'
    row_offset = 1
    result_path = 'result_joni.csv'
    column = 0
    separator = ';'
    # End of section
    ##########################

    rows = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=separator)
        counter = 0
        for row in reader:
            if counter < row_offset:
                counter += 1
                continue

            name = row[column]
            gender = gp.get_gender(name, use_predictor=True)
            new_row = row + [gender]
            rows.append(new_row)

    with open(result_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=separator)
        writer.writerows(rows)


if __name__ == '__main__':
    predict_from_csv()

