import csv


def convert_to_bio(input_file, output_true_file, output_pred_file):
    """
    Converts a CSV file with named entity recognition results to two BIO format files.

    Args:
        input_file: Path to the input CSV file.
        output_true_file: Path to the output BIO file for y_true column.
        output_pred_file: Path to the output BIO file for y_pred column.
    """

    with open(input_file, 'r', encoding='utf-8') as csvfile, \
            open(output_true_file, 'w', encoding='utf-8') as true_outfile, \
            open(output_pred_file, 'w', encoding='utf-8') as pred_outfile:

        reader = csv.DictReader(csvfile, delimiter=';')

        current_report_true = ""
        current_report_pred = ""

        for row in reader:
            report_id = row['report']
            entity = row['entity']
            y_true = row['y_true']
            y_pred = row['y_pred']

            if y_true != "O":
                y_true = y_true.replace("-", "_")

            if y_pred != "O":
                y_pred = y_pred.replace("-", "_")

            tokens = entity.split()

            # BIO tagging for y_true
            if y_true == 'O':
                bio_tags_true = ['O'] * len(tokens)
            else:
                bio_tags_true = ['B_' + y_true] + ['I_' + y_true] * (len(tokens) - 1)

            # BIO tagging for y_pred
            if y_pred == 'O':
                bio_tags_pred = ['O'] * len(tokens)
            else:
                bio_tags_pred = ['B_' + y_pred] + ['I_' + y_pred] * (len(tokens) - 1)

            # Write to output files
            if report_id != current_report_true:
                if current_report_true:
                    true_outfile.write('\n')
                current_report_true = report_id

            if report_id != current_report_pred:
                if current_report_pred:
                    pred_outfile.write('\n')
                current_report_pred = report_id

            for i in range(len(tokens)):
                true_outfile.write(f"{tokens[i]}\t{bio_tags_true[i]}\n")
                pred_outfile.write(f"{tokens[i]}\t{bio_tags_pred[i]}\n")


# Example usage:
input_file = 'entities_f1.csv'
output_true_file = 'y_true.bio'
output_pred_file = 'y_pred.bio'
convert_to_bio(input_file, output_true_file, output_pred_file)