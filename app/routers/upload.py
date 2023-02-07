from fastapi import APIRouter,HTTPException,UploadFile,status,File
# import magic
from uuid import uuid4
import boto3
from loguru import logger



AWS_BUCKET = 'betit'
s3=boto3.resource("s3")
bucket=s3.Bucket(AWS_BUCKET)

mime_file_type ={
    'image/png':'png',
     'image/jpeg':'jpg',
     'application/pdf':'pdf'
}

async def upload_s3(content:bytes,key:str):
    logger.info(f"upload {key} to s3 bucket {AWS_BUCKET}")
    bucket.put_object(Key=key,Body=content)


router=APIRouter()

# # @router.post("/upload", tags=["Phase3 backend"])
# async def upload(file:UploadFile|None=None):
#     if not file:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="no file")
#     content = await file.read()
#     file_type = magic.from_buffer(buffer=content,mime=True)
#     if(file_type not in mime_file_type):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"file type {file_type} noot support, only support {mime_file_type}")
#     print(f"{uuid4()}.{mime_file_type[file_type]}")
#     await upload_s3(content=content,key=f"{uuid4()}.{mime_file_type[file_type]}")

#      return {"crypto index"}


@router.post("/upload_from_html", tags=["Phase3 backend"])
async def upload_from_html(file:bytes= File(),name:str=File(),message:str=File()):
    await upload_s3(content=file,key=name.split("\\")[-1])
    return {f"upload {name} to s3"}

@router.get("/get_info_from_database",tags=["Phase3 backend"])
async def get_info_from_database():
    pass