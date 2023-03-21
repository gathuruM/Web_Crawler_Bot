from pymongo import MongoClient

client = MongoClient()

db = client[]
collection = db[]
# Each website I crawl gets into a separate folder
def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating Project: " + directory)
        # making the folder
        os.makedirs(directory)

# Creating data files(queue and crawled files) for each folder/project
def create_data_files(project_name, base_url):
    # Queue = A list of links waiting to be crawled
    queue = project_name + '/queue.txt'
    # Crawled = List of crawled links
    crawled = project_name + '/crawled.txt'
    # Check if a file exists if not Create
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, "")

# Create a new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

# create_project_dir('Trial')
# create_data_files('trial', "https://www.cftc.gov/")

# Appending data to the existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

# Deleting the contents in a file
def delete_file_contents(path):
    with open(path, 'w'):
        pass

# Read a file and convert links to set
def file_to_set(filename):
    results = set()
    with open(filename, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Convert the set of links into a file
def set_to_file(set_of_links, file):
    delete_file_contents(file)
    for link in sorted(set_of_links):
        append_to_file(file, link)