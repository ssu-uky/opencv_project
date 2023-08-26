from django.shortcuts import render, redirect
from .forms import SimpleUploadForm
from django.core.files.storage import FileSystemStorage


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
            
            filename = fs.save(myfile.name, myfile) # 저장이 완료 된 파일의 이름
            uploaded_file_url = fs.url(filename) # 저장이 완료 된 파일로 접근 가능한 URL // # '/media/ses.jpg' 
            
            #fs.save() - fs저장 / fs.url() - 저장 끝난 파일을 접근 가능한 url 얻어내는것 / fs.delete() - fs 파일 삭제

            context = {
                "form": form,
                "uploaded_file_url": uploaded_file_url,
            }  # filled form
            return render(request, "opencv_webapp/simple_upload.html", context)

    else:  # request.method == 'GET'
        form = SimpleUploadForm()
        context = {"form": form}  # 비어있는 form 을 보여줌
        return render(request, "opencv_webapp/simple_upload.html", context)
