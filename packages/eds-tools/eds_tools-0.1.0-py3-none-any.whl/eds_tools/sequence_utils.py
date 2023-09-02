inverted = {"A": "T", "T": "A", "C": "G", "G": "C", "N": "N"}


def reverse_complement(sequence):
    return "".join([inverted.get(base, "N") for base in reversed(sequence)])
