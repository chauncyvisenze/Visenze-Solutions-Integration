# Visenze-Solutions-Integration

This python script creates a scheduled job to output fashion attributes into a CSV file using API /recognize method. It does the following: 
1. Identify all image files given a folder path
2. Use ViSenze's API /Recognize to extract fashion attributes 
3. Output fashion attrbitues into a CSV format with fashion attributes as column headers and fashion details as cell contents

Steps to follow before executing the script
1. Create a new folder to store all image files. Record your folder path:C:\Users\Visenze\Pictures\Saved Pictures for example. 

2. Install Python Data Analysis Library — pandas
```bash

$ pip3 install pandas

```

Running the script
```bash

$ python3 ~/dir/ViSenze_fashion_attribute.py -f ~/dir/your_folder_path -u your_ViSenze_dashboard_tagging_API_admin_Access_Key -p your_ViSenze_dashboard_tagging_API_admin_Secret_Key -o ~/dir/your_output_csv_filename

```

Scheduling an API /insert cronjob at 10am everyday 
```bash
crontab -e
```
```bash
0 10 * * * python3 ~/dir/ViSenze_fashion_attribute.py -f ~/dir/your_folder_path -u your_ViSenze_dashboard_tagging_API_admin_Access_Key -p your_ViSenze_dashboard_tagging_API_admin_Secret_Key -o ~/dir/your_output_csv_filename
```
