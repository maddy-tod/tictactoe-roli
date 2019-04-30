# -*- coding: utf-8 -*-

# Copyright 2019 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import logging
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets.base import load_data
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from qiskit_aqua.input import SVMInput
import numpy as np
import random

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SVMQPlayer:
    def __init__(self):
        print("made a q player!")
        self.move = 0
        self.data_file = 'data.csv'
        self.data_path = 'PlayerLogic'

        feature_dim = 3  # dimension of each data point
        sample_Total, training_input, test_input, class_labels = SVMQPlayer.userDefinedData(self.data_path, self.data_file,
                                                                                 ['0', '1', '2', '3', '4', '5', '6',
                                                                                  '7', '8'],
                                                                                 training_size=6000, test_size=500,
                                                                                 n=feature_dim, PLOT_DATA=False)

        temp = [test_input[k] for k in test_input]
        total_array = np.concatenate(temp)

        aqua_dict = {
            'problem': {'name': 'classification'},
            'algorithm': {
                'name': 'SVM'
            },
            'multiclass_extension': {'name': 'AllPairs'}
        }

        algo_input = SVMInput(training_input, test_input, total_array)

        from qiskit.aqua import QiskitAqua
        aqua_obj = QiskitAqua(aqua_dict, algo_input)
        self.algo_obj = aqua_obj.quantum_algorithm

        result = aqua_obj.run()
        for k, v in result.items():
            print("'{}' : {}".format(k, v))

    def take_turn(self, board):
        board = [x if x else 0 for x in board]

        to_predict = SVMQPlayer.singleDataItem(self.data_path, self.data_file, board, n=3)

        self.move = self.algo_obj.predict(to_predict)[0]

        # if the move selected already contains a play, choose randomly
        if board[self.move]:
            spaces = [index for index, x in enumerate(board) if x == 0]
            self.move = random.choice(spaces)


    @staticmethod
    def userDefinedData(location, file, class_labels, training_size, test_size, n=2, PLOT_DATA=True):

        data, target, target_names = load_data(location, file)
        # sample_train is of the same form as data
        sample_train, sample_test, label_train, label_test = train_test_split(
            data, target, test_size=0.25, train_size=0.75, random_state=22)

        # Now we standarize for gaussian around 0 with unit variance
        std_scale = StandardScaler().fit(sample_train)
        sample_train = std_scale.transform(sample_train)
        sample_test = std_scale.transform(sample_test)

        # Now reduce number of features to number of qubits
        pca = PCA(n_components=n).fit(sample_train)
        sample_train = pca.transform(sample_train)
        sample_test = pca.transform(sample_test)

        # Samples are pairs of points
        samples = np.append(sample_train, sample_test, axis=0)
        minmax_scale = MinMaxScaler((-1, 1)).fit(samples)
        sample_train = minmax_scale.transform(sample_train)
        sample_test = minmax_scale.transform(sample_test)

        # If class labels are numeric
        if class_labels[0].isdigit():
            # Pick training size number of samples from each distro
            training_input = {key: (sample_train[label_train == int(key), :])[:training_size] for k, key in
                              enumerate(class_labels)}
            test_input = {key: (sample_test[label_test == int(key), :])[: test_size] for k, key in
                          enumerate(class_labels)}

        else:
            # if they aren't
            training_input = {key: (sample_train[label_train == k, :])[:training_size] for k, key in
                              enumerate(class_labels)}
            test_input = {key: (sample_train[label_train == k, :])[training_size:(
                    training_size + test_size)] for k, key in enumerate(class_labels)}

        if PLOT_DATA:
            for k in range(0, 9):
                plt.scatter(sample_train[label_train == k, 0][:training_size],
                            sample_train[label_train == k, 1][:training_size])

            plt.title("PCA dim. reduced user dataset")
            plt.show()

        return sample_train, training_input, test_input, class_labels

    @staticmethod
    def singleDataItem(location, file, data, n=2):

        # load the old data so that this new example gets transformed correctly
        test_data, target, target_names = load_data(location, file)

        # Only use sample_train to help get the right shape for the new input
        sample_train, sample_test, label_train, label_test = train_test_split(
            test_data, target, test_size=0.25, train_size=0.75, random_state=22)

        # convert to np array to enable joining to other data
        data = np.array(data)
        # add the to be tested data onto the end of the overall data
        sample_train = np.vstack((sample_train, data))

        # TODO check that none of this is changing the order of the variables - if so will cause issues and this whole method won't work!

        # Now we standarize for gaussian around 0 with unit variance
        std_scale = StandardScaler().fit(sample_train)
        sample_train = std_scale.transform(sample_train)

        # Now reduce number of features to number of qubits
        pca = PCA(n_components=n).fit(sample_train)
        sample_train = pca.transform(sample_train)

        # Scale to the range (-1,+1)
        minmax_scale = MinMaxScaler((-1, 1)).fit(sample_train)
        sample_train = minmax_scale.transform(sample_train)

        # returns array which contains one array with is the 2 data points to use
        # OUTPUT IS READY TO BE PUT INTO SVM.PREDICT
        return [sample_train[-1]]

    def get_data_view(self, board, size=3):

        board =  [x if x else 0 for x in board]

        # take this many elements to compare against
        test_str = ', '.join([str(x) for x in board[:size]])

        # mapping from move to number of times that move was seen
        results_dict = {}

        file_path = self.data_path + '/data/' + self.data_file

        with open(file_path) as file:
            lines = file.readlines()

            # look at all the data
            for line in lines:

                # if this matches the current state of the board add to counts
                if line.startswith(test_str):
                    move = line[-2:-1]
                    if move not in results_dict:
                        results_dict[move] = 0
                    results_dict[move] += 1

        return results_dict
