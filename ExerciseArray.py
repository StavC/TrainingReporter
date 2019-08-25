class ExerciseArray(object):

    def __init__(self, name):
        self.name = name
        self.records_array = []

    def add_record(self, Record):
        self.records_array.append(Record)

    def pop_record(self):
        self.records_array.pop()

    def print_array(self):
        for record in self.records_array:
            print(self.name)
            print(f"{record.weight} KG Recorded at {record.date}")

    def length(self):
        return len(self.records_array)

    def get_weights(self):
        weights_array = []
        for record in self.records_array:
            weights_array.append(record.weight)
        return weights_array

    def get_dates(self):
        dates_array = []
        for record in self.records_array:
            dates_array.append(record.date)
        return dates_array
