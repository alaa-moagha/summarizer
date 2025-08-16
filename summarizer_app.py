from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# استخدام النموذج المحلي المحسّن
MODEL_PATH = "./model"  # تأكد أن مجلد النموذج موجود هنا
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
    
    # نقل النموذج إلى GPU إذا كان متاحًا
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    print("✅ تم تحميل النموذج بنجاح!")
    
except Exception as e:
    print(f"❌ خطأ في تحميل النموذج: {e}")
    exit(1)

def summarize_text(text, max_length=150, min_length=50):
    # تحضير النص لإدخال النموذج (حسب طريقة تدريب نموذجك)
    # جرب إحدى الطريقتين:
    
    # الطريقة 1: إذا كان مدرب على مهمة summarization مباشرة
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    
    # الطريقة 2: إذا كان بحاجة لـ prefix (فكoment الأسطر التالية إذا لزم)
    # input_text = f"summarize: {text}"
    # inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
    
    inputs = inputs.to(device)
    
    with torch.no_grad():
        summary_ids = model.generate(
            inputs, 
            max_length=max_length, 
            min_length=min_length, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True,
            do_sample=False  # لتلخيص ثابت
        )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data['text']
        
        if not text.strip():
            return jsonify({'error': 'الرجاء إدخال نص للمقال'}), 400
        
        # التحقق من طول النص
        if len(text) < 30:
            return jsonify({'error': 'النص قصير جداً للتلخيص'}), 400
            
        summary = summarize_text(text)
        return jsonify({'summary': summary})
    
    except Exception as e:
        print(f"خطأ في التلخيص: {e}")  # للتصحيح
        return jsonify({'error': f'حدث خطأ أثناء التلخيص: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
