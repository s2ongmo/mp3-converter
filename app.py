from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from pydub import AudioSegment

app = Flask(__name__)

# 파일 업로드를 위한 설정
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_audio(input_path, output_format):
    # input_path 파일을 읽어 들임
    audio = AudioSegment.from_file(input_path)

    # 변환된 파일의 경로를 생성
    output_path = input_path.rsplit('.', 1)[0] + '.' + output_format

    # 파일 변환 및 저장
    audio.export(output_path, format=output_format)
    return output_path


@app.route('/convert', methods=['POST'])
def convert():
    # 파일이 있는지 확인
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    # 파일 이름이 없는 경우
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # 사용자가 요청한 형식으로 파일 변환
        output_format = request.form.get('format')
        converted_file_path = convert_audio(file_path, output_format)

        # 변환된 파일을 응답으로 보내기
        return send_file(converted_file_path, as_attachment=True)

    return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=True)
