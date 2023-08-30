import numpy as np


class GreyRelationAnalyzer:
    # resolution factor should be [0,1], usually it's 0,5
    resolution_factor: float
    reference_seq: list[float]
    seq_len: int
    analysis_sequences: list[list[float]]

    def __init__(self, resolution_factor=0.5, reference_seq=None):
        self.resolution_factor = resolution_factor
        if reference_seq is None:
            raise ValueError("reference_seq should not be none")
        reference_seq_avg = np.average(reference_seq)
        for index in range(len(reference_seq)):
            reference_seq[index] = reference_seq[index] / reference_seq_avg
        self.reference_seq = reference_seq
        self.seq_len = len(reference_seq)
        self.analysis_sequences = list()

    def add_analysis_seq(self, analysis_seq: list[float]):
        if len(analysis_seq) != self.seq_len:
            raise ValueError("analysis_seq len is not" + str(self.seq_len))
        self.analysis_sequences.append(analysis_seq)

    def analysis(self) -> list[list[float]]:
        # preprocessing
        middle = list()
        preprocessed = list()
        for analysis_sequences_index in range(len(self.analysis_sequences)):
            analysis_seq_avg = np.average(self.analysis_sequences[analysis_sequences_index])
            preprocessed_analysis_seq = list()
            middle_seq = list()
            for index in range(self.seq_len):
                preprocessed_analysis_seq_val = self.analysis_sequences[analysis_sequences_index][
                                                    index] / analysis_seq_avg
                preprocessed_analysis_seq.append(preprocessed_analysis_seq_val)
                middle_seq.append(np.abs(self.reference_seq[index] - preprocessed_analysis_seq_val))
            preprocessed.append(preprocessed_analysis_seq)
            middle.append(middle_seq)
        min_val = np.min(middle)
        max_val = np.max(middle)
        result = list()
        for preprocessed_index in range(len(preprocessed)):
            result_seq = list()
            for index in range(self.seq_len):
                result_seq.append((min_val + self.resolution_factor * max_val) / (
                        np.abs(self.reference_seq[index] - preprocessed[preprocessed_index][
                            index]) + self.resolution_factor * max_val))
            result.append(result_seq)
        return result

    def analysis_res(self) -> list[float]:
        res = self.analysis()
        ret = list()
        for index in range(len(res)):
            ret.append(np.average(res[index]))
        return ret
