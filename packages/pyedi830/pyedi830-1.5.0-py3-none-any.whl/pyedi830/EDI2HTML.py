import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
import sys
from io import StringIO
from .debug import Debug
from .EDI2CSV import EDI2CSV, HEADERS, ITEM_DETAIL_HEADERS

class EDI2HTML(EDI2CSV):
    def __init__(self, template_file_path='830_Forecast.html', use_debug=False):
        super().__init__(use_debug)
        self.template_file_path=template_file_path
        self.use_debug = use_debug
        # Initialize the Jinja2 environment and specify the template directory
        self.template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.env.filters['datetime_format'] = self.format_datetime
        self.env.filters['get_fst_iterrows'] = self.get_fst_iterrows
        self.env.filters['get_sdq_iterrows'] = self.get_sdq_iterrows
        # Load the template file
        self.template = self.env.get_template(self.template_file_path)        
        
        self.parent_df = None
        self.loop_df = None
        self.headers_df = None
        self.items_df = None
        self.lines_df = None
    
    def to_html(self, edi_file_path, html_file_path):
        parent_df, loop_df = self.parse(edi_file_path)
        self.parent_df = parent_df
        self.loop_df = loop_df
        # merged_df = pd.concat([parent_df, loop_df], axis=1)
        # merged_df.to_csv('output/edi_830_temp.csv')

        self.headers_df = self.get_values(HEADERS, parent_df)
        self.items_df = self.get_values(ITEM_DETAIL_HEADERS, loop_df)
        self.lines_df = self.items_df[self.items_df['GTIN'].notnull()]
        
        self.write_html(
            header=self.headers_df.iloc[0],
            items_df=self.items_df,
            lines_df=self.lines_df,
            org_header=parent_df.iloc[0],
            output_file_path=html_file_path
        )

    def write_html(self, header, items_df, lines_df, org_header, output_file_path):
        Debug.log_message(f"Rendering dataframe to html...")

        # Render the template with the DataFrame
        html_output = self.template.render(header=header, items_df=items_df, lines_df=lines_df, org_header=org_header)
        if isinstance(output_file_path, StringIO):
            output_file_path.write(html_output)
            output_file_path.seek(0)
            Debug.log_message(f"Done to render html into buffer")
        else:
            # Save the rendered HTML to a file
            with open(output_file_path, 'w') as f:
                f.write(html_output)

            Debug.log_message(f"Done to render html in {output_file_path}")
        return output_file_path
    
    def format_datetime(self, value):
        return value.strftime('%-m/%-d/%Y')
    
    def get_next_index(self, df, cur_index):
        loc = df.index.get_loc(cur_index)
        # Check if it's the last index
        if loc == len(df) - 1:
            return None  # or raise an error if you prefer
        return df.index[loc + 1]

    def get_fst_rows(self, cur_line_index):
        next_line_index = self.get_next_index(self.lines_df, cur_line_index)
        if next_line_index is None:
            if cur_line_index == 0:
                Debug.log_warning(f"get_fst_rows: Return empty dataframe")
                return pd.DataFrame()
            next_line_index = self.items_df.index[-1] + 1
        fst_df = self.items_df[
            (self.items_df.index >= cur_line_index) & 
            (self.items_df.index < next_line_index) & 
            self.items_df['Qty'].notnull()
        ]
        # if self.use_debug:
        #     Debug.log_debug(f"fst_df: \n{fst_df}")
        return fst_df
    
    def get_fst_iterrows(self, cur_line_index):
        return self.get_fst_rows(cur_line_index).iterrows()

    def get_sdq_rows(self, cur_line_index, cur_fst_index):
        # Get FST df
        fst_df = self.get_fst_rows(cur_line_index)
        if len(fst_df) == 0:
            Debug.log_warning(f"get_sdq_rows: Return empty dataframe")
            return pd.DataFrame()
        next_fst_index = self.get_next_index(fst_df, cur_fst_index)
        if next_fst_index is None:
            next_line_index = self.get_next_index(self.lines_df, cur_line_index)
            if next_line_index is None:
                if cur_line_index == 0:
                    Debug.log_warning(f"get_sdq_rows: Return empty dataframe")
                    return pd.DataFrame()
                next_fst_index = self.items_df.index[-1] + 1
            else:
                next_fst_index = next_line_index
        sdq_df = self.items_df[
            (self.items_df.index >= cur_fst_index) & 
            (self.items_df.index < next_fst_index) 
        ]
        # if self.use_debug:
        #     Debug.log_debug(f"sdq_df: \n{sdq_df}")
        return sdq_df
    
    def get_sdq_iterrows(self, cur_line_index, cur_fst_index):
        return self.get_sdq_rows(cur_line_index, cur_fst_index).iterrows()