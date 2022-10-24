import csv
import sys
import numpy

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)

        evidence = []
        labels = []

        # for each user in reader, add evidence and label
        for row in reader:

            # evidence for one user
            row_evidence = []

            for idx, value in enumerate(row[:17]):
                row_evidence.append(convert(row, idx))
            if len(row_evidence) != 17:
                raise ValueError('Evidence incomplete for user in this row')

            evidence.append(row_evidence)
            # append label for this user
            labels.append(convert(row, 17))

    return (evidence, labels)


def convert(row, idx):
    """
    Return the updated info for one user (at idx column from row reader), after 
    converting it to the expected data type.
    """

    # the column range for row indexes in csv is 0 - 17
    # each index expects a diferrent data type conversion
    # define templates for the expected data type based on the row's index
    months = {
        "Jan": 0, 
        "Feb": 1, 
        "Mar": 2, 
        "Apr": 3, 
        "May": 4, 
        "June": 5, 
        "Jul": 6, 
        "Aug": 7, 
        "Sep": 8, 
        "Oct": 9, 
        "Nov": 10, 
        "Dec": 11
    }

    idx_ints = [0, 2, 4, 11, 12, 13, 14]
    idx_floats = [1, 3, 5, 6, 7, 8, 9]
    idx_month = [10]
    idx_visitor = [15]
    idx_weekend = [16]
    idx_revenue = [17]
    
    # return the corresponding value after mathing the row's index
    if idx in idx_ints:
        return int(row[idx])
    elif idx in idx_floats:
        return float(row[idx])
    elif idx in idx_month:
        return months[row[idx]]
    elif idx in idx_visitor:
        if row[idx] == "Returning_Visitor":
            return 1
        else:
            return 0
    elif idx in idx_weekend:
        if row[idx] == "TRUE":
            return 1
        else:
            return 0
    elif idx in idx_revenue:
        if row[idx] == "TRUE":
            return 1
        else:
            return 0


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    
    model = KNeighborsClassifier(n_neighbors=1)

    return model.fit(evidence, numpy.ravel(labels))


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    if len(labels) != len(predictions):
        raise ValueError('Actual labels list length does not match predictions list length')
    
    positives = 0
    negatives = 0
    total_labels_positive = 0
    total_labels_negative = 0
    
    # check for each element in actual labels if it's 1 or 0 
    # 1 -> increase the total positives count and check if prediction matches to increase the positives as well
    # 0 -> increase the total negatives count and check if prediction matches to increase the negatives as well
    for actual, prediction in zip(labels, predictions):
        if actual == 1:
            total_labels_positive += 1
            if actual == prediction:
               positives += 1
        else:
            total_labels_negative += 1
            if actual == prediction:
               negatives += 1

    sensitivity = positives / total_labels_positive
    specificity = negatives / total_labels_negative

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
