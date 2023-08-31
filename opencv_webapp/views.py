from django.shortcuts import render, redirect
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face 


def first_view(request):
    return render(request, "opencv_webapp/first_view.html", {})


def simple_upload(request):
    if request.method == "POST":
        # print(request.POST) : <QueryDict: {'csrfmiddlewaretoken': [‘~~~’], 'title': ['upload_1']}>
        # print(request.FILES) : <MultiValueDict: {'image': [<InMemoryUploadedFile: ses.jpg (image/jpeg)>]}>
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES["image"]  # 메모리에 한시적으로 저장되어있는 파일 객체
            fs = FileSystemStorage()

            # myfile.name : 'ses.jpg' (사용자가 업로드한 파일 원본의 이름)
            # filename : 'ses_cKWh3Mj.jpg' (서버에 업로드가 끝난 파일의 이름, 중복될 시 자동으로 변경됨)
            # 서버에 업로드가 끝난 이미지 파일의 URL을 얻어내 Template에게 전달

            filename = fs.save(myfile.name, myfile)  # 저장이 완료 된 파일의 이름
            uploaded_file_url = fs.url(
                filename
            )  # 저장이 완료 된 파일로 접근 가능한 URL // # '/media/ses.jpg'

            # fs.save() - fs저장 / fs.url() - 저장 끝난 파일을 접근 가능한 url 얻어내는것 / fs.delete() - fs 파일 삭제

            context = {
                "form": form,
                "uploaded_file_url": uploaded_file_url,
            }  # filled form
            return render(request, "opencv_webapp/simple_upload.html", context)

    else:  # request.method == 'GET'
        form = SimpleUploadForm()
        context = {"form": form}  # 비어있는 form 을 보여줌
        return render(request, "opencv_webapp/simple_upload.html", context)


def detect_face(request):
    if request.method == "POST":
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = ImageUploadForm(request.POST, request.FILES)  # filled form
        if form.is_valid():
            post = form.save(commit=False)
            # save() 함수는 DB에 저장될 ImageUploadModel 클래스 객체 자체를 리턴함 (== record 1건)
            # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경/추가할 수 있음 (commit=False)
            # ex) post.description = papago.translate(post.description)
            post.save()  # Form 객체('form')에 채워져 있는 데이터를 DB에 실제로 저장

            # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            imageURL = settings.MEDIA_URL + form.instance.document.name
            # == form.instance.document.url
            # == post.document.url
            # == '/media/images/2021/10/29/ses_XQAftn4.jpg'
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            return render(
                request, "opencv_webapp/detect_face.html", {"form": form, "post": post}
            )

    else:
        form = ImageUploadForm()  # empty form
        return render(request, "opencv_webapp/detect_face.html", {"form": form})
