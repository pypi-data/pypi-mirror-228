import pandas as pd
from .debug import Debug
from .EDIParser import EDIParser

HEADERS = [
    {"title": "Transaction Purpose", "id": "BFR01"},
    {"title": "Reference ID", "id": "BFR02"},
    {"title": "Release #", "id": "BFR03"}, 
    {"title": "Schedule Type", "id": "BFR04"}, 
    {"title": "Qty Type", "id": "BFR05"},
    {"title": "Start Date", "id": "BFR06"},
    {"title": "End Date",  "id": "BFR07"},
    {"title": "Create Date", "id": "BFR08"},
    {"title": "Planning Schedule Type", "id": "BFR12"},
    {"title": "Supplier Name", "id": "N1_Supplier_N102"},
    {"title": "Supplier Location", "id": "N1_Supplier_N102"},
    {"title": "Buying Party Name",  "id": "N1_Buying Party_N102"},
    {"title": "Buying Party Location", "id": "N1_Buying Party_N104"},
    {"title": "Ship To Name",  "id": None},
    {"title": "Ship To Location", "id": None},
    {"title": "Ship To Address", "id": None},
    {"title": "Ship To Address", "id": None},
    {"title": "Ship To City", "id": None},
    {"title": "Ship To State", "id": None},
    {"title": "Ship To Postal Code", "id": None},
    {"title": "Planning Schedule/Material Release Issuer", "id": None},
    {"title": "Planning Schedule/Material Release Issuer Location", "id": None}
]

ITEM_DETAIL_HEADERS = [
    {"title": "Buyer Part", "id": None},
    {"title": "UPC", "id": None},
    {"title": "EAN", "id": None},
    {"title": "GTIN", "id": "LIN03"},
    {"title": "Vendor Part", "id": None},
    {"title": "Item Description", "id": "LIN07"},
    {"title": "Pack Qty", "id": "PO401"},
    {"title": "Qty", "id": "FST01"},
    {"title": "Forecast Type", "id": "FST02"},
    {"title": "Forecast Timing", "id": "FST03"},
    {"title": "Start Date", "id": "FST04"},
    {"title": "End Date", "id": "FST05"},
    {"title": "Delivery Requested", "id": None},
    {"title": "Qty per Store UOM", "id": "SDQ01"},
    {"title": "Store", "id": "SDQ03"},
    {"title": "Qty per Store #", "id": "SDQ04"},
    {"title": "Case UPC", "id": None}
]

