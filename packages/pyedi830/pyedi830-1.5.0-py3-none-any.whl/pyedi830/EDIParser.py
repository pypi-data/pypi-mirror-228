"""
Parses a provided EDI message and tries to build a dictionary from the data
Provides hints if data is missing, incomplete, or incorrect.
"""

import datetime
import json
from io import StringIO

from .supported_formats import supported_formats
from .debug import Debug

class EDIParser(object):
    VALUE_NAME = "value"
    PARED_VALUE_NAME = "parsed_value"
    
    def __init__(
        self, edi_format="830_Forecast", element_delimiter="*", segment_delimiter="~", data_delimiter="`", 
        use_parent_key_detail=False, use_parent_detail=False, parent_headers=None, 
        use_child_key_detail=False, use_child_detail=False, child_headers=None,
        use_short_name=True,
        use_debug=False,
    ):
        # Set default delimiters
        self.element_delimiter = element_delimiter
        self.segment_delimiter = segment_delimiter
        self.data_delimiter = data_delimiter
        
        self.use_parent_key_detail = use_parent_key_detail
        self.use_parent_detail = use_parent_detail
        self.parent_headers = parent_headers
        
        self.use_child_key_detail = use_child_key_detail
        self.use_child_detail = use_child_detail
        self.child_headers = child_headers
        
        self.use_short_name = use_short_name
        self.use_debug = use_debug

        # Set EDI format to use
        if edi_format in supported_formats:
            self.edi_format = supported_formats[edi_format]
        elif edi_format is None:
            self.edi_format = None
        else:
            # raise ValueError("Unsupported EDI format {}".format(edi_format))
            self.edi_format = None
            Debug.log_warning("Unsupported EDI format {}".format(edi_format))

    ################################
    # JSON Handers
    ################################
    def parse(self, file_path):
        if isinstance(file_path, StringIO):
            return self.parse_buffer(file_path)
        
        # Read the content of the file into a StringIO buffer
        with open(file_path, 'r') as file:
            buffer = StringIO(file.read())
        
        return self.parse_buffer(buffer)
    
    def parse_buffer(self, buffer: StringIO):
        json_data = None
        edi = buffer.getvalue()
        # lines = edi.split(self.segment_delimiter)
        
        # # Remove last empty lines
        # while lines and not lines[-1].strip():
        #     lines.pop()
        # edi = self.segment_delimiter.join(lines)
        
        # Add an empty line to parse
        edi += self.segment_delimiter
        found_segments, edi_data = self.parse_data(edi)
        json_data = edi_data
        
        return json_data

    def parse_data(self, data):
        """ Processes each line in the string `data`, attempting to auto-detect the EDI type.

        Returns the parsed message as a dict. """

        # Break the message up into chunks
        edi_segments = data.split(self.segment_delimiter)

        # Eventually, find the ST header and parse the EDI format
        if self.edi_format is None:
            raise NotImplementedError("EDI format autodetection not built yet. Please specify an EDI format.")

        to_return = {}
        found_segments = []
        
        while len(edi_segments) > 0:
            segment = edi_segments[0]
            # Remove whitespace and \n
            segment = segment.strip(" \n")
            if segment == "":
                edi_segments = edi_segments[1:]
                continue # Line is blank, skip
            # Capture current segment name
            segment_name = segment.split(self.element_delimiter)[0]
            if self.use_debug:
                Debug.log_debug(f"segment_name: {segment_name}")
            segment_obj = None
            # Find corresponding segment/loop format
            for seg_format in self.edi_format:
                # Check if segment is just a segment, a repeating segment, or part of a loop
                if seg_format["id"] == segment_name and seg_format["max_uses"] == 1:
                    # Found a segment
                    segment_obj = self.parse_segment(segment, seg_format)
                    edi_segments = edi_segments[1:]
                    break
                elif seg_format["id"] == segment_name and seg_format["max_uses"] > 1:
                    # Found a repeating segment
                    segment_obj, edi_segments = self.parse_repeating_segment(edi_segments, seg_format)
                    break
                elif seg_format["id"] == "L_" + segment_name:
                    # Found a loop
                    segment_name = seg_format["id"]
                    segment_obj, edi_segments = self.parse_loop(edi_segments, seg_format)
                    break

            if segment_obj is None:
                Debug.log_error("Unrecognized segment: {}".format(segment))
                edi_segments = edi_segments[1:] # Skipping segment
                continue
                # raise ValueError

            found_segments.append(segment_name)
            parent_key = self.get_parent_key(segment_name, segment_obj, seg_format)
            to_return[parent_key] = segment_obj


        return found_segments, to_return

    def parse_segment(self, segment, segment_format):
        if self.use_debug:
            Debug.log_debug(f"segment: {segment}")
        """ Parse a segment into a dict according to field IDs """
        fields = segment.split(self.element_delimiter)
        if self.use_debug:
            Debug.log_debug(f"fields: {fields}")
        if fields[0] != segment_format["id"]:
            raise TypeError("Segment type {} does not match provided segment format {}".format(fields[0], segment_format["id"]))
        elif len(fields)-1 > len(segment_format["elements"]):
            Debug.explain(segment_format)
            raise TypeError("Segment has more elements than segment definition")

        #segment_name = fields[0]
        to_return = {}
        to_return["symbol"] = segment_format["id"]
        to_return["name"] = segment_format["name"]
        if self.use_parent_detail:
            if self.parent_headers is not None and len(self.parent_headers) > 0:
                for header in self.parent_headers:
                    if header == 'symbol':
                        to_return["symbol"] = segment_format["id"]
                        continue
                    if header in segment_format:
                        to_return[header] = segment_format[header]
            else:
                to_return["notes"] = segment_format["notes"]
        to_return[EDIParser.VALUE_NAME] = None
        segment_value = {}
        for field, element in zip(fields[1:], segment_format["elements"]): # Skip the segment name field
            key = element["id"]
            if element["data_type"] == "DT":
                if len(field) == 8:
                    value = datetime.datetime.strptime(field, "%Y%m%d")
                elif len(field) == 6:
                    value = datetime.datetime.strptime(field, "%y%m%d")
                else:
                    value = field
            elif element["data_type"] == "TM":
                if len(field) == 4:
                    value = datetime.datetime.strptime(field, "%H%M")
                elif len(field) == 6:
                    value = datetime.datetime.strptime(field, "%H%M%S")
            elif element["data_type"] == "N0" and field != "":
                value = int(field)
            elif element["data_type"].startswith("N") and field != "":
                value = float(field) / (10**int(element["data_type"][-1]))
            elif element["data_type"] == "R" and field != "":
                value = float(field)
            else:
                value = field
            # Stripe the backspaces
            if isinstance(value, str):
                value = value.strip()
            element_key = key
            if self.use_child_key_detail:
                DEFAULT_NAME_KEY = "name"
                name_key = DEFAULT_NAME_KEY
                if self.use_short_name and "short_name" in element:
                    name_key = "short_name"
                    
                element_key = element[name_key]#.replace(" ", "_")
            if self.use_child_detail:
                # element_key = key
                segment_value[element_key] = {
                    "symbol": element["id"],
                    "name": element["name"],
                    EDIParser.VALUE_NAME: value,
                    EDIParser.PARED_VALUE_NAME: self.get_parsed_value(value, element)
                }
                if (self.child_headers is not None) and len(self.child_headers) > 0:
                    for header in self.child_headers:
                        if header in element:
                            segment_value[element_key][header] = element[header]
                
                # segment_value[element_key][EDIParser.PARED_VALUE_NAME] = self.get_parsed_value(value, element)
            else:
                value = self.get_parsed_value(value, element)
                segment_value[element_key] = value
        to_return[EDIParser.VALUE_NAME] = segment_value
        return to_return

    def parse_repeating_segment(self, edi_segments, segment_format):
        """ Parse all instances of this segment, and return any remaining segments with the seg_list """
        seg_list = []

        while len(edi_segments) > 0:
            segment = edi_segments[0]
            segment_name = segment.split(self.element_delimiter)[0]
            if segment_name != segment_format["id"]:
                break
            seg_list.append(self.parse_segment(segment, segment_format))
            edi_segments = edi_segments[1:]

        return seg_list, edi_segments

    def parse_loop(self, edi_segments, loop_format):
        """ Parse all segments that are part of this loop, and return any remaining segments with the loop_list """
        loop_list = []
        loop_dict = {}
        to_return = {}
        to_return["symbol"] = loop_format["id"]
        to_return["name"] = loop_format["name"]
        to_return["type"] = loop_format["type"]

        while len(edi_segments) > 0:
            segment = edi_segments[0]
            # Remove whitespace and \n
            segment = segment.strip(" \n")
            segment_name = segment.split(self.element_delimiter)[0]
            segment_obj = None

            # Find corresponding segment/loop format
            for seg_format in loop_format["segments"]:
                # Check if segment is just a segment, a repeating segment, or part of a loop
                if seg_format["id"] == segment_name and seg_format["max_uses"] == 1:
                    # Found a segment
                    segment_obj = self.parse_segment(segment, seg_format)
                    edi_segments = edi_segments[1:]
                elif seg_format["id"] == segment_name and seg_format["max_uses"] > 1:
                    # Found a repeating segment
                    segment_obj, edi_segments = self.parse_repeating_segment(edi_segments, seg_format)
                elif seg_format["id"] == "L_" + segment_name:
                    # Found a loop
                    segment_name = seg_format["id"]
                    segment_obj, edi_segments = self.parse_loop(edi_segments, seg_format)

            if segment_obj is None:
                # Reached the end of valid segments; return what we have
                break
            elif segment_name == loop_format["segments"][0]["id"] and loop_dict != {}: 
                # Beginning a new loop, tie off this one and start fresh
                loop_list.append(loop_dict.copy())
                loop_dict = {}
            parent_key = self.get_parent_key(segment_name, segment_obj, seg_format)               
            loop_dict[parent_key] = segment_obj
            # loop_list.append(segment_obj)
        if loop_dict != {}:
            loop_list.append(loop_dict.copy())
        to_return[EDIParser.VALUE_NAME] = loop_list
        return to_return, edi_segments

    def get_N1_key(self, segment_name, segment_obj):
        if self.use_debug:
            Debug.log_debug(f"get_N1_key: segment_name: {segment_name}")
            Debug.log_debug(f"get_N1_key: segment_obj: {segment_obj}")
        parent_key = segment_name
        entiry_id_code = None
        parent_obj = segment_obj[EDIParser.VALUE_NAME] if (EDIParser.VALUE_NAME in segment_obj) and isinstance(segment_obj[EDIParser.VALUE_NAME], dict) else segment_obj
        if self.use_child_key_detail:
            if self.use_child_detail:
                parent_obj = segment_obj[EDIParser.VALUE_NAME]["Entity ID Code"]
                entiry_id_code = EDIParser.VALUE_NAME
            else:
                entiry_id_code = "Entity ID Code"
        else:
            if self.use_child_detail:
                parent_obj = segment_obj["N101"]
                entiry_id_code = EDIParser.VALUE_NAME
            else:
                entiry_id_code = "N101"
        
        if self.use_debug:
            Debug.log_debug(f"get_N1_key: parent_obj: {parent_obj}")
            Debug.log_debug(f"get_N1_key: entiry_id_code: {entiry_id_code}")
            
        if entiry_id_code in parent_obj:
            if parent_obj[entiry_id_code] == "TO":
                parent_key = "Supplier name"
            elif parent_obj[entiry_id_code] == "BY":
                parent_key = "Buying party name"

        return parent_key

    def get_parent_key(self, segment_name, segment_obj, seg_format):
        parent_key = segment_name
        if self.use_debug:
            Debug.log_debug(f"parent_key: {parent_key}")
            Debug.log_debug(f"type: {seg_format['type'] if 'type' in seg_format else ''}")
        if self.use_parent_key_detail:
            if isinstance(segment_obj, dict):
                DEFAULT_NAME_KEY = "name"
                name_key = DEFAULT_NAME_KEY
                if self.use_short_name:
                    name_key = "short_name"
                if name_key in segment_obj:
                    parent_key = segment_obj[name_key]
                else:
                    if DEFAULT_NAME_KEY in segment_obj:
                        parent_key = segment_obj[DEFAULT_NAME_KEY]
                if segment_name == "N1":
                    parent_key = self.get_N1_key(segment_name, segment_obj)
                segment_obj["name"] = parent_key
                # parent_key = parent_key.replace(" ", "_")
        return parent_key

    def get_parsed_value(self, value, element_format):
        default_value = value
        if not isinstance(element_format, dict) or not "data_type_ids" in element_format:
            return default_value
        ids = element_format["data_type_ids"]
        if not ids:
            return default_value
        if value in ids:
            return ids[value]
        return default_value        
    
    def datetime_serializer(self, dt_obj):
        if isinstance(dt_obj, datetime.datetime):
            res = dt_obj.isoformat()
            # Check date or time
            if dt_obj.time().hour == 0 and dt_obj.time().minute == 0 and dt_obj.time().second == 0:
                res = dt_obj.strftime("%-m/%-d/%Y")
            else:
                if dt_obj.date() == datetime.datetime(1900, 1, 1).date():
                    res = dt_obj.strftime("%H:%M")
            return res
        raise TypeError("Type not serializable")
    
    def write_to_json_file(self, json_file_path, json_data):
        str_json = json.dumps(json_data, default=self.datetime_serializer, ensure_ascii=False, indent=4)
        with open(json_file_path, "w") as json_file:
            json_file.write(str_json)
        return json_file_path

    def write_to_buffer(self, json_data):
        str_json = json.dumps(json_data, default=self.datetime_serializer, ensure_ascii=False, indent=4)
        buffer = StringIO()
        buffer.write(str_json)
        buffer.seek(0)
        return buffer

    def to_json(self, edi_file_path, json_file_path):
        json_data = self.parse(edi_file_path)
        if json_data is None:
            Debug.log_error("Failed to parse EDI file: {edi_file_path}")
            return None
        if isinstance(json_file_path, StringIO):
            json_file_path = self.write_to_buffer(json_data)
            return json_file_path
        
        return self.write_to_json_file(json_file_path, json_data)
