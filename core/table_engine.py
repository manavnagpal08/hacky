import pdfplumber
import pandas as pd

class TableEngine:
    def __init__(self):
        pass

    def extract_tables_from_pdf(self, pdf_path):
        """
        Extracts tables from a PDF using pdfplumber.
        Returns a list of dicts with page number and pandas DataFrame.
        """
        tables_data = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    # Extract tables from the page
                    tables = page.extract_tables()
                    for t_idx, table in enumerate(tables):
                        if table:
                            # Clean the table data (remove None values)
                            cleaned_table = [[cell if cell is not None else "" for cell in row] for row in table]
                            
                            # Convert to DataFrame
                            if len(cleaned_table) > 0:
                                # Use first row as header if it exists
                                headers = cleaned_table[0]
                                data = cleaned_table[1:] if len(cleaned_table) > 1 else []
                                
                                # Sometimes headers have duplicates or empty strings, make them unique
                                if not any(headers):
                                    headers = [f"Col {j}" for j in range(len(headers))]
                                else:
                                    headers = [str(h) if h else f"Col {j}" for j, h in enumerate(headers)]
                                
                                try:
                                    df = pd.DataFrame(data, columns=headers)
                                    tables_data.append({
                                        "page": i + 1,
                                        "table_index": t_idx,
                                        "dataframe": df,
                                        "raw_data": cleaned_table
                                    })
                                except Exception as e:
                                    print(f"Error creating dataframe for table on page {i+1}: {e}")
                                    # Fallback without headers
                                    df = pd.DataFrame(cleaned_table)
                                    tables_data.append({
                                        "page": i + 1,
                                        "table_index": t_idx,
                                        "dataframe": df,
                                        "raw_data": cleaned_table
                                    })
        except Exception as e:
            print(f"Error extracting tables: {e}")
            
        return tables_data
