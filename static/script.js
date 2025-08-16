async function summarizeArticle() {
    const articleText = document.getElementById('article').value;
    const summarizeBtn = document.getElementById('summarizeBtn');
    const loadingDiv = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');
    const summaryDiv = document.getElementById('summary');
    
    if (!articleText.trim()) {
        alert('الرجاء إدخال نص المقال');
        return;
    }
    
    // إظهار مؤشر التحميل وإخفاء النتائج
    summarizeBtn.disabled = true;
    loadingDiv.style.display = 'block';
    resultSection.style.display = 'none';
    
    try {
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: articleText })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            summaryDiv.textContent = data.summary;
            resultSection.style.display = 'block';
        } else {
            alert('حدث خطأ: ' + data.error);
        }
    } catch (error) {
        alert('فشل الاتصال بالخادم: ' + error.message);
    } finally {
        loadingDiv.style.display = 'none';
        summarizeBtn.disabled = false;
    }
}

// السماح بالضغط على Enter لإرسال النموذج
document.getElementById('article').addEventListener('keypress', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        summarizeArticle();
    }
});