import json
import sys

def build_view(json_path, out_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    md = f"# Participant Record: {data.get('participant_id')}\n\n"
    md += "> **NON-CLAIM BOUNDARY**: This record is reconstructive evidence. It is out-of-band and read-only. It does not constitute governance authority, endorsement, approval, or semantic truth certification.\n\n"
    md += f"**Role:** {data.get('role')}\n"
    md += f"**Admission Status:** {data.get('admission_status')}\n\n"
    
    md += "## Evidence References\n"
    refs = data.get('evidence_references', [])
    if not refs:
        md += "No contributions logged.\n"
    for ref in refs:
        md += f"- `{ref.get('artifact_id')}` (SHA256: `{ref.get('digest')}`)\n"
        
    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(md)

if __name__ == "__main__":
    build_view(sys.argv[1], sys.argv[2])
