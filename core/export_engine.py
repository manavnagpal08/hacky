import pandas as pd
import json
import io
import os

class ExportEngine:
    def __init__(self):
        pass
        
    def export_to_json(self, data):
        """Converts dict data to JSON string."""
        return json.dumps(data, indent=4)
        
    def export_to_csv(self, data):
        """Converts tables data to CSV. Returns bytes for download."""
        if not data.get("tables"):
            return None
            
        output = io.StringIO()
        for t_idx, table in enumerate(data["tables"]):
            # Assume table['dataframe'] is a serialized dict, we recreate it
            # Actually, this data comes from JSON. We should assume it's list of lists.
            raw_data = table.get("raw_data", [])
            if raw_data:
                df = pd.DataFrame(raw_data)
                output.write(f"--- Table {t_idx} (Page {table.get('page')}) ---\n")
                df.to_csv(output, index=False, header=False)
                output.write("\n")
                
        return output.getvalue().encode('utf-8')
        
    def export_to_excel(self, data):
        """Converts tables data to Excel. Returns bytes for download."""
        if not data.get("tables"):
            return None
            
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for t_idx, table in enumerate(data["tables"]):
                raw_data = table.get("raw_data", [])
                if raw_data:
                    df = pd.DataFrame(raw_data)
                    sheet_name = f"Table_{t_idx}_Pg_{table.get('page')}"
                    # Excel sheet names max 31 chars
                    df.to_excel(writer, sheet_name=sheet_name[:31], index=False, header=False)
                    
        return output.getvalue()
