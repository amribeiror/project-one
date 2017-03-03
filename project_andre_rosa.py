FASTA_file = '../../../datasets/membrane-beta_2state.3line.txt'

#Iterates F parsing sequences and topologies
F = open(FASTA_file, 'r')
sequences = []

for line in F :
	if line.startswith('>') :
		pass
	else :
		sequences.append(line.strip())

list_sequences = sequences[::3]
list_topologies = sequences[1::3]
##QUESTION: What if the FASTA file is in a different 'format', let's say different number of line breaks, [::3](1::3] may not be valid anymore. Problem?

#Converts sequences (and protein topologies) to a list of single residues/topologies
list_single_residues = []

for sequences in list_sequences :
	list_single_sequences = []
	list_single_sequences.append(sequences)
	index_res = 0
	for single_sequences in list_single_sequences[index_res] :
		list_single_residues.append(single_sequences)

list_single_labels = []

for topologies in list_topologies :
	list_single_topologies = []
	list_single_topologies.append(topologies)
	index_label = 0
	for single_topologies in list_single_topologies[index_label] :
		list_single_labels.append(single_topologies)

sequences = list_single_residues
topologies = list_single_labels

#Converts each residue to a 20-dimensional numerical vector
all_sequences = []
aa_matrix = ['A', 'P', 'R', 'L', 'T', 'C', 'G', 'E', 'Y', 'Q', 'V', 'S', 'D', 'H', 'M', 'I', 'F', 'K', 'W', 'N']

for residue in sequences :
	list_of_zeros = [0]*20
	for i in range(len(aa_matrix)) :
		aa = aa_matrix[i]
		if residue == aa :
			list_of_zeros[i] = 1
			all_sequences.append(list_of_zeros)

#Converts each topology to a numerical list
#Creates a dataset to train the model X, by pairing the input with the expected output. Excludes last protein topologies
y = [ 0 if t == 'i' else 1 if t == 'o' else 2 if t == 'P' else 3 if t == 'L' else 4 for t in topologies]

#Creates a numpy array according to inputted window size
window_size = int(input('Please, enter window size:'))
chosen_window_size = window_size
vector_index = 0
nr_of_loops = 0
list_single_vectors = []
list_vectors = []
for vector in all_sequences :
    
    nr_of_loops += 1
    
    while window_size != 0 and len(all_sequences[:-window_size]) > window_size and vector_index < len(all_sequences):
        window_size += -1
        
        list_vectors.extend(all_sequences[vector_index])
        vector_index += 1
    list_vectors.append(list_single_vectors)    
    vector_index = nr_of_loops
    window_size = chosen_window_size
    list_single_vectors = []

#QUESTION: I have problems with the very last amino acid residues, whose window size creates vectors with fewer coordinates than the previous vectors. How to fix this? At the moment, I'm creating a new list by excluding those last rows.
list3 = list_vectors[:-window_size]
print(list3[0:2])
print(all_sequences[0:2])
print(len(all_sequences))
print(len(list3))

#TRAIN SVM
import numpy as np
from sklearn import svm

SVM = svm.SVC(kernel='linear', C = 1.0)
X = np.array(list3)
print(X)
print(len(X))
print(X.shape)

print(y)
print(len(y))
print(y.shape)

SVM.fit(X[:720],y[:720]).score(X[-720:],y[-720:])
print(SVM.fit(X[:-720],y[:-720]).score(X[-720:], y[-720:])


#K-fold cross-validation###########################
#X_folds = np.array_split(X, 3)
#y_folds = np.array_split(y, 3)
#scores = list()

#for k in range(3) :
#	X_train = list(X_folds)
#	X_test = X_train.pop(k)
#	X_train = np.concatenate(X_train)
#	y_train = list(y_folds)
#	y_test = y_train.pop(k)
#	y_train = np.concatenate(y_train)
#	scores.append(SVM.fit(X_train, y_train).score(X_test, y_test))

#print(scores)


#PREDICT
#topredict = [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
##Returns a predicted output by classifying the input using the model. Tests the last protein sequence.
#print(len(X[-720:]))
#SVM.predict(X[-720:])
#print(SVM.predict(X[-720:]))




