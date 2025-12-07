// 1. فحص الأمان عند تحميل الصفحة
// إذا لم يكن هناك توكن، حول المستخدم فوراً لصفحة الدخول
const token = localStorage.getItem('token');
if (!token) {
    window.location.href = '/login-page';
}

document.getElementById('predictionForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // منع إعادة تحميل الصفحة

    const resultDiv = document.getElementById('result');
    const btn = document.querySelector('button');

    // UI Loading State (تغيير الزر لحالة التحميل)
    btn.innerHTML = "Processing...";
    btn.disabled = true;
    resultDiv.style.display = 'none';

    // 2. تجميع البيانات من الحقول
    const formData = {
        MedInc: parseFloat(document.getElementById('MedInc').value),
        HouseAge: parseFloat(document.getElementById('HouseAge').value),
        AveRooms: parseFloat(document.getElementById('AveRooms').value),
        AveBedrms: parseFloat(document.getElementById('AveBedrms').value),
        Population: parseFloat(document.getElementById('Population').value),
        AveOccup: parseFloat(document.getElementById('AveOccup').value),
        Latitude: parseFloat(document.getElementById('Latitude').value),
        Longitude: parseFloat(document.getElementById('Longitude').value)
    };

    try {
        // 3. إرسال الطلب للسيرفر مع التوكن
        const response = await fetch('/api/v1/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token  // <--- هنا نرسل المفتاح
            },
            body: JSON.stringify(formData)
        });

        // 4. معالجة حالات الخطأ الخاصة بالتوكن
        if (response.status === 401) {
            // إذا قال السيرفر 401، يعني التوكن منتهي أو غير صالح
            alert("Session expired. Please login again.");
            localStorage.removeItem('token'); // احذف التوكن الخربان
            window.location.href = '/login-page';
            return;
        }

        const data = await response.json();

        // 5. عرض النتيجة
        resultDiv.style.display = 'block';

        if (response.ok) {
            // تحويل الرقم إلى سعر مقروء
            const price = (data.predicted_price * 100000).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });

            resultDiv.className = 'success';
            resultDiv.innerHTML = `💎 Estimated Property Value: <span style="font-size: 1.5em; display:block">${price}</span>`;
        } else {
            resultDiv.className = 'error';
            resultDiv.innerText = `Error: ${data.detail || 'Something went wrong'}`;
        }
    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'error';
        resultDiv.innerText = `Connection Error: ${error.message}`;
    } finally {
        // إعادة الزر لحالته الأصلية
        btn.innerHTML = "Calculate Value 💰";
        btn.disabled = false;
    }
});