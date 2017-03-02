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

print(list_sequences)
