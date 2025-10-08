import csv

def read_rule_csv(csv_path):
    rules = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rule = {}
            for key, value in row.items():
                # Split by ';' and strip whitespace
                rule[key] = [v.strip() for v in value.split(';') if v.strip()]
            rules.append(rule)
    return rules

# Example
mapping_rules = read_rule_csv('rule_mapping.csv')
print(mapping_rules)
