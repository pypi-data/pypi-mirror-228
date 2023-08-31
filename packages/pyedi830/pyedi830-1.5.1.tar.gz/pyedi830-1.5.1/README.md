# pyedi830
Pyedi830 uses JSON format definitions to make it easy to parse and convert from EDI830 file to JSON and CSV file/data.

## TODOs

* Finish 830 definition
* Implement colorful exceptions

## EDI Format Definitions
EDI830 parser messages consist of a set of Segments (usually lines) comprised of Elements. Some segments can be part of a Loop. These formats are defined in JSON. See the provided format(s) for examples.

A loop has certain expected properties:

* `id` (Loop ID)
* `repeat` (Max times the loop can repeat)

Each segment has certain expected properties:

* `id` (Segment ID)
* `name` (Human-readable segment name)
* `req` (Whether segment is required: [M]andatory, [O]ptional)
* `max_uses` (Some segments can be included more than once)
* `notes` (Optional details for hinting documentation)
* `syntax` (An optional list of syntax rules, defined below)
* `elements` (List of included elements)

Each element has certain expected features: 

* `id` (Element ID)
* `name` (Human-readable element name)
* `req` (Whether segment is required: [M]andatory, [O]ptional)
* `data_type` (Type of segment data, defined below)
* `data_type_ids` (If `data_type` is `ID`, this is a dict of valid IDs with descriptions)
* `length` (Dict specifying field length)
    * `min` (Min length of field)
    * `max` (Max length of field)

Valid data types include:

* `AN` (Any data type)
* `DT` (Date, must be provided as Python DATE or DATETIME object)
* `ID` (Alphanumeric ID. List of valid IDs provided as dict with descriptions)
* `R`  (Percentage)
* `Nx` (Number with `x` decimal points)
* `TM` (Time, must be provided as Python TIME or DATETIME object)

Syntax rules are specified as a dict with a `rule` and a list of `criteria`. Valid syntax rules include:

* `ATLEASTONE` (where at least one of the element IDs in the `criteria` list is included and is not empty)
* `ALLORNONE` (where either all of the element IDs in the `criteria` list are included, or none are)
* `IFATLEASTONE` (if the first element in `criteria` is included, then at least one of the other elements must be included)

# Code Examples

```python
    from pyedi830 import EDIParser
    from pyedi830 import EDI2CSV
    from pyedi830 import EDI2PDF


    edi_file_path = "test/test_edi_830_forecast.edi"

    # Convert to json file
    json_file_path = "test_edi_830_forecast.json"
    edi_parser = EDIParser(
        edi_format="830_Forecast",
        element_delimiter="*",
        segment_delimiter="~",
        use_parent_key_detail=True,
        use_parent_detail=True,
        parent_headers=['symbol', 'name', 'type', 'notes'],
        use_child_key_detail=True,
        use_child_detail=False,
        use_debug=True
    )
    edi_parser.to_json(edi_file_path, json_file_path)

    # Parse to json data
    json_data = edi_parser.parse(edi_file_path)


    # Convert to csv file.
    csv_file_path = "edi_830.csv"
    edi2csv = EDI2CSV(use_debug=True)
    edi2csv.to_csv(edi_file_path=edi_file_path, csv_file_path=csv_file_path)


    # Convert to html
    html_file_path = "edi_830.html"
    edi2csv = EDI2PDF(use_debug=True)
    edi2csv.to_html(edi_file_path=edi_file_path, html_file_path='html_file_path')

    # Convert to pdf
    pdf_file_path = "edi_830.pdf"
    edi2csv.to_pdf(edi_file_path=edi_file_path, pdf_file_path=pdf_file_path, temp_html_file_path=html_file_path)

```

# Install

Install system-wide

    pip install pyedi830

Or install in a virtual environment

    virtualenv my_env
    pip -E my_env install pyedi830

# Licensing

pyedi830 has a BSD license. The full license text is included with the source code for the package. 
