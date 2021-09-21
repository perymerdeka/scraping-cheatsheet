import flask_excel as excel

@app.route('/download', methods=['GET'])
def download_data():
    sample_data=[0, 1, 2]
    excel.init_excel(app)
    extension_type = "csv"
    filename = "test123" + "." extension_type
    d = {'colName': sample_data}
    return excel.make_response_from_dict(d, file_type=extension_type, file_name=filename)

# docs: http://flask.pyexcel.org/en/latest/
