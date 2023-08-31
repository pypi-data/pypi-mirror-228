import urllib.parse
import urllib.request
import json

def get_access_token(client_id, client_secret, redirect_uri, authorization_code):
    """
    
    
    """
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(token_url, data=data, method='POST')
    response = urllib.request.urlopen(req)
    response_data = response.read().decode('utf-8')
    access_token = json.loads(response_data)['access_token']
    return access_token

# Usage
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'YOUR_REDIRECT_URI'
authorization_code = 'CODE_FROM_AUTHORIZATION'
access_token = get_access_token(client_id, client_secret, redirect_uri, authorization_code)


def share_linkedin_post_with_media(access_token, comment, media_url, visibility_code='anyone'):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
    }
    
    payload = {
        'author': 'urn:li:person:YOUR_PERSON_URN',  # Replace with your LinkedIn URN
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': comment
                },
                'shareMediaCategory': 'IMAGE',  # Adjust for different media types
                'media': [
                    {
                        'status': 'READY',
                        'originalUrl': media_url
                    }
                ]
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': visibility_code
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req)
    response_data = response.read().decode('utf-8')
    return json.loads(response_data)

# Usage
post_comment = "Check out my latest post with media!"
media_url = 'URL_TO_YOUR_MEDIA_FILE'  # Replace with the actual media URL
response = share_linkedin_post_with_media(access_token, post_comment, media_url)
print(response)



def share_linkedin_post(access_token, comment, visibility_code='anyone'):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
    }
    
    payload = {
        'author': 'urn:li:person:YOUR_PERSON_URN',  # Replace with your LinkedIn URN
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': comment
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': visibility_code
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req)
    response_data = response.read().decode('utf-8')
    return json.loads(response_data)

# Usage
post_comment = "Check out my latest post!"
response = share_linkedin_post(access_token, post_comment)
print(response)
