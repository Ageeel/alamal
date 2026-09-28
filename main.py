import flet as ft
from supabase import create_client, Client

# ضع روابط مشروعك في Supabase هنا
SUPABASE_URL = "https://mtqowejuobffqkzfhzv.supabase.co"
SUPABASE_ANON_KEY = "مفتاح_الـ_anon_العام_الخاص_بك"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def main(page: ft.Page):
    page.title = "ملتقى الفكر"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    status_text = ft.Text("جاري التحقق من الإشعارات...", size=16)

    # دالة جلب وحفظ الـ FCM Token
    def save_fcm_token_to_supabase(token: str):
        try:
            # نقوم بحفظ أو تحديث الـ Token في جدول devices
            response = supabase.table("devices").upsert({
                "user_id": "default_user", # يمكنك تغييره لاحقاً بمعرف المستخدم الفعلي إذا كان يسجل دخولاً
                "fcm_token": token
            }, on_conflict="fcm_token").execute()

            status_text.value = "تم تفعيل استقبال الإشعارات بنجاح! ✅"
            page.update()
            print("تم الحفظ بنجاح:", response)
        except Exception as e:
            status_text.value = f"حدث خطأ أثناء الحفظ: {e}"
            page.update()
            print("خطأ:", e)

    # محاكاة أو جلب الـ Token الفعلي عند فتح التطبيق على الأندرويد
    def get_device_token(e):
        # ملاحظة: في بيئة الأندرويد الحقيقية بعد دمج مكتبات الإشعارات، 
        # سيتم جلب الرمز الحقيقي من نظام فايربيس في الهاتف.
        sample_token = "APA91bF_FCM_TOKEN_EXAMPLE_FROM_ANDROID_DEVICE"
        
        status_text.value = "جاري إرسال الرمز إلى قاعدة البيانات..."
        page.update()
        
        # استدعاء دالة الحفظ
        save_fcm_token_to_supabase(sample_token)

    page.add(
        ft.Column([
            ft.Text("مرحباً بك في تطبيق ملتقى الفكر", size=22, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            status_text,
            ft.Container(height=20),
            ft.ElevatedButton(
                text="تفعيل الإشعارات الآن",
                icon=ft.icons.NOTIFICATIONS_ACTIVE,
                on_click=get_device_token
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
