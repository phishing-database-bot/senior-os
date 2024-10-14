import os, time, tarfile, requests
from datetime import datetime, timedelta

# This method will check if the phishing database is up to date
class PhishingDatabaseModificationChecker:
    def __init__(self,my_config_data,input_from_main_url_logger):
        self.url_logger = input_from_main_url_logger
        # Get path to file SWEB_PHISH_1.txt
        self.path_to_phishing_database = my_config_data["phishing_database"]["path"]
        url_to_tar_github = my_config_data["phishing_database"]["path_to_tar_github"]

        # Create update file
        self.database_updater = FileUpdater(url_to_tar_github, self.path_to_phishing_database,self.url_logger)
    
    # Get the last modified time of the phishing database
    def get_last_modification_time(self):
        # Returns as a datetime object.
        # Check if the file is existed
        if not os.path.exists(self.path_to_phishing_database):
            raise FileNotFoundError(self.url_logger.log_blocked_url('WEBBROWSER', 2, 'UpdatePhishingTXT', f'File path not found {self.file_path_to_txt}'))
        else:
            # Get the last modificated time
            last_update_time = os.path.getmtime(self.path_to_phishing_database)
            
            # Using fromtimestamp to change it to Calender
            return datetime.fromtimestamp(last_update_time)
    
    # Returns True if modified after check_time, False otherwise.
    def file_has_been_modified_since(self, compared_time):
        return self.get_last_modification_time() > compared_time

    # Methoud check if the file was last modified more than 2 weeks ago
    def check_and_update_if_needed(self):
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        if not self.file_has_been_modified_since(two_weeks_ago):
            self.database_updater.download_and_extract_from_github()

# Method for updating phishing database
class FileUpdater:
    def __init__(self, github_url, path_to_database,input_url_logger):
        self.url_logger = input_url_logger
        self.github_url = github_url
        self.txt_path = path_to_database
        self.max_attempts = 2
        # Set delay after redirect HTTP
        self.delay_betwween_attempts = 0.1

    # Method for download the .gz file from GitHub and extract its contents to a .txt file.
    def download_and_extract_from_github(self):
        for attempt in range(self.max_attempts):
            try:
                # Connect to file_github and download
                http_response = requests.get(self.github_url, stream=True)
                # HTTPError object if an error has occurred during the process.
                http_response.raise_for_status()
                
                # Set file temp
                temp_gz_filename = "downloaded_phishing_database_temp.tar.gz"
                # Write to file temp
                with open(temp_gz_filename, "wb") as temp_file:
                    for chunk in http_response.iter_content(chunk_size=1024):
                        temp_file.write(chunk)
                
                # Extract file to .txt
                try:
                    with tarfile.open(temp_gz_filename, "r") as tar_file:
                        for member in tar_file.getmembers():
                            extracted_file = tar_file.extractfile(member)
                            if extracted_file:
                                with open(self.txt_path, "wb") as txt_file:
                                    txt_file.write(extracted_file.read())
                    # Remove file temp
                    os.remove(temp_gz_filename)
                    # Break for if the first HTTP is succeed
                    break
                except tarfile.ReadError:
                    self.url_logger.log_blocked_url('WEBBROWSER', 2, 'UpdatePhishingTXT', f'Can not open and write file tar {temp_gz_filename}')
            except (requests.ConnectionError, requests.HTTPError) as excep:
                if attempt < self.max_attempts -1:
                    # Wait for the specified delay before retrying
                    time.sleep(self.delay_betwween_attempts)  
                else:
                    self.url_logger.log_blocked_url("WEBBROWSER",2,"UpdatePhishingTXT",f'Can not update SWEB_PHISHING_1.txt')
