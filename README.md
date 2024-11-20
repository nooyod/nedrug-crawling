# Image Downloader for `nedrug.mfds.go.kr`

This Python script downloads images from the **`nedrug.mfds.go.kr`** website based on a list of IDs provided in a CSV file. Images are saved locally, and the CSV is updated with the relative paths of the downloaded images. The script supports handling Base64-encoded images embedded in HTML.

## Features

- Downloads Base64-encoded images from the target website.
- Saves images to a specified folder.
- Updates the input CSV with the relative paths to the saved images.
- Handles missing or invalid image data gracefully by logging errors in the CSV file.
- Supports processing specific rows of the CSV file, allowing for segmented execution of large datasets.

## Requirements

There are 2 ways to prepare the script
1. vscode devcontainer
    - Python 3.12-bullseye. from mcr.microsoft.com
2. Python 3.8 or higher
    ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Prepare Input CSV File**  
   Ensure the input CSV file has a column named `ID` containing the IDs to be processed. Add an empty column named `PATH` for the script to update with the downloaded image paths.

2. **Modify Script Parameters**  
   Open the script and update the following variables:
   - `CSV_INPUT`: Path to the input CSV file.
   - `CSV_OUTPUT`: Path to save the updated CSV file.
   - `INDEX_START`: Start row index to process.
   - `INDEX_END`: End row index to process (exclusive).
   - `IMAGE_FOLDER`: Folder to save the downloaded images.

3. **Run the Script**  
   Execute the script:

   ```bash
   python main.py
   ```

4. **Check Results**  
   - Images are saved in the specified folder (default: `images`).
   - The output CSV file is updated with the image paths in the `PATH` column. Rows with missing or invalid image data will have the value `not exists` or `ERROR` in the `PATH` column.

## Example

Given the following input `test.csv`:

| ID        | PATH      |
|-----------|-----------|
| 200503642 |           |
| 200503643 |           |
| 200503644 |           |

After running the script, the CSV is updated:

| ID        | PATH          |
|-----------|---------------|
| 200503642 | 200503642.jpg |
| 200503643 | not exists    |
| 200503644 | 200503644.jpg |

## Notes

- The script processes Base64-encoded images embedded in the website’s HTML. Non-Base64 image URLs are not supported.
- The script automatically creates the specified image folder if it does not exist.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Let me know if you want any additional sections or formatting changes!