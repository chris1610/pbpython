from appJar import gui
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path

# Define all the functions needed to process the files


def split_pages(input_file, page_range, out_file):
    """ Take a pdf file and copy a range of pages into a new pdf file

    Args:
        input_file: The source PDF file
        page_range: A string containing a range of pages to copy: 1-3,4
        out_file: File name for the destination PDF
    """
    output = PdfFileWriter()
    input_pdf = PdfFileReader(open(input_file, "rb"))
    output_file = open(out_file, "wb")

    # https://stackoverflow.com/questions/5704931/parse-string-of-integer-sets-with-intervals-to-list
    page_ranges = (x.split("-") for x in page_range.split(","))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    for p in range_list:
        # Need to subtract 1 because pages are 0 indexed
        try:
            output.addPage(input_pdf.getPage(p - 1))
        except IndexError:
            # Alert the user and stop adding pages
            app.infoBox("Info", "Range exceeded number of pages in input.\nFile will still be saved.")
            break
    output.write(output_file)

    if(app.questionBox("File Save", "Output PDF saved. Do you want to quit?")):
        app.stop()


def validate_inputs(input_file, output_dir, range, file_name):
    """ Verify that the input values provided by the user are valid

    Args:
        input_file: The source PDF file
        output_dir: Directory to store the completed file
        range: File A string containing a range of pages to copy: 1-3,4
        file_name: Output name for the resulting PDF

    Returns:
        True if error and False otherwise
        List of error messages
    """
    errors = False
    error_msgs = []

    # Make sure a PDF is selected
    if Path(input_file).suffix.upper() != ".PDF":
        errors = True
        error_msgs.append("Please select a PDF input file")

    # Make sure a range is selected
    if len(range) < 1:
        errors = True
        error_msgs.append("Please enter a valid page range")

    # Check for a valid directory
    if not(Path(output_dir)).exists():
        errors = True
        error_msgs.append("Please Select a valid output directory")

    # Check for a file name
    if len(file_name) < 1:
        errors = True
        error_msgs.append("Please enter a file name")

    return(errors, error_msgs)


def press(button):
    """ Process a button press

    Args:
        button: The name of the button. Either Process of Quit
    """
    if button == "Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        page_range = app.getEntry("Page_Ranges")
        out_file = app.getEntry("Output_name")
        errors, error_msg = validate_inputs(src_file, dest_dir, page_range, out_file)
        if errors:
            app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
            split_pages(src_file, page_range, Path(dest_dir, out_file))
    else:
        app.stop()


# Create the GUI Window
app = gui("PDF Splitter", useTtk=True)
app.setTtkTheme("default")
# Uncomment below to see all available themes
# print(app.getTtkThemes())
app.setSize(500, 200)

# Add the interactive components
app.addLabel("Choose Source PDF File")
app.addFileEntry("Input_File")

app.addLabel("Select Output Directory")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Output file name")
app.addEntry("Output_name")

app.addLabel("Page Ranges: 1,3,4-10")
app.addEntry("Page_Ranges")

# link the buttons to the function called press
app.addButtons(["Process", "Quit"], press)

# start the GUI
app.go()
