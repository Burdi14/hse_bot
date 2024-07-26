import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from io import BytesIO
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

# def create_service():
#     flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json", SCOPES
#             )
#             creds = flow.run_local_server(port=5555)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     try:
#         service = build("drive", "v3", credentials=creds)
#         return service
#     except HttpError as http_error:
#         print(f'Error occured: {http_error}')

def create_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=5555)
    return build('drive', 'v3', credentials=creds)

def get_img_from_google_disk():
    service = create_service()

    results = (service.files().list(pageSize=31, fields="nextPageToken, files(id, name)").execute())
    items = results.get("files", [])

    if not items:
        print("No files found.")
        return
    print("Files:")
    for item in items:
        print(f"{item['name']} ({item['id']})"
              f"")


def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)

    fh = BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download Progress: {0}".format(int(status.progress() * 100)))
#
# service = create_service()
#
# file_id = '1zcqICbOersFOp0ABQtaa0uKsTqWMmQeS'  # Replace with the actual file ID⁠
# file_name = 'IMG_1373.JPG'  # Replace with the desired file name
#
# download_file(service, file_id, file_name)
#

