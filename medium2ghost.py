# Import libraries
import os
import requests, json, jwt, re
from dotenv import load_dotenv
from datetime import datetime, timedelta
from medium_api import Medium

# Load the environment variables from the .env file
load_dotenv()

# Get RAPIDAPI_KEY from the environment
medium_api_key = os.getenv('RAPIDAPI_KEY')

# Create a `Medium` Object
medium = Medium(medium_api_key)

# Ghost Config
ghost_api_url = os.getenv('GHOST_API_URL')+"/ghost/api/admin/posts/"
ghost_api_key = os.getenv('GHOST_API_KEY')

# Split the key into ID and SECRET
id, secret = ghost_api_key.split(':')

# Prepare header and payload
iat = int(datetime.now().timestamp())

header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
payload = {
    'iat': iat,
    'exp': iat + 5 * 60,
    'aud': '/admin/'
}

# Create the token (including decoding secret)
token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)
headers = {'Authorization': 'Ghost {}'.format(token)}

# Get the `Publication` Object using "publication_slug" and print ID
publication_slug = medium.publication(publication_slug=os.getenv('MEDIUM_PUB_SLUG'))

# Create a "Publication" Object
publication = medium.publication(publication_id=publication_slug._id, save_info=False)

# Fetch all publication articles
all_articles = publication.get_articles_between(
                                _from=datetime.now(), 
                                _to=datetime.now() - timedelta(days=10) # days should be 1 less than the actual days
                            )
for article in all_articles:
    user = medium.user(user_id=article.author.user_id)

    # Remove the first H1 and cover image from the article to avoid duplication
    remove_title_md = re.sub(r'^#\s+.*\n\n?', '', article.markdown, count=1)
    updated_md = re.sub(r'^!\[\].*$', '', remove_title_md, count=1, flags=re.MULTILINE)

    data = {
        "posts": [{
            "title": article.title,
            "status": "published",
            "published_at": article.published_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "feature_image": article.image_url,
            "tags": [{"name": tag} for tag in article.tags],
            "mobiledoc": json.dumps({
                "version": "0.3.1",
                "atoms": [],
                "cards": [["markdown", {"markdown": f"Authored by **{user.fullname}**\n{updated_md}" }]], # Prepend the author name to the article
                "markups": [],
                "sections": [[10, 0]]
            }),
        }]
    }

    response = requests.post(ghost_api_url, headers=headers, json=data)

    if response.status_code == 201:
        print(article.title + " created successfully!")
    else:
        print(f"Failed to create post. Status code: {response.status_code}")
        print(response.text)
