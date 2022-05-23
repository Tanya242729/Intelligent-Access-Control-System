#import pyttsx3
import cv2
import datetime
import time
#import playsound
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
import pygame
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from ibmcloudant.cloudant_v1 import CloudantV1
from ibmcloudant import CouchDbSessionAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" #
Current list avaiable at
https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID =
"QK-6lL2JX1TK7yjNZJCi0GEcrUbVlKbbZJIah_OyVx-A" # eg
"W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_INSTANCE_CRN =
"crn:v1:bluemix:public:iam-identity::a/e296b12a0dfa4ddfbe54f3d5eca9badb::s
Page No : 18
erviceid:ServiceId-aa9e5973-a4e1-405f-94e3-7c976e56a6d1" # eg
"crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c
3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"
# Create resource
cos = ibm_boto3.resource("s3",
ibm_api_key_id=COS_API_KEY_ID,
ibm_service_instance_id=COS_INSTANCE_CRN,
config=Config(signature_version="oauth"),
endpoint_url=COS_ENDPOINT
)
authenticator =
BasicAuthenticator('apikey-v2-qy5qcpihygwozrugn8t18q4j8owzr269lxi4rkjmb
c1', '220fd8d9797d68fd912dd4d7bd1ecdd0')
service = CloudantV1(authenticator=authenticator)
service.set_service_url('https://apikey-v2-qy5qcpihygwozrugn8t18q4j8owzr269
lxi4rkjmbc1:220fd8d9797d68fd912dd4d7bd1ecdd0@341e9043-5fc4-47e8-8d6
5-ae1a1c302533-bluemix.cloudantnosqldb.appdomain.cloud')
bucket = "sharonhelmet"
def multi_part_upload(bucket_name, item_name, file_path):
try:
print("Starting file transfer for {0} to bucket: {1}\n".format(item_name,
bucket_name))
# set 5 MB chunks
part_size = 1024 * 1024 * 5
# set threadhold to 15 MB
file_threshold = 1024 * 1024 * 15
# set the transfer threshold and chunk size
transfer_config = ibm_boto3.s3.transfer.TransferConfig(
multipart_threshold=file_threshold,
multipart_chunksize=part_size
Page No : 19
)
# the upload_fileobj method will automatically execute a multi-part upload
# in 5 MB chunks for all files over 15 MB
with open(file_path, "rb") as file_data:
cos.Object(bucket_name, item_name).upload_fileobj(
Fileobj=file_data,
Config=transfer_config
)
print("Transfer for {0} Complete!\n".format(item_name))
except ClientError as be:
print("CLIENT ERROR: {0}\n".format(be))
except Exception as e:
print("Unable to complete multi-part upload: {0}".format(e))
# This is how you authenticate.
metadata = (('authorization', 'Key 62ab2f4fa9bf46f487fa50bdf63deaf2'),)
#face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#eye_classifier=cv2.CascadeClassifier("haarcascade_eye.xml")
#It will read the first frame/image of the video
video=cv2.VideoCapture(0)
while True:
check,frame=video.read()
gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow('Face detection', frame)
picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
cv2.imwrite("helmet777.jpg",frame)
with
open(r'C:\Users\Sharon\Desktop\SmartInternz-IoT\VIT-cv2\Haar_cascade\helm
et777.jpg', "rb") as f:
file_bytes = f.read()
request = service_pb2.PostModelOutputsRequest(
Page No : 20
# This is the model ID of a publicly available General model. You may
use any other public or custom model ID.
model_id='aaa03c23b3724a16a56b629203edc62c',
inputs=[
resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(ba
se64=file_bytes)))
])
response = stub.PostModelOutputs(request, metadata=metadata)
if response.status.code != status_code_pb2.SUCCESS:
raise Exception("Request failed, status code: " + str(response.status.code))
a= []
for concept in response.outputs[0].data.concepts:
if(concept.value > 0.8):
a.append(concept.name)
#print(a)
t=1
for i in a:
if(i == "person" or i == "people"):
#print("Person is detected")
for j in a:
if j == "helmet":
print("Person is wearing the helmet and you are allowed into the
industry")
#engine.say("Person is wearing the helmet and you are allowed
into the industry")
#engine.runAndWait()
t=1
break
else:
t=0
Page No : 21
if(t==0):
print("Person is not wearing the helmet")
print('Playing..')
pygame.mixer.init()
pygame.mixer.music.load('new1.mp3')
pygame.mixer.music.play()
while not(pygame.mixer.music.get_busy()):
pygame.mixer.quit()
picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
cv2.imwrite(picname+".jpg",frame)
multi_part_upload('sharonhelmet', picname+'.jpg', picname+'.jpg')
json_document={"link":COS_ENDPOINT+'/'+bucket+'/'+picname+'.jpg'}
response = service.post_document(db="helmet1",
document=json_document).get_result()
elif(t==1):
break
#drawing rectangle boundries for the detected eyes
#for(ex,ey,ew,eh) in eyes:
#cv2.rectangle(frame, (ex,ey), (ex+ew,ey+eh), (127,0,255), 2)
#cv2.imshow('Face detection', frame)
#waitKey(1)- for every 1 millisecond new frame will be captured
Key=cv2.waitKey(1000)
if Key==ord('q'):
#release the camera
video.release()
#destroy all windows
cv2.destroyAllWindows()
break
