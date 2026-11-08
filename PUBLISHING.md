# نشر SWP-BUDJET على GitHub Pages

المستودع: https://github.com/cpaswp/swp-1

1. افتح Settings داخل المستودع.
2. من القائمة الجانبية اختر Pages.
3. تحت Build and deployment اختر Source = Deploy from a branch.
4. اختر Branch = main والمجلد = /(root)، ثم اضغط Save.
5. انتظر اكتمال النشر، ثم افتح https://cpaswp.github.io/swp-1/ .
6. راجع Settings → Pages؛ يجب أن تظهر حالة Published ورابط Visit site.

المستودع عام وملف index.html موجود في الجذر. تمت إضافة .nojekyll و404.html. إذا كان Source مضبوطاً بالفعل على main /(root)، افتح Actions وتحقق من نجاح سير عمل pages build and deployment، ثم انتظر حتى 10 دقائق وأعد التحميل مع Ctrl+F5.

تنبيه: GitHub Pages يستضيف الواجهة الثابتة فقط. النسخة الحالية تحفظ البيانات في المتصفح المحلي، ولا توفر قاعدة بيانات سحابية أو مزامنة بين الأجهزة أو حسابات مستخدمين حتى يتم ربط Backend فعلي.


## ملاحظات النسخة المعدلة
- استبدل `index.html` الموجود في جذر المستودع بالملف المرفق في هذه الحزمة، مع الاحتفاظ بمجلد `worker` وملفات الإعداد.
- الدخول أصبح OTP فقط؛ لا توجد كلمة مرور مدير ثابتة داخل الواجهة. يجب ضبط Worker وفق `OTP-SETUP.md` قبل النشر الفعلي.
- استيراد Excel يتم من الشاشة المقابلة لكل ورقة وبالترتيب: Budget ثم Contracts ثم ContractAmendments ثم Claims. يمكن رفع ملف Excel نفسه في كل شاشة.
- البيانات التشغيلية ما زالت في localStorage بالمتصفح؛ لا تعتمد هذه النسخة وحدها لمشاركة البيانات بين أجهزة أو مستخدمين متعددين.
