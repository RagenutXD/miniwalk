import requests, dotenv, os

dotenv.load_dotenv()

def get_unread_letters(res):
    url = f"{os.environ.get('SUPABASE_URL')}/rest/v1/letters"
    payload = {'seen': 'eq.false'}

    headers = {
        'apikey': os.environ.get('SUPABASE_SECRET_KEY'),
        'Authorization': f"Bearer {os.environ.get('SUPABASE_SECRET_KEY')}"
    }
    
    try: 
        data = requests.get(url, params=payload, headers=headers)
        res[0] = data.json()
    except requests.exceptions.RequestException as e:
        res[0] = [{'failed':e}]

def mark_as_read(id, res):
    url = f"{os.environ.get('SUPABASE_URL')}/rest/v1/letters"
    payload = {'id': f"eq.{id}"}

    headers = {
        'apikey': os.environ.get('SUPABASE_SECRET_KEY'),
        'Authorization': f"Bearer {os.environ.get('SUPABASE_SECRET_KEY')}",
        'Prefer': 'return=representation'
    }

    try:
        data = requests.patch(url, params=payload, headers=headers, data={'seen': 'true'})
        res[0] = data.status_code
    except requests.exceptions.RequestException as e:
        res[0] = [{'failed':e}]

