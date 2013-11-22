__author__ = 'ajit'
# Naive Bayes learning on the data;
# Assignment 1: Vishwajit Kolathur Nov 17th 2013

import csv

#constant for calculating Laplace-estimate of P(C = c)
k = 10
#constant for calculating M-estimate of P(Xi = xi | C = c)
m = 0.4


def take_csv(file_name, array):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'letter':
                continue
            else:
                array.append(row)


def test_classify(train_data, test_data):
    # Initializing P(C=c) holder and data structures to optimize lookup based on c
    prior_probability = {}
    lexical_order = {}
    # Initialize Counter for correct classification
    classify = 0
    # Iterate over training data and organize it in lexical order to optimize lookup
    for data in train_data:
        if data[0] in lexical_order:
            lexical_order[data[0]].append(data)
        else:
            lexical_order[data[0]] = []
            lexical_order[data[0]].append(data)
    # For each alphabet calculate prior probability P(C = c)
    for alphabet in "abcdefghijklmnopqrstuvwxyz":
        prior_probability[alphabet] = (len(lexical_order[alphabet]) + k) / (len(train_data) + 26 * k)
    # For each test case find argmax[ P(C = c) pi( P(Xi = xi | C =c) ] and compare with output
    for data in test_data:
        # Initialize Probabilities data structures as a hash table
        pi_probability_xi_given_c = {}
        probabilities = {}
        for alphabet in "abcdefghijklmnopqrstuvwxyz":
            # Init the base probability to 1
            pi_probability_xi_given_c[alphabet] = 1
            # For each alphabet calculate for this test instance P(Xi = xi | C = c) and multiply
            for i in range(1, 41):
                # Find number of occurrences of Xi = xi in the training data with C = c
                count = len([occurrence for occurrence in lexical_order[alphabet] if occurrence[i] == data[i]])
                # Calculate Probability with M estimate method
                pi_probability_xi_given_c[alphabet] *= ((count + m * 1/10)/(len(lexical_order[alphabet]) + m))
            # Calculating the final probability that the given test case is a character
            probabilities[alphabet] = prior_probability[alphabet] * pi_probability_xi_given_c[alphabet]
        # Finding Argmax
        if max(probabilities, key=probabilities.get) == data[0]:
            classify += 1
    # Output classification statistics, rate, raw number etc
    print("Classified Correctly: " + str(classify))
    print("Classified Incorrectly: " + str(len(test_data) - classify))
    # Calculating classification rate and miss-classification rate
    classify, miss_classify = classify / len(test_data), (len(test_data) - classify)/len(test_data)
    print("Classification Rate: " + str(classify))
    print("MissClassification Rate: " + str(miss_classify))
    # returning control


def split_data(array, training, testing, split):
    i = 0
    for element in array:
        i += 1
        i %= 10
        if i % 11 < (10 - split):
            training.append(element)
        else:
            testing.append(element)


def main():
    # Initializing holders for training and test data
    train_data = []
    test_data = []
    # Start reading data from the CSVs
    print("Starting Reading")
    take_csv('./test_binning.csv', test_data)
    take_csv('./train_binning.csv', train_data)
    print("Reading Done")
    # Calculating Training accuracy
    print("Training Accuracy (testing training data against itself)")
    test_classify(train_data, train_data)
    # Start testing, to verify accuracy of Learner
    print("Starting Testing")
    # Calculating testing accuracy
    test_classify(train_data, test_data)
    print("Testing Done")
    print("If training and testing combined and split 70:30")
    train_data.extend(test_data)
    del test_data
    array = train_data
    del train_data
    test_data = []
    train_data = []
    split_data(array, train_data, test_data, 3)
    del array
    print("Starting Testing 70:30 split")
    test_classify(train_data, test_data)
    print("Testing Done on 70:30 split")
    # End

if __name__ == "__main__":
    main()