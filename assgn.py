import csv
import math
import difflib

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def is_name_similar(name1, name2, threshold=0.6):
    ratio = difflib.SequenceMatcher(None, name1, name2).ratio()
    return ratio >= threshold

def find_similar_entries(entries, distance_threshold=0.2, name_similarity_threshold=0.6):
    for i, entry1 in enumerate(entries):
        for j, entry2 in enumerate(entries[i+1:]):
            distance = haversine_distance(entry1['latitude'], entry1['longitude'],
                                           entry2['latitude'], entry2['longitude'])
            if distance <= distance_threshold and is_name_similar(entry1['name'], entry2['name'], name_similarity_threshold):
                entry1['similar_entries'] = 1
                entry2['similar_entries'] = 1
            else:
                if 'similar_entries' not in entry1:
                    entry1['similar_entries'] = 0
                if 'similar_entries' not in entry2:
                    entry2['similar_entries'] = 0

def write_entries_to_csv(entries, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['latitude', 'longitude', 'name', 'similar_entries']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

def main():
    entries = []
    with open('assignment_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entries.append({'latitude': float(row['latitude']), 'longitude': float(row['longitude']), 'name': row['name']})
    find_similar_entries(entries)
    write_entries_to_csv(entries, 'entries_with_similarity.csv')

if __name__ == '__main__':
    main()
