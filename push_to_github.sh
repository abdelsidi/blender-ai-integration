#!/bin/bash
# سكربت لرفع المشروع على GitHub

echo "🚀 رفع مشروع Blender AI Integration على GitHub"
echo "================================================"
echo ""

cd /home/vboxuser/.openclaw/workspace/blender-ai-integration

# التأكد من الـ remote
echo "🔗 التحقق من إعدادات GitHub..."
git remote -v

echo ""
echo "📝 للرفع، اختر إحدى الطريقتين:"
echo ""
echo "الطريقة 1: HTTPS (يحتاج اسم مستخدم وكلمة مرور GitHub)"
echo "------------------------------------------------------"
echo "git push -u origin main"
echo ""
echo "الطريقة 2: SSH (إذا كان مضبوطاً)"
echo "----------------------------------"
echo "git push -u origin main"
echo ""
echo "الطريقة 3: GitHub CLI (الأسهل)"
echo "-------------------------------"
echo "gh auth login"
echo "git push -u origin main"
echo ""
echo "📌 ملاحظة: إذا استخدمت HTTPS، استخدم رمز GitHub الشخصي (PAT)"
echo "   كـ password بدلاً من كلمة المرور العادية"
echo ""
echo "لإنشاء PAT:"
echo "1. اذهب إلى https://github.com/settings/tokens"
echo "2. انقر Generate new token (classic)"
echo "3. اختر scope: repo"
echo "4. انقر Generate token"
echo "5. انسخ الرمز واستخدمه كـ password"
echo ""
