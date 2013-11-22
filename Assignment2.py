__author__ = 'ajit'
import csv
import sys

#constant for calculating Laplace-estimate of P(C = c)
k = 2.1
#constant for calculating M-estimate of P(Xi = xi | C = c)
m = 2


def read_data_file(file_name, array):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        if len(array) == 0:
            for row in reader:
                if row[len(row) - 1] == "label":
                    continue
                label = row.pop(len(row)-1)
                row.insert(0, label)
                array.append(row)
        else:
            i = 0
            for row in reader:
                if row[len(row) - 1] == "label":
                    continue
                label = row.pop(len(row)-1)
                if label == array[i][0]:
                    array[i].extend(row)
                    i += 1
                else:
                    print("Mix Match ERROR!")
                    sys.exit(1)


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
    for alphabet in range(0, 122):
        if str(alphabet) in lexical_order:
            prior_probability[str(alphabet)] = (len(lexical_order[str(alphabet)]) + k) / (len(train_data) + 122 * k)
        else:
            lexical_order[str(alphabet)] = []
            prior_probability[str(alphabet)] = 0
    # For each test case find argmax[ P(C = c) pi( P(Xi = xi | C =c) ] and compare with output
    for data in test_data:
        # Initialize Probabilities data structures as a hash table
        pi_probability_xi_given_c = {}
        probabilities = {}
        for alphabet in range(0, 122):
            # Init the base probability to 1
            pi_probability_xi_given_c[str(alphabet)] = 1
            # For each alphabet calculate for this test instance P(Xi = xi | C = c) and multiply
            for i in range(1, 130):
                # Find number of occurrences of Xi = xi in the training data with C = c
                if len(lexical_order[str(alphabet)]) != 0:
                    count = len([occurrence for occurrence in lexical_order[str(alphabet)] if occurrence[i] == data[i]])
                else:
                    count = 0
                # Calculate Probability with M estimate method
                pi_probability_xi_given_c[str(alphabet)] *= ((count + m * 1/10)/(len(lexical_order[str(alphabet)]) + m))
            # Calculating the final probability that the given test case is a character
            probabilities[str(alphabet)] = prior_probability[str(alphabet)] * pi_probability_xi_given_c[str(alphabet)]
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
    data = []
    train_data = []
    test_data = []
    print("Starting Reading")
    read_data_file("1_data_nd.csv", data)
    read_data_file("7_data_nd.csv", data)
    read_data_file("8_data_nd.csv", data)
    read_data_file("12_data_nd.csv", data)
    read_data_file("50_data_nd.csv", data)
    read_data_file("51_data_nd.csv", data)
    print("Reading Done")
    print("Starting Splitting")
    split_data(data, train_data, test_data, 3)
    del data
    print("Done Splitting")
    print("Training Accuracy (testing training data against itself)")
    test_classify(train_data, train_data)
    print("Starting Testing")
    test_classify(train_data, test_data)
    print("Testing Done")
if __name__ == "__main__":
    main()