from functions import *

# Your parameters
#########

# File with product that you need to classify
NOT_CLASSIFIED_XLSX = 'products_to_classify_yevhenii.xlsx'
NOT_CLASSIFIED_SHEET = "Sheet1"
NOT_CLASSIFIED_PRODUCT_COLUMN='A'
NOT_CLASSIFIED_CATEGORY_COLUMN='last'
NOT_CLASSIFIED_ROW_OFFSET = 1

# File with examples of classfied products
EXAMPLES_XLSX = 'manual_all products_030917.xlsx'
EXAMPLES_SHEET = "Sheet1"
EXAMPLES_PRODUCT_COLUMN='A'
EXAMPLES_CATEGORY_COLUMN='B'
EXAMPLES_ROW_OFFSET = 1
WRITE_PREDICTED_PRODUCT = True

###########

def main_function():

    # reading file that we need to classify
    async_print('READING {}'.format(NOT_CLASSIFIED_XLSX))
    notclassified = read_notclassified(NOT_CLASSIFIED_XLSX, 
        sheet=NOT_CLASSIFIED_SHEET, 
        product_column=NOT_CLASSIFIED_PRODUCT_COLUMN, 
        offset=NOT_CLASSIFIED_ROW_OFFSET)
    async_print()

    # correcting decoding errors
    notclassified = correct_decoding(notclassified)

    # reading file that has classified examples
    async_print('READING {}'.format(EXAMPLES_XLSX))
    examples = read_examples(EXAMPLES_XLSX, 
        sheet=EXAMPLES_SHEET, 
        product_column=EXAMPLES_PRODUCT_COLUMN, 
        category_column=EXAMPLES_CATEGORY_COLUMN, 
        offset=EXAMPLES_ROW_OFFSET)
    async_print()

    # Deleting from examples all non Finnish symbols
    cleaned_prodcuts = cleaner_vect(examples[:, 0])

    # Training predictive model
    async_print('TRAINING PREDICTIVE MODEL') 
    model = get_model(examples)
    async_print()

    # Iterating over products
    result = []
    predicted_product = []

    async_print('ITERATING OVER PRODUCTS')
    for i, product in enumerate(notclassified):
        
        # Printing how many products already classified 
        if i % 100 == 0: 
            async_print(i, end='\t')
        
        # Getting products that have exactly 
        # the same name in examples
        matched_products = examples[examples[:, 0] == product]
        if len(matched_products) > 0:
            category = get_category(matched_products)
            result.append([product, category])
            continue
        
        # Deleting from current product name all non finnish symbols
        cleaned_current = cleaner(product)

        # Getting products that have exactly 
        # the same name in examples after cleaning.
        matched_products = examples[cleaned_prodcuts == cleaned_current]
        if len(matched_products) > 0:
            category = get_category(matched_products)
            result.append([product, category])
            continue
        
        # Getting products that contains all words 
        matched_conditions = contains_words(cleaned_prodcuts, cleaned_current)
        matched_products = examples[matched_conditions]

        if len(matched_products) > 0:
            category = get_category(matched_products)
            result.append([product, category])
            predicted_product.append([product, category])
            continue
        
        category = model.predict([product])[0]
        predicted_product.append([product, category])
        result.append([product, category])

    async_print('\n')
    async_print("WRITING RESULT TO {}".format(NOT_CLASSIFIED_XLSX))
    write_result(NOT_CLASSIFIED_XLSX, result, 
        sheet=NOT_CLASSIFIED_SHEET, 
        category_column=NOT_CLASSIFIED_CATEGORY_COLUMN, 
        offset=NOT_CLASSIFIED_ROW_OFFSET)
    async_print()
    async_print("WRITING PREDICTED predicted.xlsx")
    write_predicted(predicted_product)
    async_print()
    async_print("ALL IS COMPLETE.")
    async_print("")



if __name__ == '__main__':
    main_function()
    
