class DNA():

    def __init__(self, gene):
        self.gene = gene
        self.pair = {
            'A':'T',
            'T':'A',
            'C':'G',
            'G':'C'
        }

    def complement(self):
        #developing the complement of the specific gene
        complement = ''
        for i in self.gene:
            complement += self.pair[i]
        return complement

    def count(self):
        #count the number of nitrogenous base within the string
        frequency = {}
        for i in self.pair.keys():
            frequency[i] = self.gene.count(i)
        return frequency

    def percentage_base(self):
        #calculating the percentage of each nitrogenous base in the gene
        percentages = {}
        amounts = self.count()
        for i in amounts.keys():
            percentages[i] = str(round(amounts[i]*100/len(self.gene),2)) + "%"
        return percentages

    def convert_amino_acid(self):
        #divide the gene into codons, which is then converted to the appropriate amino acids
        codon = [self.gene[i-3:i] for i in range(3, len(self.gene)+1,3)]
        if len(self.gene)%3 != 0:
            codon.append(self.gene[len(self.gene) - len(self.gene)%3:len(self.gene)+1])
        return codon

    def convert_to_RNA(self, start, end):
        RNA = ""
        for i in self.gene[start-1:end]:
            if i == 'T':
                RNA += "U"
            else:
                RNA += i
        return RNA

    def count_occurrence(self, pattern, optional_dna = None):
        counter = 0
        if optional_dna == None:
            optional_dna = self.gene
        for i in range(len(optional_dna) - len(pattern) + 1):
            if optional_dna[i:i + len(pattern)] == pattern:
                counter += 1
        return counter

    def frequency_map_k(self, k):
        #count the number of occurrences of all k-mers
        potential_k = {}
        for i in range(len(self.gene) - k + 1):
            current_combo = self.gene[i:i+k]
            if current_combo in potential_k.keys():
                potential_k[current_combo] += 1
                continue
            else:
                potential_k[current_combo] = 1
        return potential_k

    def SymbolArray(self, symbol):
        #count the number of times that a symbol occurs in a substring
        array = {}
        extended_gene = self.gene + self.gene[:len(self.gene)//2]
        array[0] = self.count_occurrence(symbol,self.gene[:len(self.gene)//2])
        for i in range(1, len(self.gene)):
            array[i] = array[i-1]
            if extended_gene[i - 1] == symbol:
                array[i] = array[i] -1
            if extended_gene[i + len(self.gene)//2 - 1] == symbol:
                array[i] = array[i] + 1
        return array


class Motif(DNA):
    def __init__(self, gene):
        super().__init__(self)
        self.gene = gene
