import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

lessons_db = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>منصة كلية الشريعة - خروبة</title>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-base: #030a07;
                --gold-primary: #f3c68f;
                --gold-glow: #d4af37;
                --card-glass: rgba(10, 26, 18, 0.75);
                --border-glass: rgba(243, 198, 143, 0.18);
                --text-main: #f4f9f5;
                --text-muted: #95b8a6;
            }
            body { 
                font-family: 'Amiri', serif; 
                background: var(--bg-base);
                background-image: 
                    radial-gradient(circle at 10% 10%, rgba(27, 67, 50, 0.5) 0%, transparent 40%),
                    radial-gradient(circle at 90% 90%, rgba(212, 175, 55, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 50% 50%, rgba(15, 42, 29, 0.8) 0%, #030a07 100%);
                margin: 0; padding: 35px 15px; text-align: center; color: var(--text-main); 
                display: flex; flex-direction: column; min-height: 85vh; justify-content: space-between; background-attachment: fixed;
            }
            .wrapper { max-width: 540px; margin: 0 auto; width: 100%; }
            .container { 
                background: var(--card-glass); padding: 35px 28px; border-radius: 28px; 
                box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6), 0 0 50px rgba(27, 67, 50, 0.3); 
                border: 1px solid var(--border-glass); text-align: right; backdrop-filter: blur(25px); position: relative; overflow: hidden;
            }
            .logo-container { text-align: center; margin-bottom: 25px; }
            .logo-container img { width: 100%; max-width: 100%; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); border: 1px solid rgba(243,198,143,0.3); }
            .category-title {
                font-size: 20px; color: var(--gold-primary); margin: 0 0 18px 0; font-weight: 700; 
                border-bottom: 1px solid rgba(243, 198, 143, 0.2); padding-bottom: 12px; display: flex; align-items: center; gap: 12px;
            }
            .category-title span.icon {
                background: linear-gradient(135deg, #1b4332, #0f2a1d); color: var(--gold-primary); 
                width: 40px; height: 40px; display: inline-flex; align-items: center; justify-content: center; border-radius: 14px; font-size: 16px; border: 1px solid rgba(243, 198, 143, 0.3);
            }
            .btn { 
                display: block; background: linear-gradient(135deg, rgba(45, 106, 79, 0.85) 0%, rgba(27, 67, 50, 0.95) 100%); 
                color: var(--text-main); padding: 16px 22px; margin: 14px 0; text-decoration: none; border-radius: 16px; 
                font-size: 18px; font-weight: 700; transition: all 0.4s ease; text-align: center; border: 1px solid rgba(255, 255, 255, 0.08);
            }
            .btn:hover { 
                transform: translateY(-4px) scale(1.01); background: linear-gradient(135deg, rgba(64, 145, 108, 0.9) 0%, rgba(45, 106, 79, 1) 100%); 
                border-color: var(--gold-glow); color: #ffffff;
            }
            .btn-secondary { background: linear-gradient(135deg, rgba(30, 70, 52, 0.85) 0%, rgba(15, 42, 29, 0.95) 100%); }
            footer { font-size: 13px; color: var(--text-muted); margin-top: 35px; font-weight: 700; }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="container">
                <div class="logo-container">
                    <img src="https://share.google/7efEujTvKRzdKDguT" alt="شعار منصة كلية الشريعة">
                </div>
                <div class="category-title"><span class="icon">🏛️</span> اختر السداسي الدراسي</div>
                <a href="/semester1" class="btn">السداسي الأول (أو الخامس)</a>
                <a href="#" class="btn btn-secondary" style="opacity: 0.5; cursor: not-allowed;" onclick="return false;">السداسي الثاني</a>
            </div>
        </div>
        <footer>جميع الحقوق محفوظة منصة كلية الشريعة © 2026</footer>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/semester1')
def semester1():
    html_content = '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>السداسي الخامس - السنة الثالثة فقه وأصوله</title>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-base: #030a07;
                --gold-primary: #f3c68f;
                --gold-glow: #d4af37;
                --card-glass: rgba(10, 26, 18, 0.75);
                --border-glass: rgba(243, 198, 143, 0.18);
                --text-main: #f4f9f5;
                --text-muted: #95b8a6;
            }
            body { 
                font-family: 'Amiri', serif; background: var(--bg-base);
                background-image: 
                    radial-gradient(circle at 10% 10%, rgba(27, 67, 50, 0.5) 0%, transparent 40%),
                    radial-gradient(circle at 90% 90%, rgba(212, 175, 55, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 50% 50%, rgba(15, 42, 29, 0.8) 0%, #030a07 100%);
                margin: 0; padding: 35px 15px; text-align: center; color: var(--text-main); 
                display: flex; flex-direction: column; min-height: 85vh; justify-content: space-between; background-attachment: fixed;
            }
            .wrapper { max-width: 540px; margin: 0 auto; width: 100%; }
            .top-nav { display: flex; justify-content: flex-start; margin-bottom: 22px; }
            .back-home-btn {
                background: rgba(15, 42, 29, 0.6); backdrop-filter: blur(16px); color: var(--gold-primary); 
                padding: 11px 22px; border-radius: 16px; text-decoration: none; font-size: 16px; font-weight: 700; 
                border: 1px solid var(--border-glass); transition: 0.3s; display: inline-flex; align-items: center; gap: 8px;
            }
            .back-home-btn:hover { background: rgba(27, 67, 50, 0.9); border-color: var(--gold-glow); color: #fff; }
            .container { 
                background: var(--card-glass); padding: 45px 28px; border-radius: 28px; 
                box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6); border: 1px solid var(--border-glass); text-align: right; backdrop-filter: blur(25px); 
            }
            .category-title {
                font-size: 20px; color: var(--gold-primary); margin: 38px 0 18px 0; font-weight: 700; 
                border-bottom: 1px solid rgba(243, 198, 143, 0.2); padding-bottom: 12px; display: flex; align-items: center; gap: 12px;
            }
            .category-title:first-of-type { margin-top: 0; }
            .category-title span.icon {
                background: linear-gradient(135deg, #1b4332, #0f2a1d); color: var(--gold-primary); 
                width: 40px; height: 40px; display: inline-flex; align-items: center; justify-content: center; border-radius: 14px; font-size: 16px; border: 1px solid rgba(243, 198, 143, 0.3);
            }
            .btn { 
                display: block; background: linear-gradient(135deg, rgba(45, 106, 79, 0.85) 0%, rgba(27, 67, 50, 0.95) 100%); 
                color: var(--text-main); padding: 16px 22px; margin: 14px 0; text-decoration: none; border-radius: 16px; 
                font-size: 18px; font-weight: 700; transition: all 0.4s ease; text-align: center; border: 1px solid rgba(255, 255, 255, 0.08);
            }
            .btn:hover { 
                transform: translateY(-3px); background: linear-gradient(135deg, rgba(64, 145, 108, 0.9) 0%, rgba(45, 106, 79, 1) 100%); 
                border-color: var(--gold-glow); color: #ffffff;
            }
            .btn-secondary { background: linear-gradient(135deg, rgba(30, 70, 52, 0.85) 0%, rgba(15, 42, 29, 0.95) 100%); }
            footer { font-size: 13px; color: var(--text-muted); margin-top: 35px; font-weight: 700; }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="top-nav">
                <a href="/" class="back-home-btn"><span>← الرئيسية</span></a>
            </div>
            <div class="container">
                <div class="category-title"><span class="icon">📜</span> أعمال توجيهية (تطبيق TD)</div>
                <a href="/module/quran_tp" class="btn">ترتيل و حفظ القرآن</a>
                <a href="/module/arabic_tp" class="btn">لغة عربية (بلاغة)</a>
                <a href="/module/qawaid_tp" class="btn">قواعد تفسير النصوص</a>
                <a href="/module/mawarith_tp" class="btn">المواريث</a>
                <a href="/module/fiqh_tp" class="btn">فقه مقارن</a>
                <a href="/module/contemporary_tp" class="btn">قضايا فقهية معاصرة</a>
                <a href="/module/english_tp" class="btn">لغة أجنبية (إنجليزية)</a>

                <div class="category-title" style="margin-top: 42px;"><span class="icon">🏛️</span> محاضرات (Cours)</div>
                <a href="/module/qawaid_lec" class="btn btn-secondary">قواعد تفسير النصوص</a>
                <a href="/module/contemporary_lec" class="btn btn-secondary">قضايا فقهية معاصرة</a>
                <a href="/module/mawarith_lec" class="btn btn-secondary">المواريث</a>
                <a href="/module/maqasid_lec" class="btn btn-secondary">مقاصد الشريعة</a>
                <a href="/module/judiciary_lec" class="btn btn-secondary">النظام القضائي</a>
                <a href="/module/tafseer_lec" class="btn btn-secondary">التفسير و الحديث الموضوعي</a>
                <a href="/module/governance_lec" class="btn btn-secondary">الحوكمة و أخلاقيات المهنة</a>
            </div>
        </div>
        <footer>جميع الحقوق محفوظة منصة كلية الشريعة © 2026</footer>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/module/<module_name>')
def manage_module(module_name):
    names_map = {
        'quran_tp': 'ترتيل و حفظ القرآن',
        'arabic_tp': 'لغة عربية (بلاغة)',
        'qawaid_tp': 'قواعد تفسير النصوص (TD)',
        'mawarith_tp': 'المواريث (TD)',
        'fiqh_tp': 'فقه مقارن (TD)',
        'contemporary_tp': 'قضايا فقهية معاصرة (TD)',
        'english_tp': 'لغة أجنبية (إنجليزية)',
        'qawaid_lec': 'قواعد تفسير النصوص (محاضرات)',
        'contemporary_lec': 'قضايا فقهية معاصرة (محاضرات)',
        'mawarith_lec': 'المواريث (محاضرات)',
        'maqasid_lec': 'مقاصد الشريعة (محاضرات)',
        'judiciary_lec': 'النظام القضائي (محاضرات)',
        'tafseer_lec': 'التفسير و الحديث الموضوعي',
        'governance_lec': 'الحوكمة و أخلاقيات المهنة'
    }
    
    display_name = names_map.get(module_name, 'إدارة محتوى المقياس')
    module_lessons = lessons_db.get(module_name, [])

    lessons_html = ""
    if module_lessons:
        for item in module_lessons:
            file_url = url_for('uploaded_file', filename=item['filename'])
            lessons_html += f'''
            <div style="background: rgba(15, 42, 29, 0.8); border: 1px solid rgba(243, 198, 143, 0.25); padding: 15px; border-radius: 12px; margin-top: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0 0 5px 0; color: var(--gold-primary); font-size: 17px;">{item['title']}</h4>
                    <span style="font-size: 12px; color: var(--text-muted);">ملف مرفق</span>
                </div>
                <a href="{file_url}" target="_blank" style="background: var(--gold-primary); color: #030a07; padding: 6px 14px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px;">عرض / تحميل</a>
            </div>
            '''
    else:
        lessons_html = '<p class="no-lessons">لا توجد دروس مرفوعة حتى الآن.</p>'

    html_content = f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{display_name} - منصة كلية الشريعة</title>
        <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-base: #030a07;
                --gold-primary: #f3c68f;
                --gold-glow: #d4af37;
                --card-glass: rgba(10, 26, 18, 0.75);
                --border-glass: rgba(243, 198, 143, 0.18);
                --text-main: #f4f9f5;
                --text-muted: #95b8a6;
            }}
            body {{ 
                font-family: 'Amiri', serif; background: var(--bg-base);
                background-image: 
                    radial-gradient(circle at 10% 10%, rgba(27, 67, 50, 0.5) 0%, transparent 40%),
                    radial-gradient(circle at 90% 90%, rgba(212, 175, 55, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 50% 50%, rgba(15, 42, 29, 0.8) 0%, #030a07 100%);
                margin: 0; padding: 25px 15px; text-align: center; color: var(--text-main); 
                display: flex; flex-direction: column; min-height: 85vh; justify-content: space-between; background-attachment: fixed;
            }}
            .wrapper {{ max-width: 540px; margin: 0 auto; width: 100%; }}
            .top-nav {{ display: flex; justify-content: flex-start; margin-bottom: 15px; }}
            .back-btn {{
                background: rgba(15, 42, 29, 0.7); backdrop-filter: blur(16px); color: var(--gold-primary); 
                padding: 8px 16px; border-radius: 12px; text-decoration: none; font-size: 15px; font-weight: 700; 
                border: 1px solid var(--border-glass); transition: 0.3s; display: inline-flex; align-items: center; gap: 6px;
            }}
            .back-btn:hover {{ background: rgba(27, 67, 50, 0.9); border-color: var(--gold-glow); color: #fff; }}
            .container {{ 
                background: var(--card-glass); padding: 30px 22px; border-radius: 24px; 
                box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6); border: 1px solid var(--border-glass); text-align: right; backdrop-filter: blur(25px);
            }}
            .module-title {{
                font-size: 20px; color: var(--gold-primary); margin: 0 0 18px 0; font-weight: 700; 
                border-bottom: 1px solid rgba(243, 198, 143, 0.2); padding-bottom: 10px; text-align: center;
            }}
            .upload-box {{
                background: rgba(15, 42, 29, 0.6); border: 1px dashed rgba(243, 198, 143, 0.35); padding: 20px; border-radius: 18px; margin-bottom: 20px;
            }}
            .input-field {{
                width: 100%; background: rgba(10, 26, 18, 0.8); border: 1px solid rgba(243, 198, 143, 0.25); 
                padding: 12px 15px; border-radius: 12px; color: var(--text-main); font-family: 'Amiri', serif; font-size: 16px; box-sizing: border-box; margin-bottom: 12px; outline: none;
            }}
            .input-field::placeholder {{ color: var(--text-muted); }}
            .file-label {{
                display: block; background: linear-gradient(135deg, rgba(30, 70, 52, 0.9), rgba(15, 42, 29, 0.9)); 
                border: 1px solid rgba(243, 198, 143, 0.3); padding: 12px; border-radius: 12px; text-align: center; 
                color: var(--gold-primary); cursor: pointer; font-weight: 700; font-size: 16px; transition: 0.3s; margin-bottom: 12px;
            }}
            .file-label:hover {{ background: linear-gradient(135deg, rgba(45, 106, 79, 1), rgba(30, 70, 52, 1)); border-color: var(--gold-glow); color: #fff; }}
            .submit-btn {{
                display: block; width: 100%; background: linear-gradient(135deg, rgba(45, 106, 79, 0.9), rgba(27, 67, 50, 1)); 
                color: var(--text-main); padding: 12px; border: none; border-radius: 12px; font-size: 17px; font-weight: 700; 
                font-family: 'Amiri', serif; cursor: pointer; border: 1px solid var(--border-glass); transition: 0.3s;
            }}
            .submit-btn:hover {{ background: linear-gradient(135deg, rgba(64, 145, 108, 1), rgba(45, 106, 79, 1)); border-color: var(--gold-glow); color: #fff; }}
            .no-lessons {{ text-align: center; color: var(--text-muted); font-size: 15px; padding: 20px 0; margin: 0; }}
            footer {{ font-size: 13px; color: var(--text-muted); margin-top: 25px; font-weight: 700; }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="top-nav">
                <a href="/semester1" class="back-btn">← العودة للسداسي الأول</a>
            </div>

            <div class="container">
                <div class="module-title">📖 {display_name}</div>
                
                <div class="upload-box">
                    <form action="/upload_lesson/{module_name}" method="POST" enctype="multipart/form-data">
                        <input type="text" name="lesson_title" class="input-field" placeholder="أدخل عنوان الدرس (مثال: محاضرة المدخل)" required>
                        
                        <label for="file-input" class="file-label">
                            📁 اضغط لاختيار صورة أو ملف PDF
                        </label>
                        <input type="file" id="file-input" name="lesson_file" accept="image/*,.pdf" required style="display: none;">
                        
                        <button type="submit" class="submit-btn">نشر الدرس / الملف</button>
                    </form>
                </div>

                <div style="text-align: right; margin-top: 15px;">
                    <h3 style="color: var(--gold-primary); font-size: 17px; border-bottom: 1px solid rgba(243,198,143,0.15); padding-bottom: 8px;">الدروس والمحاضرات المتاحة:</h3>
                    {lessons_html}
                </div>
            </div>
        </div>
        <footer>جميع الحقوق محفوظة منصة كلية الشريعة © 2026</footer>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/upload_lesson/<module_name>', methods=['POST'])
def upload_lesson(module_name):
    if 'lesson_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['lesson_file']
    lesson_title = request.form.get('lesson_title', 'درس بدون عنوان')

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if module_name not in lessons_db:
            lessons_db[module_name] = []

        lessons_db[module_name].append({
            'title': lesson_title,
            'filename': filename
        })

    return redirect(url_for('manage_module', module_name=module_name))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
