from flask import Blueprint, request, jsonify, Response
from app.services.mbti_service import analyze_mbti_personality
from app.services.topic_analysis import extract_topic_metrics
from app.services.conversation_pattern import extract_pattern_metrics
import os
from app.db import get_db
import json
from app.services.basic import extract_speaker

bp = Blueprint('bp', __name__)

UPLOAD_DIR = os.path.abspath('./uploads')  # 절대 경로로 변환

@bp.route('/file', methods=['POST'])
def file():    
    # 파일 받기
    chat_file = request.files.get('chat_file')
    if not chat_file:
        return jsonify({'error': '파일이 없습니다.'}), 400

    # 파일 저장
    file_path = os.path.join(UPLOAD_DIR, chat_file.filename)
    chat_file.save(file_path)

    print(f"파일 저장 완료: {file_path}")
    speakers = extract_speaker(file_path)

    return jsonify({
        'status': 'success',
        'message': '저장 성공',
        'speakers': speakers,
        'uploaded_filename': chat_file.filename
    }), 200
    
@bp.route('/analyze', methods=['POST'])
def analyze():
    # 사용자 정보 받기
    my_name = request.form.get('my_name')
    my_mbti = request.form.get('my_mbti')
    my_gender = request.form.get('my_gender')
    partner_name = request.form.get('partner_name')
    partner_mbti = request.form.get('partner_mbti')
    partner_gender = request.form.get('partner_gender')
    filename = request.form.get('filename')

    file_path = os.path.join(UPLOAD_DIR, filename)
    
    db = get_db()
    cursor = db.execute('INSERT INTO info (user_name,user_mbti,user_gender,partner_name,partner_mbti,partner_gender,file_name) VALUES (?,?,?,?,?,?,?)'
               , (my_name,my_mbti,my_gender,partner_name,partner_mbti,partner_gender,file_path,))
    db.commit()

    new_user_id = cursor.lastrowid  # 자동 증가된 ID

    # 응답 반환
    return jsonify({
        'status': 'success',
        'message': '저장 성공',
        'id': new_user_id,
        'my_info': {
            'name': my_name,
            'mbti': my_mbti,
            'gender': my_gender
        },
        'partner_info': {
            'name': partner_name,
            'mbti': partner_mbti,
            'gender': partner_gender
        },
        'uploaded_filename': filename
    })

@bp.route('/analyze-mbti/<string:id>', methods=['GET'])
def analyze_mbti(id):
    db = get_db()
    info = db.execute('SELECT * FROM info WHERE id = ?', (id,)).fetchone()

    partner_name = info["partner_name"]
    partner_mbti = info["partner_mbti"] or None
    partner_gender = info["partner_gender"] or None

    user_name = info["user_name"]
    user_mbti = info["user_mbti"] or None
    user_gender = info["user_gender"] or None

    mbti_str = f", MBTI는 {partner_mbti}" if partner_mbti else ""
    gender_str = f", 성별은 {partner_gender}" if partner_gender else ""

    p_profile = f"상대방 이름은 {partner_name} {mbti_str} {gender_str}입니다."

    user_mbti_str = f", 나의 MBTI는 {user_mbti}" if user_mbti else ""
    user_gender_str = f", 나의 성별은 {user_gender}" if user_gender else ""
    
    profile = f"{p_profile} 나의 이름은 {user_name} {user_mbti_str} {user_gender_str}입니다"

    #content = data.get("content")
    file_path = os.path.join(UPLOAD_DIR, info["file_name"])
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    result = analyze_mbti_personality(profile, file_path)

    print(result)
    return jsonify({"result": result})

# @bp.route('/topic/<string:file_name>', methods=['GET'])
# def topic(file_name):
#     file_path = os.path.join(UPLOAD_DIR, file_name)
    
#     result = extract_topic_metrics(file_path)
#     return Response(
#         json.dumps(result, ensure_ascii=False),
#         content_type='application/json; charset=utf-8'
#     )

# @bp.route('/pattern/<string:file_name>', methods=['GET'])
# def pattern(file_name):
#     file_path = os.path.join(UPLOAD_DIR, file_name)
    
#     result = extract_pattern_metrics(file_path)
#     return Response(
#         json.dumps(result, ensure_ascii=False),
#         content_type='application/json; charset=utf-8'
#     )

@bp.route('/topic/<string:id>', methods=['GET'])
def topic(id):
    db = get_db()
    info = db.execute('SELECT * FROM info WHERE id = ?', (id,)).fetchone()

    file_path = os.path.join(UPLOAD_DIR, info["file_name"])
    
    result = extract_topic_metrics(file_path)
    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )

@bp.route('/pattern/<string:id>', methods=['GET'])
def pattern(id):
    db = get_db()
    info = db.execute('SELECT * FROM info WHERE id = ?', (id,)).fetchone()

    file_path = os.path.join(UPLOAD_DIR, info["file_name"])
    
    result = extract_pattern_metrics(file_path)
    return Response(
        json.dumps(result, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )