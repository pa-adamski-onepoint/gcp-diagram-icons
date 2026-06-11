import os
import json
import re
from urllib.parse import quote

ICON_DIRS = ["google-cloud-legacy-icons", "category-icons", "core-products-icons"]
REPO_URL_BASE = "https://raw.githubusercontent.com/pa-adamski-onepoint/gcp-diagram-icons/main"

ACRONYMS = {
    "Ai": "AI", "Api": "API", "Apis": "APIs", "Gke": "GKE", "Vpc": "VPC", "Cdn": "CDN",
    "Hsm": "HSM", "Ekm": "EKM", "Tpu": "TPU", "Nat": "NAT", "Vpn": "VPN",
    "Iam": "IAM", "Ids": "IDs", "Gpu": "GPU", "Gpus": "GPUs", "Dns": "DNS", "Sql": "SQL",
    "Nlp": "NLP", "Iap": "IAP", "Cas": "CAS", "Hpc": "HPC", "Iot": "IoT",
    "Saas": "SaaS", "Saa S": "SaaS", "Vertexai": "Vertex AI",
    "Pubsub": "PubSub", "Os": "OS", "Ssd": "SSD", "Gce": "GCE", "Cx": "CX", "Qna": "QnA"
}

def clean_name(filename):
    name = filename.replace("-512-color-rgb.svg", "").replace("-512-color.svg", "").replace(".svg", "")
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = name.replace("_", " ").replace("-", " ")
    name = " ".join(name.split())
    name = name.title()
    name = name.replace(" 512 Color Rgb", "").replace(" 512 Color", "")
    
    words = name.strip().split(' ')
    new_words = []
    for w in words:
        if w in ACRONYMS:
            new_words.append(ACRONYMS[w])
        else:
            new_words.append(w)
            
    return " ".join(new_words)

def generate_map():
    icon_map = {}
    seen_products = set()
    
    for dir_path in ICON_DIRS:
        if not os.path.exists(dir_path): continue
        
        for root, _, files in os.walk(dir_path):
            rel_path = os.path.relpath(root, dir_path)
            if rel_path == '.' and dir_path == 'category-icons':
                continue

            for file in sorted(files):
                if not file.endswith(".svg"): continue
                
                original_product_name = clean_name(file)
                product_name = original_product_name
                
                if product_name in seen_products:
                    product_name = f"{product_name} 2"
                seen_products.add(product_name)

                # Build raw github URL
                # E.g., core-products-icons/Database/cloud-sql.svg
                full_local_path = os.path.join(root, file)
                # Need to URL encode parts of the path
                url_path_parts = [quote(p) for p in full_local_path.split(os.sep)]
                url_path = "/".join(url_path_parts)
                
                full_url = f"{REPO_URL_BASE}/{url_path}"
                icon_map[product_name] = full_url

    with open("gcp_icon_map.json", "w") as f:
        json.dump(icon_map, f, indent=2)
        
    print(f"Generated map with {len(icon_map)} icons.")

if __name__ == "__main__":
    generate_map()
