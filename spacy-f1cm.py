import ast
import spacy
from sklearn.metrics import confusion_matrix, accuracy_score, precision_recall_fscore_support
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the spaCy model
nlp = spacy.load("model-best")


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return ast.literal_eval(content)


def parse_entities(this_data, this_nlp):
    this_true_entities = []
    this_pred_entities = []
    
    for text, annotations in this_data:
        true_ents = annotations['entities']
        
        # Get predictions from the loaded model
        doc = this_nlp(text)
        pred_ents = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        
        # Ensure we have a prediction for each true entity
        for start, end, label in true_ents:
            this_true_entities.append(label)
            pred_label = next((ent[2] for ent in pred_ents if ent[0] == start and ent[1] == end), 'O')
            this_pred_entities.append(pred_label)
    
    return this_true_entities, this_pred_entities


def plot_confusion_matrix(cmatrix, this_labels):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cmatrix, annot=True, fmt='d', cmap='Blues', xticklabels=this_labels, yticklabels=this_labels)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    plt.close()
    return


def generate_confusion_matrix_report(this_cm, this_labels):
    report = "Confusion Matrix Report\n"
    report += "=============================================\n\n"

    # Header
    report += "Tr\\Pr\t" + "\t".join(this_labels) + "\tTP\tFP\tFN\tTN\n"

    tp = np.diag(this_cm)
    fp = this_cm.sum(axis=0) - tp
    fn = this_cm.sum(axis=1) - tp
    tn = this_cm.sum() - (fp + fn + tp)

    for i, true_label in enumerate(this_labels):
        row = [str(this_cm[i, j]) for j in range(len(this_labels))]
        report += f"{true_label}\t" + "\t".join(row) + f"\t{tp[i]}\t{fp[i]}\t{fn[i]}\t{tn[i]}\n"

    return report


def generate_report(y_true, y_pred, this_labels):
    report = "Entity Recognition Report\n"
    report += "==========================\n\n"

    # Calculate overall accuracy
    accuracy = accuracy_score(y_true, y_pred)
    report += f"Overall Accuracy: {accuracy:.4f}\n\n"

    # Calculate precision, recall, and F1-score for each label
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=this_labels, zero_division=0)

    # Calculate macro and weighted averages
    macro_precision, macro_recall, macro_f1, _ = precision_recall_fscore_support(y_true, y_pred, labels=this_labels,
                                                                                 average='macro', zero_division=0)
    weighted_precision, weighted_recall, weighted_f1, _ = precision_recall_fscore_support(y_true, y_pred, labels=this_labels,
                                                                                          average='weighted',
                                                                                          zero_division=0)

    # Add macro and weighted averages to the report
    report += "Macro Average:\n"
    report += f"  Precision: {macro_precision:.4f}\n"
    report += f"  Recall: {macro_recall:.4f}\n"
    report += f"  F1-score: {macro_f1:.4f}\n\n"

    report += "Weighted Average:\n"
    report += f"  Precision: {weighted_precision:.4f}\n"
    report += f"  Recall: {weighted_recall:.4f}\n"
    report += f"  F1-score: {weighted_f1:.4f}\n\n"

    report += "Individual Labels:\n"
    for i, label in enumerate(this_labels):
        report += f"{label}:\n"
        report += f"  Precision: {precision[i]:.4f}\n"
        report += f"  Recall: {recall[i]:.4f}\n"
        report += f"  F1-score: {f1[i]:.4f}\n"
        report += f"  Support: {support[i]}\n\n"

    return report


# Load the data
data = load_data('test.json')

# Parse entities using the loaded model
true_entities, pred_entities = parse_entities(data, nlp)

print(f"Number of true entities: {len(true_entities)}")
print(f"Number of predicted entities: {len(pred_entities)}")

# Get unique labels
labels = sorted(set(true_entities + pred_entities))

# Filter out "O" labels
y_true_filtered = [y for y in true_entities if y != 'O']
y_pred_filtered = [pred_entities[i] for i, y in enumerate(true_entities) if y != 'O']
labels_filtered = [label for label in labels if label != 'O']

# Create confusion matrix
cm = confusion_matrix(y_true_filtered, y_pred_filtered, labels=labels_filtered)

# Plot confusion matrix and get the matrix (excluding "O" label)
plot_confusion_matrix(cm, labels_filtered)

# Generate confusion matrix report (excluding "O" label)
cm_report = generate_confusion_matrix_report(cm, labels_filtered)

# Generate entity recognition report (excluding "O" label)
er_report = generate_report(y_true_filtered, y_pred_filtered, labels_filtered)

# Save confusion matrix report to TXT file
with open('confusion_matrix_report.txt', 'w', encoding='utf-8') as f:
    f.write(cm_report)

# Save entity recognition report to TXT file
with open('entity_recognition_report.txt', 'w', encoding='utf-8') as f:
    f.write(er_report)

print("Confusion matrix saved as 'confusion_matrix.png'")
print("Confusion matrix report saved as 'confusion_matrix_report.txt'")
print("Entity recognition report saved as 'entity_recognition_report.txt'")
