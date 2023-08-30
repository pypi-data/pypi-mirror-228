import requests
import base64
from PIL import Image
import io

def submit(id_student, name, assignment_name, result, question_name='', code=''):
    data = {
        "id": id_student,
        "name": name,
        "assignment_name": assignment_name,
        "question_name": question_name,
        "code": code,
        "result": result
    }

    r = requests.post('https://ai-grader-ihcwj2lvaq-as.a.run.app/submission/submit/bquery', json=data)
    if r.status_code == 200:
        return 'Assignment successfully submitted'
    else:
        return 'Failed to submit assignment'

def submit_image(id, question_name, image_path):
    image = Image.open(image_path).convert('RGB')
    image_byte_arr = io.BytesIO()
    
    image.save(image_byte_arr, format='JPEG')
    image_byte_arr = image_byte_arr.getvalue()
    
    image_base64 = base64.b64encode(image_byte_arr).decode()
    
    data = {
        "id": id,
        "question_name": question_name,
        "image_base64": image_base64,
    }
    
    r = requests.post('https://ai-grader-ihcwj2lvaq-as.a.run.app/submission/submit/gdrive', json=data)
    if r.status_code == 200:
        return 'Assignment successfully submitted'
    else:
        return 'Failed to submit assignment'