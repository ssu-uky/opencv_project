from django import forms
from .models import ImageUploadModel


class SimpleUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    
    # ImageField Inherits all attributes and methods from FileField, but also validates that the uploaded object is a valid image.
    # file = forms.FileField()
    image = forms.ImageField() # ImageField는 FileField를 상속받아서 이미지인지 체크하고 이미지만 받음.

class ImageUploadForm(forms.ModelForm):
    # form을 통해 받아야하는 데이터 (db테이블 연결)
    class Meta:
        model = ImageUploadModel
        fields = ("description","document") #uploaded_at