import sqlite3
import json

try:
    conn = sqlite3.connect('openfang.db')
    c = conn.cursor()
    c.execute("SELECT id, name, manifest FROM agents WHERE name = 'assistant'")
    row = c.fetchone()
    if row:
        agent_id, name, manifest_blob = row
        manifest = json.loads(manifest_blob.decode('utf-8'))
        
        # Patch the model and provider
        manifest['llm'] = {
            'provider': 'openrouter',
            'model': 'openrouter/google/gemma-2-9b-it'
        }
        
        new_blob = json.dumps(manifest).encode('utf-8')
        c.execute("UPDATE agents SET manifest = ? WHERE id = ?", (new_blob, agent_id))
        conn.commit()
        print(f"Agent {name} patched successfully!")
    else:
        print("Assistant agent not found in db.")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