class EDI2CSV(EDIParser):
    def __init__(self, element_delimiter="*", segment_delimiter="~", data_delimiter="`", use_debug=False):
        self.parser = EDIParser(
            edi_format="830_Forecast",
            element_delimiter=element_delimiter,
            segment_delimiter=segment_delimiter,
            data_delimiter=data_delimiter,
            use_parent_key_detail=False,
            use_parent_detail=True,
            parent_headers=['symbol', 'id', 'name', 'short_name', 'type', 'notes', 'req', 'data_type', 'data_type_ids', 'length'],
            use_child_key_detail=False,
            use_child_detail=False,
            use_short_name=False,
            use_debug=use_debug
        )
        self.json_data = None
        self.use_debug = use_debug

    def to_csv(self, edi_file_path, csv_file_path):
        
        parent_df, loop_df = self.parse(edi_file_path)
        
        Debug.log_message(f"Writing a csv file...")
        header_title_df = self.create_header_title_df()
        header_title_df.to_csv(csv_file_path, header=True, index=False)
        
        headers_df = self.get_values(HEADERS, parent_df)
        headers_df.to_csv(csv_file_path, mode='a', header=True, index=False)

        item_title_headers_df = self.create_item_title_headers_df()
        item_title_headers_df.to_csv(csv_file_path, mode='a', header=True, index=False)
        
        item_headers_df = self.get_values(ITEM_DETAIL_HEADERS, loop_df)
        item_headers_df.to_csv(csv_file_path, mode='a', header=True, index=False)
        Debug.log_message(f"Done to write the csv file.")
        
    def create_header_title_df(self):
        headers = ["HEADER"]
        df = pd.DataFrame(columns=headers)
        return df
        
    def get_values(self, headers, data):
        df = pd.DataFrame(index=data.index, columns=[header["title"] for header in headers])
        for header in headers:
            title = header["title"]
            col_id = header["id"]
            if col_id in data.columns:
                df[title] = data[col_id]
            else:
                df[title] = None
        if self.use_debug:
            Debug.log_debug(f"values: {df}")
        return df
    
    def create_item_title_headers_df(self):
        headers = ["ITEM DETAIL","","","","","","","FORECAST DETAIL"]
        return pd.DataFrame(columns=headers)

    def parse(self, edi_file_path):
        Debug.log_message(f"Parsing an EDI file...")
        data = self.parser.parse(edi_file_path)
        
        parent_df = self.create_parent_df(data)
        loop_df = self.create_loop_df(data)
        
        if self.use_debug:
            Debug.log_debug(f"parent df: \n{parent_df}")
            Debug.log_debug(f"loop df: \n{loop_df}")
            # Debug.log_debug(f"merged df: \n{merged_df}")
        Debug.log_message(f"Done to parse the edi file.")
        return parent_df, loop_df

    def create_parent_df(self, data):
        df = pd.DataFrame()
        for parent_key, parent in data.items():
            parent_type = parent['type']
            parent_symbol = parent['symbol']

            if parent_type == 'loop':
                continue

            if self.use_debug:
                Debug.log_debug(f"\nParsing: {parent_symbol}")

            values = parent[EDIParser.VALUE_NAME]
            for name, value in values.items():
                # col_name = f"{parent_symbol}_{name}"
                col_name = name
                if self.use_debug:
                    Debug.log_debug(f"{col_name}: {value}")
                df[col_name] = [value]

        # Create Names dataframe
        n1_df = self.create_n1_df(data["L_N1"])
        df = pd.concat([df, n1_df], axis=1)
        return df

    def create_n1_df(self, n1_segment):
        df = pd.DataFrame()
        segments = n1_segment[EDIParser.VALUE_NAME]
        for segment in segments:
            for segment_key, segment_data in segment.items():
                n1_values = segment_data[EDIParser.VALUE_NAME]
                prefix_key = f"{segment_data['symbol']}_{n1_values['N101']}"
                for n1_value_name, n1_vavlue in n1_values.items():
                    col_name = f'{prefix_key}_{n1_value_name}'
                    df[col_name] = [n1_vavlue]
        return df

    def create_loop_df(self, data):
        df = pd.DataFrame()
        # segment_value = data[EDIParser.VALUE_NAME]
        for s_key, segment in data.items():
            s_type = segment['type']
            s_symbol = segment['symbol']

            if s_type != 'loop':
                continue
            # e_value = segment[EDIParser.VALUE_NAME]
            if s_symbol == "L_N1":
                continue

            if self.use_debug:
                Debug.log_debug(f"\nParsing: {s_symbol}")
            
            loop_df = self.parse_loop_df(segment)
            df = pd.concat([df, loop_df], axis=1)
        return df

    def parse_loop_df(self, loop_segment):
        df = pd.DataFrame()
        loop_key = loop_segment["symbol"]
        loop_value = loop_segment["value"]
        # Array data
        for list_item in loop_value:
            # Dict data
            v_df = pd.DataFrame(index=[0])
            for s_key, segment in list_item.items():
                s_symbol = segment["symbol"]
                s_type = segment["type"]
                
                if s_type == "segment":
                    prefix_col_name = s_symbol
                    
                    s_values = segment["value"]
                    for v_key, v_value in s_values.items():
                        col_name = v_key
                        v_df[col_name] = [v_value]
                if s_type == "loop":
                    nested_df = self.parse_loop_df(segment)
                    v_df = pd.concat([v_df, nested_df], axis=1)
            if df.empty:
                df = v_df
            else:
                df = pd.concat([df, v_df], axis=0, ignore_index=True)
        return df
