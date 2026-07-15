import json
import jsonschema

SCHEMA_PATH = "schemas/participant_profile_registry_v0_1.schema.json"

def check_registry_record(record):
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    try:
        jsonschema.validate(instance=record, schema=schema)
    except jsonschema.ValidationError as e:
        return {"status": "NON_CONFORMING", "reason": f"Schema violation: {e.message}"}

    # Specification Boundary Enforcement
    consent = record.get("consent_profile", {})
    if not consent.get("attribution_opt_in") and record.get("public_attribution_name"):
        return {
            "status": "SPECIFICATION_PRESSURE", 
            "reason": "Attribution name present but attribution_opt_in is false. Privacy boundary violated."
        }

    return {"status": "CONFORMING", "reason": "Structural boundaries preserved"}

if __name__ == "__main__":
    import sys
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        print(json.dumps(check_registry_record(json.load(f))))
