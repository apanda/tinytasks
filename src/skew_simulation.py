import random
import sys

def sample(distribution):
    """ Returns a sample from the given distribution, where the distribution
    should be specified as a list of (value, cumulative_probability) tuples,
    in increasing order of cumulative probability. """
    r = random.random()
    for value, cum_prob in distribution:
        if r < cum_prob:
            return value

def get_file_access_distribution(distribution_filename, num_files):
    """ Returns a list of cumulative probabilities that the particular file
    was accesses.
    TODO: that comment makes no sense. """
    access_frequency_counts = []
    distribution_file = open(distribution_filename, "r")
    print "Reading distribution from file %s" % distribution_filename
    for line in distribution_file:
        if line.startswith("File"):
            continue
        items = line.split("\t")
        access_frequency = int(items[0])
        file_cum_prob = float(items[3])
        access_frequency_counts.append((access_frequency, file_cum_prob))

    print "Sampling to determine # accesses for each file"
    file_access_counts = []
    total_accesses = 0.0
    while len(file_access_counts) < num_files:
        # Sample from the distribution of file access frequencies to determine
        # how many accesses are for this file.
        num_accesses = sample(access_frequency_counts)
        file_access_counts.append(num_accesses)
        total_accesses += num_accesses

    print "Finding distribution of accesses for each file"
    # Now that we have the number of accesses per file, create a distribution
    # accessses (note that accesses per file is used only as a relative
    # number).
    file_access_distribution = []
    cumulative_accesses = 0.0
    for index, file_access_count in enumerate(file_access_counts):
        cumulative_accesses += file_access_count
        file_access_distribution.append((index,
                                         cumulative_accesses / total_accesses))
    return total_accesses, file_access_distribution

def get_uniform_distribution(num_files):
    distribution = []
    while len(distribution) < num_files:
        cumulative_probability = (len(distribution) + 1) * 1.0 / num_files
        distribution.append((len(distribution), cumulative_probability))
    return distribution

def get_files_to_machines(num_files, num_machines):
    file_ids = range(num_files)
    random.shuffle(file_ids)
    current_index = 0
    files_to_machines = {}
    for machine_id in range(num_machines):
        files_per_machine = ((num_files - current_index) /
                             (num_machines - machine_id))
        for file in file_ids[current_index:current_index+files_per_machine]:
            files_to_machines[file] = machine_id
        current_index += files_per_machine
    return files_to_machines

def main(argv):
    # Cluster utilization
    utilization = 0.6
    # The number of file accesses that can be handled each minute on a single
    # machine, for a full-sized file.
    file_accesses_per_minute = 30
    # Frequency with which to measure the # of file accesses that have occured.
    measurement_period_minutes = 0.25
 
    num_machines = 100
    # This is probably small in terms of how many blocks we expect per
    # machine...
    base_number_files = num_machines*1000
    multiplier_values = [1, 2, 5, 10, 100, 1000]
    for multiplier in multiplier_values: 
        num_files = multiplier * base_number_files

        total_accesses, distribution = get_file_access_distribution(
                "aggregated_access_frequencies", num_files)
        # Comment the below 2 lines back in to use uniform (rather than
        # facebook-inspired) file access pattern distributions.
        #distribution = get_uniform_distribution(num_files)
        #total_accesses = num_files * 5

        files_to_machines = get_files_to_machines(num_files, num_machines)
        # right now this makes no sense, because this is fewer accesses than
        # will happen in a minute.
        accesses_per_measurement = (num_machines * file_accesses_per_minute *
                                    multiplier * measurement_period_minutes *
                                    utilization)
        num_measurements = max(1, total_accesses / accesses_per_measurement)
        print "Num measurements: %s" % num_measurements

        num_accesses_per_machine_minute = []

        for measurement in range(1): 
            accesses_per_machine = []
            while len(accesses_per_machine) < num_machines:
                accesses_per_machine.append(0)

            for i in range(accesses_per_measurement):
                # Ignore any difference between local and non-local accesses.
                file_accessed = sample(distribution)
                accesses_per_machine[files_to_machines[file_accessed]] += 1 
            num_accesses_per_machine_minute.extend(accesses_per_machine)

        num_accesses_per_machine_minute.sort()
        # Write CDF.
        results_filename = "skew_results_%s" % num_files
        results_file = open(results_filename, "w")
        stride = max(1, len(num_accesses_per_machine_minute) / 100)
        average_accesses_per_machine = accesses_per_measurement * 1.0 / num_machines
        for i, num_accesses in enumerate(
                num_accesses_per_machine_minute[::stride]):
            normalized_num_accesses = (num_accesses * 1.0 /
                                       average_accesses_per_machine)
            results_file.write("%s\t%s\n" %
                    (i * 1.0 / len(num_accesses_per_machine_minute[::stride]),
                     normalized_num_accesses))

if __name__ == "__main__":
    main(sys.argv)
