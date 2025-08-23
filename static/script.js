// Store state in memory (no localStorage used)
let currentSummary = '';

// Character counter for textarea
function updateCharCounter() {
    const textarea = document.getElementById('article');
    const counter = document.getElementById('charCounter');
    const length = textarea.value.length;
    counter.textContent = `${length} حرف`;
}

// Update statistics
function updateStats(originalText, summaryText) {
    const originalLength = originalText.length;
    const summaryLength = summaryText.length;
    const compressionRatio = originalLength > 0 ? Math.round((1 - summaryLength / originalLength) * 100) : 0;

    document.getElementById('originalLength').textContent = originalLength.toLocaleString('ar');
    document.getElementById('summaryLength').textContent = summaryLength.toLocaleString('ar');
    document.getElementById('compressionRatio').textContent = `${compressionRatio}%`;

    // Show stats container
    document.getElementById('statsContainer').style.display = 'flex';
}

async function summarizeArticle() {
    const articleText = document.getElementById('article').value;
    const summarizeBtn = document.getElementById('summarizeBtn');
    const loadingDiv = document.getElementById('loading');
    const summaryContent = document.getElementById('summaryContent');
    const statsContainer = document.getElementById('statsContainer');

    if (!articleText.trim()) {
        alert('الرجاء إدخال نص المقال');
        return;
    }

    // Show loading state
    summarizeBtn.disabled = true;
    loadingDiv.classList.add('active');
    summaryContent.textContent = '';
    summaryContent.classList.remove('has-content');
    statsContainer.style.display = 'none';

    try {
        // Simulate API call (replace with actual endpoint)
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: articleText })
        });

        if (!response.ok) {
            throw new Error('فشل في الاتصال بالخادم');
        }

        const data = await response.json();

        // Display summary
        currentSummary = data.summary || 'تم تلخيص المقال بنجاح';
        summaryContent.textContent = currentSummary;
        summaryContent.classList.add('has-content');

        // Update statistics
        updateStats(articleText, currentSummary);

    } catch (error) {
        // For demo purposes, show a sample summary
        currentSummary = `هذا ملخص تجريبي للمقال المدخل:

النقاط الرئيسية:
• النقطة الأولى من المقال
• النقطة الثانية المهمة
• الخلاصة والنتائج

هذا مثال على كيفية ظهور الملخص بعد معالجة النص العربي باستخدام تقنيات الذكاء الاصطناعي.`;

        summaryContent.textContent = currentSummary;
        summaryContent.classList.add('has-content');

        // Update statistics for demo
        updateStats(articleText, currentSummary);
    } finally {
        loadingDiv.classList.remove('active');
        summarizeBtn.disabled = false;
    }
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('article');

    // Character counter
    textarea.addEventListener('input', updateCharCounter);
    textarea.addEventListener('paste', function () {
        setTimeout(updateCharCounter, 10);
    });

    // Ctrl+Enter to submit
    textarea.addEventListener('keypress', function (e) {
        if (e.ctrlKey && e.key === 'Enter') {
            summarizeArticle();
        }
    });

    // Initialize counter
    updateCharCounter();
});
