# Usage: python garden_planner.py <zone> <plants,comma,sep,list>
# Example: python garden_planner.py 8b radishes,potatoes,turnips,thyme

#import garden_schema as gs # garden_schema.py, actually calls GPT-4 API
import json, os, sys

from pathlib import Path

from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader


def sanitize_json(data):
    """
    Goes through the JSON and makes sure that all the values are valid JSON.
    """

    for key, value in data.items():
            try:
                data[key] = json.loads(value)
            except (TypeError, json.JSONDecodeError):
                # If it's a non-string value or not a valid JSON string, continue
                pass
                
    return data

#####

if __name__ == "__main__":

    # Load Templates
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    plant_template = env.get_template('plant-template.html')
    base_template = env.get_template('base-template.html')
    index_template = env.get_template('index-template.html')

    garden_object = {}

    # Get a list of all files in the json directory
    json_dir = os.path.join(root, 'json')
    json_files = [f for f in os.listdir(json_dir) if os.path.isfile(os.path.join(json_dir, f))]
    json_files = [os.path.join(json_dir, f) for f in json_files]

    for file in json_files:
        with open(file, 'r') as fh:
            data = json.load(fh)
            fname = os.path.basename(file.strip('.json'))

            garden_object[fname] = data
            

    #filename = os.path.join(root, 'output.html')

    #garden_object = sanitize_json(garden_object)

    # Create individual HTML files for each plant
    for plant in garden_object:
        with open(f"html/{plant}.html", 'w') as fh:

            plantdata = garden_object[plant]
            plantdata = sanitize_json(plantdata)
            fh.write(plant_template.render(base_template=base_template, plant=plantdata, zone="8b"))
            print(f"Saved html/{plant}.html")

            #htmldoc = HTML(string=open("output.html", "r").read(), base_url="")
            #Path("out.pdf").write_bytes(htmldoc.write_pdf())

            #print("PDF version written to out.pdf")
            #print("HTML version written to output.html")

    # Get a list of all files in the html directory
    html_dir = os.path.join(root, 'html')
    html_files = [f for f in os.listdir(html_dir) if os.path.isfile(os.path.join(html_dir, f))]
    
    listlink={}

    for file in html_files:
        fname = file.removesuffix('.html')
        listlink[fname] = f"html/{file}"

    # Alphabatize the linklist by key
    listlink = dict(sorted(listlink.items()))
    # Create the index.html file
    with open(f"index.html", 'w') as fh:
        fh.write(index_template.render(base_template=base_template, linklist=listlink))
        print(f"Saved index.html")



        
