from flask import Flask
from app.config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/*": {"origins": "*"}})  # 개발 시엔 * 허용, 운영 시엔 특정 도메인만

    # DB 관련: teardown + init 명령 등록
    from app import db
    app.teardown_appcontext(db.close_db)

    with app.app_context():
        try:
            db.init_db()
            print("✔ DB 초기화 완료 (앱 실행 중)")
        except Exception as e:
            print(f"❌ DB 초기화 실패: {e}")

    # 라우트 등록
    from app.routes.routes import bp
    from app.routes.sample import sample_bp
    app.register_blueprint(bp)
    app.register_blueprint(sample_bp)
    
    return app